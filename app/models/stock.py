from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Enum, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func as sql_func

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
    last_updated = Column(DateTime(timezone=True), server_default=sql_func.now(), onupdate=sql_func.now(), comment="마지막 업데이트 시간")

    # Relationships
    users = relationship("UserStock", back_populates="stock")
    recommendations = relationship("AdvisoryRecommendation", back_populates="stock")

    def __repr__(self):
        return f"{self.code} - {self.name}"

    @classmethod
    def get_total_count(cls, db: Session) -> int:
        """현재 등록된 총 증권 개수를 반환합니다."""
        return db.query(func.count(cls.id)).scalar()

    @classmethod
    def can_delete(cls, db: Session) -> bool:
        """증권 삭제가 가능한지 확인합니다. (최소 10개 이상일 때만 가능)"""
        return cls.get_total_count(db) > 10

    @classmethod
    def get_seed_data(cls) -> list:
        """시스템 초기화를 위한 시드 데이터를 반환합니다."""
        return [
            cls(
                code="005930",  # 삼성전자
                name="삼성전자",
                current_price=75000.0,
                market_cap=450000000000000.0,
                volume=15000000,
                high_price=76000.0,
                low_price=74000.0,
                open_price=74500.0,
                prev_close=74500.0,
                change_rate=0.67,
                change_amount=500.0,
                pe_ratio=12.5,
                dividend_yield=2.1,
                sector="전기전자",
                industry="반도체",
                description="글로벌 전자기업"
            ),
            cls(
                code="035720",  # 카카오
                name="카카오",
                current_price=45000.0,
                market_cap=200000000000000.0,
                volume=8000000,
                high_price=46000.0,
                low_price=44000.0,
                open_price=44500.0,
                prev_close=44500.0,
                change_rate=1.12,
                change_amount=500.0,
                pe_ratio=25.3,
                dividend_yield=0.5,
                sector="IT",
                industry="소프트웨어",
                description="IT 플랫폼 기업"
            ),
            cls(
                code="035420",  # NAVER
                name="NAVER",
                current_price=250000.0,
                market_cap=150000000000000.0,
                volume=5000000,
                high_price=255000.0,
                low_price=245000.0,
                open_price=248000.0,
                prev_close=248000.0,
                change_rate=0.81,
                change_amount=2000.0,
                pe_ratio=30.5,
                dividend_yield=0.3,
                sector="IT",
                industry="소프트웨어",
                description="인터넷 서비스 기업"
            ),
            cls(
                code="000660",  # SK하이닉스
                name="SK하이닉스",
                current_price=120000.0,
                market_cap=180000000000000.0,
                volume=12000000,
                high_price=122000.0,
                low_price=118000.0,
                open_price=119000.0,
                prev_close=119000.0,
                change_rate=0.84,
                change_amount=1000.0,
                pe_ratio=8.5,
                dividend_yield=1.2,
                sector="전기전자",
                industry="반도체",
                description="메모리 반도체 기업"
            ),
            cls(
                code="207940",  # 삼성바이오로직스
                name="삼성바이오로직스",
                current_price=850000.0,
                market_cap=120000000000000.0,
                volume=3000000,
                high_price=860000.0,
                low_price=840000.0,
                open_price=845000.0,
                prev_close=845000.0,
                change_rate=0.59,
                change_amount=5000.0,
                pe_ratio=45.2,
                dividend_yield=0.2,
                sector="제약",
                industry="바이오",
                description="바이오시밀러 기업"
            ),
            cls(
                code="005380",  # 현대차
                name="현대차",
                current_price=180000.0,
                market_cap=380000000000000.0,
                volume=9000000,
                high_price=182000.0,
                low_price=178000.0,
                open_price=179000.0,
                prev_close=179000.0,
                change_rate=0.56,
                change_amount=1000.0,
                pe_ratio=6.8,
                dividend_yield=2.5,
                sector="자동차",
                industry="자동차",
                description="자동차 제조 기업"
            ),
            cls(
                code="051910",  # LG화학
                name="LG화학",
                current_price=450000.0,
                market_cap=65000000000000.0,
                volume=4000000,
                high_price=455000.0,
                low_price=445000.0,
                open_price=448000.0,
                prev_close=448000.0,
                change_rate=0.45,
                change_amount=2000.0,
                pe_ratio=15.2,
                dividend_yield=1.8,
                sector="화학",
                industry="화학",
                description="화학 기업"
            ),
            cls(
                code="006400",  # 삼성SDI
                name="삼성SDI",
                current_price=550000.0,
                market_cap=95000000000000.0,
                volume=3500000,
                high_price=555000.0,
                low_price=545000.0,
                open_price=548000.0,
                prev_close=548000.0,
                change_rate=0.36,
                change_amount=2000.0,
                pe_ratio=20.5,
                dividend_yield=1.0,
                sector="전기전자",
                industry="2차전지",
                description="2차전지 기업"
            ),
            cls(
                code="068270",  # 셀트리온
                name="셀트리온",
                current_price=180000.0,
                market_cap=120000000000000.0,
                volume=6000000,
                high_price=182000.0,
                low_price=178000.0,
                open_price=179000.0,
                prev_close=179000.0,
                change_rate=0.56,
                change_amount=1000.0,
                pe_ratio=35.8,
                dividend_yield=0.3,
                sector="제약",
                industry="바이오",
                description="바이오시밀러 기업"
            ),
            cls(
                code="105560",  # KB금융
                name="KB금융",
                current_price=55000.0,
                market_cap=220000000000000.0,
                volume=7000000,
                high_price=56000.0,
                low_price=54000.0,
                open_price=54500.0,
                prev_close=54500.0,
                change_rate=0.92,
                change_amount=500.0,
                pe_ratio=6.2,
                dividend_yield=3.5,
                sector="금융",
                industry="은행",
                description="금융기업"
            )
        ]


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
    price_at_time = Column(Float, nullable=False, comment="추천 시점의 주가")
    total_investment = Column(Float, nullable=False, comment="총 투자금액")
    market_cap = Column(Float, nullable=False, comment="시가총액")
    change_rate = Column(Float, nullable=False, comment="등락률")
    volume = Column(Integer, nullable=False, comment="거래량")

    advisory_request = relationship("AdvisoryRequest", back_populates="recommendations")
    stock = relationship("Stock", back_populates="recommendations")
