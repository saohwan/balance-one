from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.stock import AdvisoryRequest, AdvisoryRecommendation
from app.schemas.stock import (
    AdvisoryRequestCreate,
    AdvisoryRequest as AdvisoryRequestSchema,
    AdvisoryRecommendation as AdvisoryRecommendationSchema
)
from app.utils.portfolio import calculate_portfolio, validate_portfolio
from app.utils.audit import log_user_action
import uuid

router = APIRouter()


@router.post("/request", response_model=AdvisoryRequestSchema)
def create_advisory_request(
        *,
        db: Session = Depends(get_db),
        request_in: AdvisoryRequestCreate,
        current_user: User = Depends(get_current_user),
        request: Request
) -> Any:
    """
    자문 요청을 생성합니다.
    """
    # 포트폴리오 추천 계산
    recommendations = calculate_portfolio(
        db,
        current_user.balance,
        request_in.portfolio_type
    )

    # 추천 결과 검증
    is_valid, message = validate_portfolio(recommendations, current_user.balance)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    # 자문 요청 생성
    advisory_request = AdvisoryRequest(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        portfolio_type=request_in.portfolio_type,
        status="completed"
    )

    db.add(advisory_request)
    db.commit()
    db.refresh(advisory_request)

    # 추천 결과 저장
    for rec in recommendations:
        recommendation = AdvisoryRecommendation(
            id=str(uuid.uuid4()),
            advisory_request_id=advisory_request.id,
            stock_id=rec["stock_id"],
            quantity=rec["quantity"],
            price_at_time=rec["price_at_time"]
        )
        db.add(recommendation)

    db.commit()

    # 감사 로그 기록
    log_user_action(
        db,
        "advisory_request",
        current_user.id,
        {
            "portfolio_type": request_in.portfolio_type,
            "recommendations_count": len(recommendations)
        },
        request
    )

    return advisory_request


@router.get("/requests", response_model=List[AdvisoryRequestSchema])
def get_advisory_requests(
        *,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 10
) -> Any:
    """
    자문 요청 내역을 조회합니다.
    """
    requests = (
        db.query(AdvisoryRequest)
        .filter(AdvisoryRequest.user_id == current_user.id)
        .order_by(AdvisoryRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return requests


@router.get("/requests/{request_id}", response_model=AdvisoryRequestSchema)
def get_advisory_request(
        *,
        db: Session = Depends(get_db),
        request_id: str,
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    특정 자문 요청의 상세 정보를 조회합니다.
    """
    advisory_request = (
        db.query(AdvisoryRequest)
        .filter(
            AdvisoryRequest.id == request_id,
            AdvisoryRequest.user_id == current_user.id
        )
        .first()
    )

    if not advisory_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="자문 요청을 찾을 수 없습니다."
        )

    return advisory_request
