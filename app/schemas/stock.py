from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal

from pydantic import BaseModel, Field, validator

from app.models.stock import PortfolioType


class StockBase(BaseModel):
    """증권 기본 정보 스키마"""
    code: str  # 증권 코드
    name: str  # 증권명
    current_price: float  # 현재가
    market_cap: float  # 시가총액
    volume: int  # 거래량
    high_price: float  # 고가
    low_price: float  # 저가
    open_price: float  # 시가
    prev_close: float  # 전일 종가
    change_rate: float  # 등락률
    change_amount: float  # 등락금액


class StockCreate(StockBase):
    """증권 생성 스키마"""
    pass


class StockUpdate(BaseModel):
    """증권 정보 수정 스키마"""
    name: Optional[str] = None  # 증권명 (선택)
    current_price: Optional[float] = None  # 현재가 (선택)
    market_cap: Optional[float] = None  # 시가총액 (선택)
    volume: Optional[int] = None  # 거래량 (선택)
    high_price: Optional[float] = None  # 고가 (선택)
    low_price: Optional[float] = None  # 저가 (선택)
    open_price: Optional[float] = None  # 시가 (선택)
    prev_close: Optional[float] = None  # 전일 종가 (선택)
    change_rate: Optional[float] = None  # 등락률 (선택)
    change_amount: Optional[float] = None  # 등락금액 (선택)


class StockInDB(StockBase):
    """데이터베이스에 저장된 증권 정보 스키마"""
    id: str  # 증권 ID
    created_at: datetime  # 생성일시
    updated_at: Optional[datetime] = None  # 수정일시

    class Config:
        from_attributes = True


class Stock(StockInDB):
    """증권 정보 응답 스키마"""
    pass


class UserStockBase(BaseModel):
    """사용자 보유 증권 기본 정보 스키마"""
    stock_id: str  # 증권 ID
    quantity: int  # 보유 수량
    average_price: float  # 평균 매수가


class UserStockCreate(UserStockBase):
    """사용자 보유 증권 생성 스키마"""
    pass


class UserStockInDB(UserStockBase):
    """데이터베이스에 저장된 사용자 보유 증권 정보 스키마"""
    id: str  # 보유 증권 ID
    user_id: str  # 사용자 ID
    created_at: datetime  # 생성일시
    updated_at: Optional[datetime] = None  # 수정일시

    class Config:
        from_attributes = True


class UserStock(UserStockInDB):
    """사용자 보유 증권 정보 응답 스키마"""
    stock: Stock  # 증권 상세 정보


class TransactionBase(BaseModel):
    """거래 기본 정보 스키마"""
    type: str   # 거래 유형 ('deposit' 입금 또는 'withdraw' 출금)
    amount: float = Field(..., gt=0, description="거래 금액 (원화)")  # 거래 금액

    @validator('amount')
    def validate_amount(cls, v):
        """금액 유효성 검사"""
        if v <= 0:
            raise ValueError("금액은 0보다 커야 합니다.")
        if v > 1000000000:  # 10억원 제한
            raise ValueError("금액은 10억원을 초과할 수 없습니다.")
        return round(v, 0)  # 원화는 소수점 없이 반올림


class TransactionCreate(TransactionBase):
    """거래 생성 스키마"""
    pass


class TransactionInDB(TransactionBase):
    """데이터베이스에 저장된 거래 정보 스키마"""
    id: str  # 거래 ID
    user_id: str  # 사용자 ID
    status: str  # 거래 상태
    ip_address: Optional[str] = None  # 거래 IP 주소
    created_at: datetime  # 생성일시
    updated_at: Optional[datetime] = None  # 수정일시

    class Config:
        from_attributes = True


class Transaction(TransactionInDB):
    """거래 정보 응답 스키마"""
    def format_amount(self) -> str:
        """금액을 원화 형식으로 포맷팅"""
        return f"{self.amount:,.0f}원"


class AdvisoryRequestBase(BaseModel):
    """자문 요청 기본 정보 스키마"""
    portfolio_type: PortfolioType  # 포트폴리오 유형


class AdvisoryRequestCreate(AdvisoryRequestBase):
    """자문 요청 생성 스키마"""
    pass


class AdvisoryRequestInDB(AdvisoryRequestBase):
    """데이터베이스에 저장된 자문 요청 정보 스키마"""
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdvisoryRequest(AdvisoryRequestInDB):
    """자문 요청 정보 응답 스키마"""
    recommendations: List[AdvisoryRecommendation]  # 추천 증권 목록
    total_investment: float  # 총 투자금액
    portfolio_summary: Dict[str, Any]  # 포트폴리오 요약 정보

    def format_summary(self) -> Dict[str, str]:
        """포트폴리오 요약 정보를 포맷팅"""
        return {
            "total_investment": f"{self.total_investment:,.0f}원",
            "num_stocks": f"{len(self.recommendations)}개",
            "average_investment": f"{self.total_investment / len(self.recommendations):,.0f}원"
        }


class AdvisoryRecommendationBase(BaseModel):
    """자문 추천 기본 정보 스키마"""
    stock_id: str  # 증권 ID
    quantity: int  # 추천 수량
    price_at_time: float  # 추천 시점 가격
    market_cap: float  # 시가총액
    change_rate: float  # 등락률
    volume: int  # 거래량
    total_investment: float  # 총 투자금액

    def format_amounts(self) -> Dict[str, str]:
        """금액 정보를 포맷팅"""
        return {
            "price": f"{self.price_at_time:,.0f}원",
            "market_cap": f"{self.market_cap:,.0f}원",
            "total_investment": f"{self.total_investment:,.0f}원",
            "change_rate": f"{self.change_rate:+.2f}%",
            "volume": f"{self.volume:,}주"
        }


class AdvisoryRecommendationCreate(AdvisoryRecommendationBase):
    """자문 추천 생성 스키마"""
    advisory_request_id: str  # 자문 요청 ID


class AdvisoryRecommendationInDB(AdvisoryRecommendationBase):
    """데이터베이스에 저장된 자문 추천 정보 스키마"""
    id: str  # 추천 ID
    advisory_request_id: str  # 자문 요청 ID
    created_at: datetime  # 생성일시

    class Config:
        from_attributes = True


class AdvisoryRecommendation(AdvisoryRecommendationInDB):
    """자문 추천 정보 응답 스키마"""
    stock: Stock  # 증권 상세 정보
