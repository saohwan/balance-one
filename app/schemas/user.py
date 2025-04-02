from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, PortfolioType

class UserBase(BaseModel):
	email: EmailStr
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	portfolio_type: Optional[PortfolioType] = None

class UserCreate(UserBase):
	password: str

class UserLogin(UserBase):
	password: str

class UserUpdate(BaseModel):
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	portfolio_type: Optional[PortfolioType] = None
	password: Optional[str] = None

class UserInDB(UserBase):
	id: str
	role: UserRole
	is_active: bool
	balance: float
	created_at: datetime
	updated_at: Optional[datetime] = None

	class Config:
		from_attributes = True

class User(UserInDB):
	pass

class UserBalance(BaseModel):
	balance: float
	stocks: list[dict]  # 보유 증권 목록

class Token(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str



