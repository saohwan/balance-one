from sqlalchemy import Column, Boolean, Integer, String , DateTime, func
import uuid

from sqlalchemy.orm import declarative_base

from app.core.database import Base


class CommonModel(Base):
    """
    모든 모델의 기본이 되는 추상 클래스
    공통적으로 사용되는 필드들을 정의합니다.
    """
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True, comment="UUID 형식의 고유 식별자")
    # id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True, comment="레코드 활성화 상태")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="수정 일시")
