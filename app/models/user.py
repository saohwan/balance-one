import enum

from sqlalchemy import Boolean, Column, String, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.utils.constant.globals import UserRole
from .common import CommonModel


# class UserRole(str, PythonEnum):
# 	user = "user"
# 	admin = "admin"

class PortfolioType(str, enum.Enum):
    """
    포트폴리오 유형을 정의하는 열거형
    사용자의 투자 성향에 따른 포트폴리오 구성을 결정합니다.
    """
    AGGRESSIVE = "aggressive"  # 최대한 많은 증권 구매
    BALANCED = "balanced"  # 중간 수준 증권 구매


class User(CommonModel):
    """
    사용자 정보를 저장하는 테이블
    시스템을 이용하는 모든 사용자의 기본 정보와 계정 상태를 관리합니다.
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False, comment="사용자 이메일 (로그인 ID)")
    hashed_password = Column(String(255), nullable=False, comment="암호화된 비밀번호")
    first_name = Column(String(255), comment="이름")
    last_name = Column(String(255), comment="성")
    role = Column(Enum(UserRole), default=UserRole.USER, comment="사용자 역할 (일반 사용자/관리자)")
    is_active = Column(Boolean, default=True, comment="계정 활성화 상태")
    balance = Column(Float, default=0.0, comment="보유 현금 잔고")
    portfolio_type = Column(Enum(PortfolioType), nullable=True, comment="선호 포트폴리오 유형")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    # Relationships
    stocks = relationship("UserStock", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    advisory_requests = relationship("AdvisoryRequest", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"{self.email}"


metadata = Base.metadata
