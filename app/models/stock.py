from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.common import Base


class Stock(Base):
    """
    증권 정보를 저장하는 테이블
    거래소에 상장된 모든 증권의 기본 정보를 관리합니다.
    """
    __tablename__ = "stocks"

    id = Column(String(36), primary_key=True, index=True, comment="UUID 형식의 고유 식별자")
    code = Column(String(20), unique=True, index=True, nullable=False, comment="증권 거래소 코드 (예: 005930)")
    name = Column(String(255), nullable=False, comment="증권명 (예: 삼성전자)")
    current_price = Column(Float, nullable=False, comment="현재 주가")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    # Relationships
    users = relationship("UserStock", back_populates="stock")
    recommendations = relationship("AdvisoryRecommendation", back_populates="stock")


class UserStock(Base):
    """
    사용자의 보유 증권 정보를 저장하는 테이블
    각 사용자가 보유한 증권의 수량과 평균 매수가를 관리합니다.
    """
    __tablename__ = "user_stocks"

    id = Column(String(36), primary_key=True, index=True, comment="UUID 형식의 고유 식별자")
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False, comment="증권 ID")
    quantity = Column(Integer, nullable=False, comment="보유 수량")
    average_price = Column(Float, nullable=False, comment="평균 매수가")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    user = relationship("User", back_populates="stocks")
    stock = relationship("Stock", back_populates="users")


class Transaction(Base):
    """
    사용자의 입금/출금 거래 내역을 저장하는 테이블
    모든 금전 거래의 이력을 추적하고 관리합니다.
    """
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, index=True, comment="UUID 형식의 고유 식별자")
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    type = Column(String(20), nullable=False, comment="거래 유형 (입금/출금)")
    amount = Column(Float, nullable=False, comment="거래 금액")
    status = Column(String(20), nullable=False, comment="거래 상태 (완료/대기/실패)")
    ip_address = Column(String(45), comment="거래 발생 IP 주소")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    user = relationship("User", back_populates="transactions")


class AdvisoryRequest(Base):
    """
    사용자의 자문 요청 정보를 저장하는 테이블
    포트폴리오 자문 요청의 상태와 결과를 관리합니다.
    """
    __tablename__ = "advisory_requests"

    id = Column(String(36), primary_key=True, index=True, comment="UUID 형식의 고유 식별자")
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    portfolio_type = Column(String(20), nullable=False, comment="포트폴리오 유형 (공격형/균형형)")
    status = Column(String(20), nullable=False, comment="자문 상태 (대기/완료/실패)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    user = relationship("User", back_populates="advisory_requests")
    recommendations = relationship("AdvisoryRecommendation", back_populates="advisory_request")


class AdvisoryRecommendation(Base):
    """
    자문 요청에 대한 포트폴리오 추천 정보를 저장하는 테이블
    각 자문 요청에 대한 구체적인 증권 추천 내용을 관리합니다.
    """
    __tablename__ = "advisory_recommendations"

    id = Column(String(36), primary_key=True, index=True, comment="UUID 형식의 고유 식별자")
    advisory_request_id = Column(String(36), ForeignKey("advisory_requests.id"), nullable=False, comment="자문 요청 ID")
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False, comment="추천 증권 ID")
    quantity = Column(Integer, nullable=False, comment="추천 수량")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 일시")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="수정 일시")

    advisory_request = relationship("AdvisoryRequest", back_populates="recommendations")
    stock = relationship("Stock", back_populates="recommendations")
