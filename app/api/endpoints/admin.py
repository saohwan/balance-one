import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.audit import AuditLog
from app.models.stock import Stock
from app.models.user import User
from app.schemas.stock import StockCreate, StockUpdate, Stock as StockSchema
from app.utils.audit import log_user_action

router = APIRouter()


@router.post("/stocks", response_model=StockSchema)
def create_stock(
        *,
        db: Session = Depends(get_db),
        stock_in: StockCreate,
        current_user: User = Depends(get_current_admin_user),
        request: Request
) -> Any:
    """
    새로운 증권을 등록합니다.
    """
    # 증권 코드 중복 체크
    stock = db.query(Stock).filter(Stock.code == stock_in.code).first()
    if stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 증권 코드입니다."
        )

    # 증권 생성
    stock = Stock(
        id=str(uuid.uuid4()),
        code=stock_in.code,
        name=stock_in.name,
        current_price=stock_in.current_price
    )

    db.add(stock)
    db.commit()
    db.refresh(stock)

    # 감사 로그 기록
    log_user_action(
        db,
        "create_stock",
        current_user.id,
        {
            "stock_code": stock_in.code,
            "stock_name": stock_in.name,
            "price": stock_in.current_price
        },
        request
    )

    return stock


@router.put("/stocks/{stock_id}", response_model=StockSchema)
def update_stock(
        *,
        db: Session = Depends(get_db),
        stock_id: str,
        stock_in: StockUpdate,
        current_user: User = Depends(get_current_admin_user),
        request: Request
) -> Any:
    """
    증권 정보를 업데이트합니다.
    """
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="증권을 찾을 수 없습니다."
        )

    # 업데이트할 필드만 업데이트
    update_data = stock_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stock, field, value)

    db.commit()
    db.refresh(stock)

    # 감사 로그 기록
    log_user_action(
        db,
        "update_stock",
        current_user.id,
        {
            "stock_id": stock_id,
            "updates": update_data
        },
        request
    )

    return stock


@router.delete("/stocks/{stock_id}")
def delete_stock(
        *,
        db: Session = Depends(get_db),
        stock_id: str,
        current_user: User = Depends(get_current_admin_user),
        request: Request
) -> Any:
    """
    증권을 삭제합니다.
    """
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="증권을 찾을 수 없습니다."
        )

    # 감사 로그 기록
    log_user_action(
        db,
        "delete_stock",
        current_user.id,
        {
            "stock_id": stock_id,
            "stock_code": stock.code,
            "stock_name": stock.name
        },
        request
    )

    db.delete(stock)
    db.commit()

    return {"message": "증권이 삭제되었습니다."}


@router.get("/stocks", response_model=List[StockSchema])
def get_stocks(
        *,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin_user),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    모든 증권 목록을 조회합니다.
    """
    stocks = (
        db.query(Stock)
        .order_by(Stock.code)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return stocks


@router.get("/audit-logs")
def get_audit_logs(
        *,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin_user),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    감사 로그를 조회합니다.
    """
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return logs
