import uuid
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.settings import settings
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
        form_data: OAuth2PasswordRequestForm = Depends(),
        request: Request
) -> Any:
    """
    사용자 로그인을 처리합니다.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 계정입니다."
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
