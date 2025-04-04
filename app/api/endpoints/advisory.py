import uuid
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.stock import AdvisoryRequest, AdvisoryRecommendation, Stock
from app.models.user import User
from app.schemas.stock import (
    AdvisoryRequestCreate,
    AdvisoryRequest as AdvisoryRequestSchema
)
from app.utils.audit import log_user_action
from app.utils.portfolio import calculate_portfolio, validate_portfolio

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
    자문 요청을 생성하고 포트폴리오를 추천합니다.
    
    Args:
        request_in: 자문 요청 정보 (포트폴리오 유형)
        current_user: 현재 로그인한 사용자
        request: HTTP 요청 객체
    
    Returns:
        자문 요청 정보와 추천 포트폴리오
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
            price_at_time=rec["price_at_time"],
            total_investment=rec["price_at_time"] * rec["quantity"],
            market_cap=rec["market_cap"],
            change_rate=rec["change_rate"],
            volume=rec["volume"]
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
            "recommendations_count": len(recommendations),
            "total_investment": sum(rec["total_investment"] for rec in recommendations)
        },
        request
    )

    # 응답 데이터 구성
    total_investment = sum(rec["total_investment"] for rec in recommendations)
    portfolio_summary = {
        "total_investment": total_investment,
        "num_stocks": len(recommendations),
        "average_investment": total_investment / len(recommendations) if recommendations else 0,
        "portfolio_type": request_in.portfolio_type,
        "risk_level": "높음" if request_in.portfolio_type == "aggressive" else "중간" if request_in.portfolio_type == "balanced" else "낮음"
    }

    # 추천 결과에 필요한 필드 추가
    recommendations_with_details = []
    for rec in recommendations:
        stock = db.query(Stock).filter(Stock.id == rec["stock_id"]).first()
        recommendations_with_details.append({
            "id": str(uuid.uuid4()),
            "advisory_request_id": advisory_request.id,
            "stock_id": rec["stock_id"],
            "stock": stock,
            "quantity": rec["quantity"],
            "price_at_time": rec["price_at_time"],
            "total_investment": rec["total_investment"],
            "market_cap": rec["market_cap"],
            "change_rate": rec["change_rate"],
            "volume": rec["volume"],
            "created_at": datetime.now()
        })

    return {
        "id": advisory_request.id,
        "user_id": advisory_request.user_id,
        "portfolio_type": advisory_request.portfolio_type,
        "status": advisory_request.status,
        "created_at": advisory_request.created_at,
        "recommendations": recommendations_with_details,
        "total_investment": total_investment,
        "portfolio_summary": portfolio_summary
    }


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
    
    Args:
        current_user: 현재 로그인한 사용자
        skip: 건너뛸 레코드 수
        limit: 반환할 최대 레코드 수
    
    Returns:
        자문 요청 목록
    """
    requests = (
        db.query(AdvisoryRequest)
        .filter(AdvisoryRequest.user_id == current_user.id)
        .order_by(AdvisoryRequest.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # 각 요청에 대한 상세 정보 추가
    result = []
    for request in requests:
        recommendations = (
            db.query(AdvisoryRecommendation)
            .filter(AdvisoryRecommendation.advisory_request_id == request.id)
            .all()
        )

        total_investment = sum(rec.quantity * rec.price_at_time for rec in recommendations)
        portfolio_summary = {
            "total_investment": total_investment,
            "num_stocks": len(recommendations),
            "average_investment": total_investment / len(recommendations) if recommendations else 0,
            "portfolio_type": request.portfolio_type,
            "risk_level": "높음" if request.portfolio_type == "aggressive" else "중간" if request.portfolio_type == "balanced" else "낮음"
        }

        result.append({
            **request.__dict__,
            "recommendations": recommendations,
            "total_investment": total_investment,
            "portfolio_summary": portfolio_summary
        })

    return result


@router.get("/requests/{request_id}", response_model=AdvisoryRequestSchema)
def get_advisory_request(
        *,
        db: Session = Depends(get_db),
        request_id: str,
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    특정 자문 요청의 상세 정보를 조회합니다.
    
    Args:
        request_id: 자문 요청 ID
        current_user: 현재 로그인한 사용자
    
    Returns:
        자문 요청 상세 정보
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

    # 추천 정보 조회
    recommendations = (
        db.query(AdvisoryRecommendation)
        .filter(AdvisoryRecommendation.advisory_request_id == request_id)
        .all()
    )

    # 포트폴리오 요약 정보 계산
    total_investment = sum(rec.quantity * rec.price_at_time for rec in recommendations)
    portfolio_summary = {
        "total_investment": total_investment,
        "num_stocks": len(recommendations),
        "average_investment": total_investment / len(recommendations) if recommendations else 0,
        "portfolio_type": advisory_request.portfolio_type,
        "risk_level": "높음" if advisory_request.portfolio_type == "aggressive" else "중간" if advisory_request.portfolio_type == "balanced" else "낮음"
    }

    return {
        **advisory_request.__dict__,
        "recommendations": recommendations,
        "total_investment": total_investment,
        "portfolio_summary": portfolio_summary
    }
