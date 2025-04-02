import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.stock import Stock, UserStock
from app.models.transaction import Transaction
from app.schemas.account import (
    UserStockResponse,
    TransactionResponse,
    UserBalanceResponse,
    UserProfileResponse,
    UserProfileUpdate
)
from app.schemas.stock import TransactionCreate, Transaction as TransactionSchema
from app.schemas.user import UserBalance
from app.utils.audit import log_user_action
from app.utils.constant.globals import TransactionType

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


@router.get("/stocks", response_model=List[UserStockResponse])
def get_user_stocks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자의 보유 주식 목록을 조회합니다."""
    user_stocks = db.query(UserStock).filter(UserStock.user_id == current_user.id).all()
    return user_stocks


@router.get("/transactions", response_model=List[TransactionResponse])
def get_user_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자의 거래 내역을 조회합니다."""
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    return transactions


@router.get("/balance", response_model=UserBalanceResponse)
def get_user_balance(
    current_user: User = Depends(get_current_user)
):
    """사용자의 계좌 잔고를 조회합니다."""
    return {"balance": current_user.balance}


@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """사용자의 프로필 정보를 조회합니다."""
    return current_user


@router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자의 프로필 정보를 업데이트합니다."""
    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user
