import uuid
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.settings import settings
from app.models.login_attempt import LoginAttempt
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, Token
from app.utils.audit import log_user_action
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)

router = APIRouter()

MAX_LOGIN_ATTEMPTS = 5  # 최대 로그인 시도 횟수
LOGIN_TIMEOUT_MINUTES = 30  # 로그인 시도 제한 시간 (분)


class LoginRequest(BaseModel):
    username: str
    password: str


def check_login_attempts(db: Session, user: User, ip_address: str) -> bool:
    """로그인 시도 횟수를 확인하고 제한을 적용합니다."""
    # 최근 30분 동안의 실패한 로그인 시도 횟수 확인
    recent_attempts = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == user.id,
        LoginAttempt.ip_address == ip_address,
        LoginAttempt.is_successful == False,
        LoginAttempt.last_attempt_at >= func.now() - timedelta(minutes=LOGIN_TIMEOUT_MINUTES)
    ).order_by(LoginAttempt.last_attempt_at.desc()).first()

    if recent_attempts and recent_attempts.attempt_count >= MAX_LOGIN_ATTEMPTS:
        return False
    return True


def record_login_attempt(
        db: Session,
        user: User,
        ip_address: str,
        user_agent: str,
        is_successful: bool
) -> None:
    """로그인 시도 기록을 저장합니다."""
    # 최근 시도 기록 조회
    recent_attempt = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == user.id,
        LoginAttempt.ip_address == ip_address,
        LoginAttempt.last_attempt_at >= func.now() - timedelta(minutes=LOGIN_TIMEOUT_MINUTES)
    ).order_by(LoginAttempt.last_attempt_at.desc()).first()

    if recent_attempt and not is_successful:
        # 실패한 경우 시도 횟수 증가
        recent_attempt.attempt_count += 1
        recent_attempt.last_attempt_at = func.now()
    else:
        # 새로운 시도 기록 생성
        new_attempt = LoginAttempt(
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=is_successful,
            attempt_count=1
        )
        db.add(new_attempt)

    db.commit()


@router.post("/register", response_model=UserSchema)
def register(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate,
        request: Request
) -> Any:
    """
    새로운 사용자를 등록합니다.
    """
    # 이메일 중복 체크
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )

    # 사용자 생성
    user = User(
        id=str(uuid.uuid4()),
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        portfolio_type=user_in.portfolio_type
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 감사 로그 기록
    log_user_action(db, "register", user.id, request=request)

    return user


@router.post("/login", response_model=Token)
def login(
        *,
        db: Session = Depends(get_db),
        login_data: LoginRequest,
        request: Request
) -> Any:
    """
    사용자 로그인을 처리합니다.
    """
    user = db.query(User).filter(User.email == login_data.username).first()

    # IP 주소와 User-Agent 정보 추출
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "")

    if not user:
        # 존재하지 않는 사용자의 경우에도 시도 기록
        record_login_attempt(
            db=db,
            user=User(id=str(uuid.uuid4()), email=login_data.username),  # 임시 사용자 객체
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    # 로그인 시도 횟수 확인
    if not check_login_attempts(db, user, ip_address):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"로그인 시도 횟수가 너무 많습니다. {LOGIN_TIMEOUT_MINUTES}분 후에 다시 시도해주세요."
        )

    if not verify_password(login_data.password, user.hashed_password):
        # 비밀번호가 틀린 경우 시도 기록
        record_login_attempt(
            db=db,
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            is_successful=False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 계정입니다."
        )

    # 로그인 성공 기록
    record_login_attempt(
        db=db,
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        is_successful=True
    )

    # 토큰 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.id})

    # 감사 로그 기록
    log_user_action(db, "login", user.id, request=request)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(
        *,
        db: Session = Depends(get_db),
        refresh_token: str,
        request: Request
) -> Any:
    """
    리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급합니다.
    """
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 리프레시 토큰입니다."
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )

    # 새로운 액세스 토큰 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    # 감사 로그 기록
    log_user_action(db, "refresh_token", user.id, request=request)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
