import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_current_admin_user
from app.core.settings import settings
from app.main import app
from app.models.user import User
from app.utils.constant.globals import UserRole

# API 경로 설정
API_V1_STR = settings.API_V1_STR
ADMIN_API_PREFIX = f"{API_V1_STR}/admin"

# 테스트용 관리자 사용자
test_admin_user = User(
    id="test-admin-id",
    email="admin@test.com",
    role=UserRole.ADMIN,
    hashed_password="test_password",
    is_active=True,
    first_name="Test",
    last_name="Admin"
)

# 테스트용 증권 데이터
test_stocks = [
    {
        "code": "005930",
        "name": "삼성전자",
        "current_price": 75000,
        "market_cap": 4500000000000,
        "volume": 15000000,
        "high_price": 76000,
        "low_price": 74000,
        "open_price": 74500,
        "prev_close": 74500,
        "change_rate": 0.67,
        "change_amount": 500
    },
    {
        "code": "035720",
        "name": "카카오",
        "current_price": 45000,
        "market_cap": 200000000000,
        "volume": 8000000,
        "high_price": 46000,
        "low_price": 44000,
        "open_price": 44500,
        "prev_close": 44500,
        "change_rate": 1.12,
        "change_amount": 500
    },
    {
        "code": "035420",
        "name": "NAVER",
        "current_price": 250000,
        "market_cap": 400000000000,
        "volume": 5000000,
        "high_price": 255000,
        "low_price": 245000,
        "open_price": 248000,
        "prev_close": 248000,
        "change_rate": 0.81,
        "change_amount": 2000
    },
    {
        "code": "000660",
        "name": "SK하이닉스",
        "current_price": 150000,
        "market_cap": 100000000000,
        "volume": 3000000,
        "high_price": 155000,
        "low_price": 145000,
        "open_price": 148000,
        "prev_close": 148000,
        "change_rate": 1.35,
        "change_amount": 2000
    },
    {
        "code": "207940",
        "name": "삼성바이오로직스",
        "current_price": 800000,
        "market_cap": 500000000000,
        "volume": 1000000,
        "high_price": 810000,
        "low_price": 790000,
        "open_price": 795000,
        "prev_close": 795000,
        "change_rate": 0.63,
        "change_amount": 5000
    },
    {
        "code": "005380",
        "name": "현대차",
        "current_price": 180000,
        "market_cap": 350000000000,
        "volume": 4000000,
        "high_price": 185000,
        "low_price": 175000,
        "open_price": 178000,
        "prev_close": 178000,
        "change_rate": 1.12,
        "change_amount": 2000
    },
    {
        "code": "051910",
        "name": "LG화학",
        "current_price": 450000,
        "market_cap": 300000000000,
        "volume": 2000000,
        "high_price": 460000,
        "low_price": 440000,
        "open_price": 445000,
        "prev_close": 445000,
        "change_rate": 1.12,
        "change_amount": 5000
    },
    {
        "code": "006400",
        "name": "삼성SDI",
        "current_price": 550000,
        "market_cap": 400000000000,
        "volume": 1500000,
        "high_price": 560000,
        "low_price": 540000,
        "open_price": 545000,
        "prev_close": 545000,
        "change_rate": 0.92,
        "change_amount": 5000
    },
    {
        "code": "068270",
        "name": "셀트리온",
        "current_price": 180000,
        "market_cap": 250000000000,
        "volume": 2500000,
        "high_price": 185000,
        "low_price": 175000,
        "open_price": 178000,
        "prev_close": 178000,
        "change_rate": 1.12,
        "change_amount": 2000
    },
    {
        "code": "003670",
        "name": "포스코퓨처엠",
        "current_price": 350000,
        "market_cap": 150000000000,
        "volume": 1000000,
        "high_price": 360000,
        "low_price": 340000,
        "open_price": 345000,
        "prev_close": 345000,
        "change_rate": 1.45,
        "change_amount": 5000
    }
]


@pytest.fixture
def db_session():
    """테스트용 데이터베이스 세션 생성"""
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def override_get_current_admin_user():
    """테스트용 관리자 사용자 의존성 오버라이드"""

    async def _override_get_current_admin_user():
        return test_admin_user

    return _override_get_current_admin_user


@pytest.fixture
def test_app(override_get_current_admin_user):
    """테스트용 FastAPI 앱 생성"""
    app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user
    return app


@pytest.fixture
def test_client(test_app):
    """테스트용 클라이언트 생성"""
    return TestClient(test_app)


def test_create_stock(test_client, db_session):
    """증권 등록 API 테스트"""
    test_stock = test_stocks[0]
    response = test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=test_stock)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == test_stock["code"]
    assert data["name"] == test_stock["name"]
    assert data["current_price"] == test_stock["current_price"]
    assert data["market_cap"] == test_stock["market_cap"]


def test_create_duplicate_stock(test_client, db_session):
    """중복 증권 등록 방지 테스트"""
    test_stock = test_stocks[0]

    # 첫 번째 등록
    response1 = test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=test_stock)
    assert response1.status_code == 200

    # 중복 등록 시도
    response2 = test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=test_stock)
    assert response2.status_code == 400
    assert "이미 등록된 증권 코드입니다" in response2.json()["detail"]


def test_update_stock(test_client, db_session):
    """증권 가격 업데이트 API 테스트"""
    # 먼저 증권 등록
    test_stock = test_stocks[0]
    create_response = test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=test_stock)
    stock_id = create_response.json()["id"]

    # 가격 업데이트
    update_data = {"current_price": 76000}
    response = test_client.put(f"{ADMIN_API_PREFIX}/stocks/{stock_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["current_price"] == update_data["current_price"]


def test_delete_stock(test_client, db_session):
    """증권 삭제 API 테스트"""
    # 먼저 증권 등록
    test_stock = test_stocks[0]
    create_response = test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=test_stock)
    stock_id = create_response.json()["id"]

    # 증권 삭제
    response = test_client.delete(f"{ADMIN_API_PREFIX}/stocks/{stock_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "증권이 삭제되었습니다"

    # 삭제된 증권 조회 시도
    get_response = test_client.get(f"{ADMIN_API_PREFIX}/stocks/{stock_id}")
    assert get_response.status_code == 404


def test_bulk_stock_creation(test_client, db_session):
    """다수의 증권 등록 테스트"""
    for stock in test_stocks:
        response = test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=stock)
        assert response.status_code == 200

    # 전체 증권 목록 조회
    response = test_client.get(f"{ADMIN_API_PREFIX}/stocks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= len(test_stocks)


def test_stock_list_pagination(test_client, db_session):
    """증권 목록 페이지네이션 테스트"""
    # 먼저 여러 증권 등록
    for stock in test_stocks:
        test_client.post(f"{ADMIN_API_PREFIX}/stocks", json=stock)

    # 페이지네이션 파라미터로 조회
    response = test_client.get(f"{ADMIN_API_PREFIX}/stocks?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
