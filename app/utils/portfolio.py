import random
from typing import List, Dict, Tuple

from sqlalchemy.orm import Session

from app.models.stock import Stock
from app.models.user import PortfolioType


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
        portfolio_type: 포트폴리오 유형 (aggressive, balanced, conservative)
        min_stocks: 최소 증권 수
        max_stocks: 최대 증권 수
    
    Returns:
        추천 증권 목록 (증권 ID, 수량, 가격 포함)
    """
    # 사용 가능한 모든 증권 조회
    available_stocks = db.query(Stock).filter(Stock.is_active == True).all()

    if not available_stocks:
        return []

    # 포트폴리오 유형에 따른 설정
    portfolio_settings = {
        PortfolioType.AGGRESSIVE: {
            "num_stocks": max_stocks,
            "balance_ratio": 0.95,  # 잔고의 95% 사용
            "min_stocks_by_price": [  # 가격대별 최소 주식 수
                {"max_price": 100000, "count": 2},  # 10만원 이하
                {"max_price": 500000, "count": 2},  # 50만원 이하
                {"max_price": float('inf'), "count": 1}  # 나머지
            ]
        },
        PortfolioType.BALANCED: {
            "num_stocks": (min_stocks + max_stocks) // 2,
            "balance_ratio": 0.7,  # 잔고의 70% 사용
            "min_stocks_by_price": [
                {"max_price": 100000, "count": 2},
                {"max_price": 300000, "count": 1},
                {"max_price": float('inf'), "count": 1}
            ]
        },
        PortfolioType.CONSERVATIVE: {
            "num_stocks": min_stocks,
            "balance_ratio": 0.5,  # 잔고의 50% 사용
            "min_stocks_by_price": [
                {"max_price": 100000, "count": 2},
                {"max_price": float('inf'), "count": 1}
            ]
        }
    }

    settings = portfolio_settings[portfolio_type]
    
    # 사용할 잔고 계산
    available_balance = balance * settings["balance_ratio"]

    # 가격대별로 주식 분류
    price_categories = {
        "low": [],    # 10만원 이하
        "medium": [], # 10만원 초과 50만원 이하
        "high": []    # 50만원 초과
    }
    
    for stock in available_stocks:
        if stock.current_price <= 100000:
            price_categories["low"].append(stock)
        elif stock.current_price <= 500000:
            price_categories["medium"].append(stock)
        else:
            price_categories["high"].append(stock)

    # 각 가격대별로 주식 선택
    selected_stocks = []
    for price_range in settings["min_stocks_by_price"]:
        max_price = price_range["max_price"]
        count = price_range["count"]
        
        # 해당 가격대의 주식들 선택
        candidate_stocks = [
            stock for stock in available_stocks
            if stock.current_price <= max_price and stock not in selected_stocks
        ]
        
        if candidate_stocks:
            # 시가총액과 거래량 기준으로 가중치 계산
            weights = [
                (stock.market_cap * stock.volume)
                for stock in candidate_stocks
            ]
            
            # 필요한 수만큼 선택
            for _ in range(min(count, len(candidate_stocks))):
                if not weights:
                    break
                selected_idx = weights.index(max(weights))
                selected_stocks.append(candidate_stocks[selected_idx])
                weights.pop(selected_idx)
                candidate_stocks.pop(selected_idx)

    if not selected_stocks:
        return []

    # 투자금액 분배
    total_price = sum(stock.current_price for stock in selected_stocks)
    recommendations = []
    
    for stock in selected_stocks:
        # 각 주식의 가격 비율에 따라 투자금액 할당
        stock_ratio = stock.current_price / total_price
        stock_investment = available_balance * stock_ratio
        
        # 수량 계산 (소수점 제거)
        quantity = int(stock_investment / stock.current_price)
        
        if quantity > 0:  # 최소 1주 이상
            recommendations.append({
                "stock_id": stock.id,
                "quantity": quantity,
                "price_at_time": stock.current_price,
                "total_investment": quantity * stock.current_price,
                "market_cap": stock.market_cap,
                "change_rate": stock.change_rate,
                "volume": stock.volume
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

    # 최소 투자 금액 검증
    min_investment = 100000  # 최소 10만원
    for rec in recommendations:
        if rec["total_investment"] < min_investment:
            return False, f"증권당 최소 투자 금액은 {min_investment:,}원입니다."

    return True, "포트폴리오가 유효합니다."
