from enum import Enum as PythonEnum


class UserRole(str, PythonEnum):
    USER = "user"
    ADMIN = "admin"


class TransactionType(str, PythonEnum):
    """거래 유형"""
    DEPOSIT = "deposit"  # 입금
    WITHDRAWAL = "withdrawal"  # 출금


class AdvisoryStatus(str, PythonEnum):
    """자문 상태"""
    PENDING = "pending"  # 대기
    COMPLETED = "completed"  # 완료
    FAILED = "failed"  # 실패


class PortfolioType(str, PythonEnum):
    """포트폴리오 유형"""
    BALANCED = "balanced"  # 균형형
    AGGRESSIVE = "aggressive"  # 공격형
    CONSERVATIVE = "conservative"  # 보수형
