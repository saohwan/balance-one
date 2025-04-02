from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.utils.constant.globals import TransactionType, AdvisoryStatus, PortfolioType
from app.models.common import CommonModel


class Stock(CommonModel):
    """
    증권 정보를 저장하는 테이블
    거래소에 상장된 모든 증권의 기본 정보를 관리합니다.
    """
    __tablename__ = "stocks"

    code = Column(String(20), unique=True, index=True, nullable=False, comment="증권 거래소 코드 (예: 005930)")
    name = Column(String(255), nullable=False, comment="증권명 (예: 삼성전자)")
    current_price = Column(Float, nullable=False, comment="현재 주가")
    market_cap = Column(Float, nullable=False, comment="시가총액")
    volume = Column(Integer, nullable=False, comment="거래량")
    high_price = Column(Float, nullable=False, comment="고가")
    low_price = Column(Float, nullable=False, comment="저가")
    open_price = Column(Float, nullable=False, comment="시가")
    prev_close = Column(Float, nullable=False, comment="전일 종가")
    change_rate = Column(Float, nullable=False, comment="등락률")
    change_amount = Column(Float, nullable=False, comment="등락금액")
    pe_ratio = Column(Float, nullable=True, comment="PER")
    dividend_yield = Column(Float, nullable=True, comment="배당수익률")
    sector = Column(String(50), nullable=True, comment="섹터")
    industry = Column(String(50), nullable=True, comment="산업")
    description = Column(String(500), nullable=True, comment="증권 설명")
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="마지막 업데이트 시간")

    # Relationships
    users = relationship("UserStock", back_populates="stock")
    recommendations = relationship("AdvisoryRecommendation", back_populates="stock")
    transactions = relationship("Transaction", back_populates="stock")

    def __repr__(self):
        return f"{self.code} - {self.name}"


class UserStock(CommonModel):
    """
    사용자의 보유 증권 정보를 저장하는 테이블
    각 사용자가 보유한 증권의 수량과 평균 매수가를 관리합니다.
    """
    __tablename__ = "user_stocks"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False, comment="증권 ID")
    quantity = Column(Integer, nullable=False, comment="보유 수량")
    average_price = Column(Float, nullable=False, comment="평균 매수가")

    user = relationship("User", back_populates="stocks")
    stock = relationship("Stock", back_populates="users")


class AdvisoryRequest(CommonModel):
    """
    사용자의 자문 요청 정보를 저장하는 테이블
    포트폴리오 자문 요청의 상태와 결과를 관리합니다.
    """
    __tablename__ = "advisory_requests"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    portfolio_type = Column(Enum(PortfolioType), nullable=False, comment="포트폴리오 유형")
    status = Column(String(20), nullable=False, comment="자문 상태 (대기/완료/실패)")

    user = relationship("User", back_populates="advisory_requests")
    recommendations = relationship("AdvisoryRecommendation", back_populates="advisory_request")


class AdvisoryRecommendation(CommonModel):
    """
    자문 요청에 대한 포트폴리오 추천 정보를 저장하는 테이블
    각 자문 요청에 대한 구체적인 증권 추천 내용을 관리합니다.
    """
    __tablename__ = "advisory_recommendations"

    advisory_request_id = Column(String(36), ForeignKey("advisory_requests.id"), nullable=False, comment="자문 요청 ID")
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False, comment="추천 증권 ID")
    quantity = Column(Integer, nullable=False, comment="추천 수량")

    advisory_request = relationship("AdvisoryRequest", back_populates="recommendations")
    stock = relationship("Stock", back_populates="recommendations")
