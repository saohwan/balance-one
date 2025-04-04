import enum

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, validates, declarative_base
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.common import CommonModel


class DepositWithdrawalType(str, enum.Enum):
    """입출금 유형"""
    DEPOSIT = "deposit"  # 입금
    WITHDRAWAL = "withdrawal"  # 출금


class DepositWithdrawalStatus(str, enum.Enum):
    """입출금 상태"""
    PENDING = "pending"  # 대기
    COMPLETED = "completed"  # 완료
    FAILED = "failed"  # 실패
    CANCELLED = "cancelled"  # 취소


class DepositWithdrawal(CommonModel):
    """
    입출금 정보를 저장하는 테이블
    사용자의 입금/출금 내역을 관리합니다.
    """
    __tablename__ = "deposit_withdrawals"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    type = Column(Enum(DepositWithdrawalType), nullable=False, comment="입출금 유형 (입금/출금)")
    amount = Column(Float, nullable=False, comment="금액 (원화)")
    status = Column(Enum(DepositWithdrawalStatus), nullable=False, default=DepositWithdrawalStatus.PENDING,
                    comment="입출금 상태")
    ip_address = Column(String(45), nullable=True, comment="입출금 발생 IP 주소")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    # Relationships
    user = relationship("User", back_populates="deposit_withdrawals")

    @validates('amount')
    def validate_amount(self, key, amount):
        """금액 유효성 검사"""
        if amount <= 0:
            raise ValueError("금액은 0보다 커야 합니다.")
        if amount > 1000000000:  # 10억원 제한
            raise ValueError("금액은 10억원을 초과할 수 없습니다.")
        return round(float(amount), 0)  # 원화는 소수점 없이 반올림

    def complete(self):
        """입출금 완료 처리"""
        self.status = DepositWithdrawalStatus.COMPLETED
        self.updated_at = func.now()

    def fail(self):
        """입출금 실패 처리"""
        self.status = DepositWithdrawalStatus.FAILED
        self.updated_at = func.now()

    def cancel(self):
        """입출금 취소 처리"""
        self.status = DepositWithdrawalStatus.CANCELLED
        self.updated_at = func.now()

    def is_completed(self) -> bool:
        """입출금 완료 여부 확인"""
        return self.status == DepositWithdrawalStatus.COMPLETED

    def is_pending(self) -> bool:
        """입출금 대기 여부 확인"""
        return self.status == DepositWithdrawalStatus.PENDING

    def is_failed(self) -> bool:
        """입출금 실패 여부 확인"""
        return self.status == DepositWithdrawalStatus.FAILED

    def is_cancelled(self) -> bool:
        """입출금 취소 여부 확인"""
        return self.status == DepositWithdrawalStatus.CANCELLED

    def get_formatted_amount(self) -> str:
        """포맷된 금액 반환 (원화)"""
        return f"{self.amount:,.0f}원"

    def __repr__(self):
        return f"{self.type.value} - {self.get_formatted_amount()} ({self.status.value})"
