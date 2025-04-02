from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.common import CommonModel


class UserStock(CommonModel):
    """
    사용자별 보유 주식 정보를 저장하는 테이블
    각 사용자가 보유한 주식의 수량과 평균 매수가를 관리합니다.
    """
    __tablename__ = "user_stocks"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False, comment="주식 ID")
    quantity = Column(Integer, nullable=False, default=0, comment="보유 수량")
    average_price = Column(Float, nullable=False, default=0.0, comment="평균 매수가")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    # Relationships
    user = relationship("User", back_populates="stocks")
    stock = relationship("Stock", back_populates="user_stocks")

    def __repr__(self):
        return f"{self.user.email} - {self.stock.symbol}: {self.quantity} shares" 