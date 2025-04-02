import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.stock import UserStock
from app.models.user import User
from app.schemas.stock import TransactionCreate, Transaction as TransactionSchema, Transaction
from app.schemas.user import UserBalance
from app.utils.audit import log_user_action

router = APIRouter()


@router.post("/deposit", response_model=TransactionSchema)
def deposit(
        *,
        db: Session = Depends(get_db),
        transaction_in: TransactionCreate,
        current_user: User = Depends(get_current_user),
        request: Request
) -> Any:
    """
    입금을 처리합니다.
    """
    if transaction_in.type != "deposit":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 거래 유형입니다."
        )

    # 트랜잭션 생성
    transaction = Transaction(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        type=transaction_in.type,
        amount=transaction_in.amount,
        status="completed",
        ip_address=request.client.host
    )

    # 잔고 업데이트
    current_user.balance += transaction_in.amount

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # 감사 로그 기록
    log_user_action(
        db,
        "deposit",
        current_user.id,
        {"amount": transaction_in.amount},
        request
    )

    return transaction


@router.post("/withdraw", response_model=TransactionSchema)
def withdraw(
        *,
        db: Session = Depends(get_db),
        transaction_in: TransactionCreate,
        current_user: User = Depends(get_current_user),
        request: Request
) -> Any:
    """
    출금을 처리합니다.
    """
    if transaction_in.type != "withdraw":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 거래 유형입니다."
        )

    # 잔고 확인
    if current_user.balance < transaction_in.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잔고가 부족합니다."
        )

    # 트랜잭션 생성
    transaction = Transaction(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        type=transaction_in.type,
        amount=transaction_in.amount,
        status="completed",
        ip_address=request.client.host
    )

    # 잔고 업데이트
    current_user.balance -= transaction_in.amount

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # 감사 로그 기록
    log_user_action(
        db,
        "withdraw",
        current_user.id,
        {"amount": transaction_in.amount},
        request
    )

    return transaction


@router.get("/balance", response_model=UserBalance)
def get_balance(
        *,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    현재 잔고와 보유 증권 목록을 조회합니다.
    """
    # 보유 증권 목록 조회
    user_stocks = db.query(UserStock).filter(UserStock.user_id == current_user.id).all()

    stocks = []
    for user_stock in user_stocks:
        stocks.append({
            "stock_id": user_stock.stock_id,
            "quantity": user_stock.quantity,
            "average_price": user_stock.average_price,
            "current_price": user_stock.stock.current_price,
            "total_value": user_stock.quantity * user_stock.stock.current_price
        })

    return {
        "balance": current_user.balance,
        "stocks": stocks
    }


@router.get("/transactions", response_model=List[TransactionSchema])
def get_transactions(
        *,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 10
) -> Any:
    """
    거래 내역을 조회합니다.
    """
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return transactions
