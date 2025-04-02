from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from .common import CommonModel


class AuditLog(Base):
    """
    시스템의 모든 주요 행위에 대한 감사 로그를 저장하는 테이블
    보안 감사와 시스템 모니터링을 위한 상세한 활동 기록을 관리합니다.

    """
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, index=True, comment="UUID 형식의 고유 식별자")
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, comment="행위를 수행한 사용자 ID (시스템 로그의 경우 Null)")
    action = Column(String(50), nullable=False, comment="수행된 행위 유형 (예: 로그인, 입금, 자문 요청)")
    details = Column(JSON, comment="행위에 대한 상세 정보")
    ip_address = Column(String(45), comment="행위 발생 IP 주소")
    user_agent = Column(String(255), comment="사용자 브라우저/클라이언트 정보")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")

    user = relationship("User", back_populates="audit_logs")
