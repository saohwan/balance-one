from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.settings import settings
from app.models.user import User
from app.utils.constant.globals import UserRole


# db connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    """
    현재 인증된 사용자를 가져오는 의존성 함수
    
    Args:
        db: 데이터베이스 세션
        token: JWT 토큰
        
    Returns:
        User: 현재 인증된 사용자
        
    Raises:
        HTTPException: 인증 실패 시 발생
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    현재 인증된 슈퍼유저를 가져오는 의존성 함수
    
    Args:
        current_user: 현재 인증된 사용자
        
    Returns:
        User: 현재 인증된 슈퍼유저
        
    Raises:
        HTTPException: 슈퍼유저가 아닐 경우 발생
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    현재 인증된 관리자 사용자를 가져오는 의존성 함수
    
    Args:
        current_user: 현재 인증된 사용자
        
    Returns:
        User: 현재 인증된 관리자 사용자
        
    Raises:
        HTTPException: 관리자 권한이 없는 경우 발생
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have admin privileges"
        )
    return current_user
