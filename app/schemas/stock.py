from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.stock import PortfolioType


class StockBase(BaseModel):
    """증권 기본 정보 스키마"""
    code: str  # 증권 코드
    name: str  # 증권명
    current_price: float  # 현재가


class StockCreate(StockBase):
    """증권 생성 스키마"""
    pass


class StockUpdate(BaseModel):
    """증권 정보 수정 스키마"""
    name: Optional[str] = None  # 증권명 (선택)
    current_price: Optional[float] = None  # 현재가 (선택)


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
    type: str  # 거래 유형 ('deposit' 입금 또는 'withdraw' 출금)
    amount: float  # 거래 금액


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
    pass


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
    recommendations: List['AdvisoryRecommendation']  # 추천 증권 목록


class AdvisoryRecommendationBase(BaseModel):
    """자문 추천 기본 정보 스키마"""
    stock_id: str  # 증권 ID
    quantity: int  # 추천 수량
    price_at_time: float  # 추천 시점 가격


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
