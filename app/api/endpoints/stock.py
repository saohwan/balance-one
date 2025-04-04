from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Stock
from app.models.user import User
from app.schemas.stock import StockCreate, StockUpdate, StockResponse

router = APIRouter()


@router.post("/", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def create_stock(
        stock_in: StockCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """새로운 증권을 생성합니다."""
    stock = Stock(**stock_in.model_dump())
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@router.get("/", response_model=list[StockResponse])
def get_stocks(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """등록된 모든 증권 목록을 조회합니다."""
    stocks = db.query(Stock).offset(skip).limit(limit).all()
    return stocks


@router.get("/{stock_id}", response_model=StockResponse)
def get_stock(
        stock_id: str,
        db: Session = Depends(get_db)
):
    """특정 증권의 상세 정보를 조회합니다."""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="증권을 찾을 수 없습니다."
        )
    return stock


@router.put("/{stock_id}", response_model=StockResponse)
def update_stock(
        stock_id: str,
        stock_in: StockUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """증권 정보를 업데이트합니다."""
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="증권을 찾을 수 없습니다."
        )

    for field, value in stock_in.model_dump(exclude_unset=True).items():
        setattr(stock, field, value)

    db.commit()
    db.refresh(stock)
    return stock


@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock(
        stock_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """증권을 삭제합니다."""
    # 최소 증권 개수 확인
    if not Stock.can_delete(db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="최소 10개 이상의 증권이 있어야 삭제가 가능합니다."
        )

    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="증권을 찾을 수 없습니다."
        )

    db.delete(stock)
    db.commit()
    return None
