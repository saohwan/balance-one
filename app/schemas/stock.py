from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.stock import PortfolioType

class StockBase(BaseModel):
    code: str
    name: str
    current_price: float

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    name: Optional[str] = None
    current_price: Optional[float] = None

class StockInDB(StockBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Stock(StockInDB):
    pass

class UserStockBase(BaseModel):
    stock_id: str
    quantity: int
    average_price: float

class UserStockCreate(UserStockBase):
    pass

class UserStockInDB(UserStockBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserStock(UserStockInDB):
    stock: Stock

class TransactionBase(BaseModel):
    type: str  # 'deposit' or 'withdraw'
    amount: float

class TransactionCreate(TransactionBase):
    pass

class TransactionInDB(TransactionBase):
    id: str
    user_id: str
    status: str
    ip_address: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Transaction(TransactionInDB):
    pass

class AdvisoryRequestBase(BaseModel):
    portfolio_type: PortfolioType

class AdvisoryRequestCreate(AdvisoryRequestBase):
    pass

class AdvisoryRequestInDB(AdvisoryRequestBase):
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AdvisoryRequest(AdvisoryRequestInDB):
    recommendations: List['AdvisoryRecommendation']

class AdvisoryRecommendationBase(BaseModel):
    stock_id: str
    quantity: int
    price_at_time: float

class AdvisoryRecommendationCreate(AdvisoryRecommendationBase):
    advisory_request_id: str

class AdvisoryRecommendationInDB(AdvisoryRecommendationBase):
    id: str
    advisory_request_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AdvisoryRecommendation(AdvisoryRecommendationInDB):
    stock: Stock 