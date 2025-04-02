from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from .common import CommonModel


class LoginAttempt(CommonModel):
    """
    로그인 시도 정보를 저장하는 테이블
    사용자의 로그인 시도 기록과 디바이스 정보를 관리합니다.
    """
    __tablename__ = "login_attempts"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    ip_address = Column(String(45), nullable=False, comment="로그인 시도 IP 주소")
    user_agent = Column(String(255), nullable=False, comment="사용자 브라우저/클라이언트 정보")
    is_successful = Column(Boolean, nullable=False, comment="로그인 성공 여부")
    attempt_count = Column(Integer, nullable=False, default=1, comment="연속 시도 횟수")
    last_attempt_at = Column(DateTime(timezone=True), server_default=func.now(), comment="마지막 시도 일시")

    # Relationships
    user = relationship("User", back_populates="login_attempts")

    def __repr__(self):
        return f"{self.user.email} - {self.ip_address} ({'성공' if self.is_successful else '실패'})" 