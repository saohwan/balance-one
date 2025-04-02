from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.models.stock import Stock
from app.models.user import PortfolioType
import random

def calculate_portfolio(
    db: Session,
    balance: float,
    portfolio_type: PortfolioType,
    min_stocks: int = 3,
    max_stocks: int = 5
) -> List[Dict[str, any]]:
    """
    사용자의 잔고와 포트폴리오 유형에 따라 증권 추천을 계산합니다.
    
    Args:
        db: 데이터베이스 세션
        balance: 사용자 잔고
        portfolio_type: 포트폴리오 유형 (aggressive or balanced)
        min_stocks: 최소 증권 수
        max_stocks: 최대 증권 수
    
    Returns:
        추천 증권 목록 (증권 ID, 수량, 가격 포함)
    """
    # 사용 가능한 모든 증권 조회
    available_stocks = db.query(Stock).all()
    
    if not available_stocks:
        return []
    
    # 포트폴리오 유형에 따른 증권 수 결정
    if portfolio_type == PortfolioType.AGGRESSIVE:
        num_stocks = max_stocks
        balance_ratio = 0.95  # 잔고의 95% 사용
    else:  # BALANCED
        num_stocks = min_stocks
        balance_ratio = 0.5  # 잔고의 50% 사용
    
    # 사용할 잔고 계산
    available_balance = balance * balance_ratio
    
    # 증권 수 조정
    num_stocks = min(num_stocks, len(available_stocks))
    
    # 랜덤하게 증권 선택
    selected_stocks = random.sample(available_stocks, num_stocks)
    
    # 각 증권별 투자 금액 계산
    investment_per_stock = available_balance / num_stocks
    
    recommendations = []
    for stock in selected_stocks:
        # 수량 계산 (소수점 제거)
        quantity = int(investment_per_stock / stock.current_price)
        
        if quantity > 0:  # 최소 1주 이상
            recommendations.append({
                "stock_id": stock.id,
                "quantity": quantity,
                "price_at_time": stock.current_price,
                "total_investment": quantity * stock.current_price
            })
    
    return recommendations

def validate_portfolio(
    recommendations: List[Dict[str, any]],
    balance: float
) -> Tuple[bool, str]:
    """
    포트폴리오 추천이 유효한지 검증합니다.
    
    Args:
        recommendations: 추천 증권 목록
        balance: 사용자 잔고
    
    Returns:
        (유효성 여부, 오류 메시지)
    """
    if not recommendations:
        return False, "추천할 증권이 없습니다."
    
    total_investment = sum(rec["total_investment"] for rec in recommendations)
    
    if total_investment > balance:
        return False, "추천된 포트폴리오가 잔고를 초과합니다."
    
    return True, "포트폴리오가 유효합니다." 