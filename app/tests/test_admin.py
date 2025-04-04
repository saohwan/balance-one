import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import uuid

client = TestClient(app)


@pytest.fixture(scope="session")
def create_test_admin_user():
    """ 테스트 관리자 계정을 생성하는 픽스처 """
    db = SessionLocal()
    test_email = "admin@example.com"
    test_password = "test"

    user = db.query(User).filter(User.email == test_email).first()
    if user:
        db.delete(user)
        db.commit()

    new_user = User(
        id=str(uuid.uuid4()),
        email=test_email,
        hashed_password=get_password_hash(test_password),
        is_active=True,
        role="admin"
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {
        "username": test_email,
        "password": test_password
    }


@pytest.fixture(scope="session")
def auth_token(create_test_admin_user):
    """ 관리자 계정의 인증 토큰을 생성하는 픽스처 """
    login_data = {
        "username": create_test_admin_user["username"],
        "password": create_test_admin_user["password"]
    }

    response = client.post("/api/v1/login", json=login_data)

    assert response.status_code == 200, "로그인 실패: 테스트 계정 확인 필요"

    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="function")
def stock_data():
    """ 테스트용 주식 데이터를 생성하는 픽스처 """
    return {
        "name": "Test Stock",
        "quantity": 10,
        "price": 1000,
        "code": f"TST-{uuid.uuid4().hex[:8]}",  # 랜덤한 증권 코드
        "current_price": 1000,
        "market_cap": 1000000000,
        "volume": 50000,
        "high_price": 1200,
        "low_price": 900,
        "open_price": 950,
        "prev_close": 980,
        "change_rate": 2.04,
        "change_amount": 20
    }




@pytest.fixture(scope="function")
def create_test_stock(stock_data, auth_token):
    """ 테스트용 주식 데이터를 생성하고 API를 통해 등록하는 픽스처 """
    response = client.post(
        "/api/v1/stocks",
        json=stock_data,
        headers=auth_headers(auth_token)
    )

    assert response.status_code == 201, f"Stock 생성 실패: {response.json()}"
    return response.json()



def auth_headers(token):
    """ 인증 토큰을 헤더 형식으로 변환하는 헬퍼 함수 """
    return {"Authorization": f"Bearer {token}"}


def test_create_stock_endpoint(stock_data, auth_token):
    """ 주식 생성 API 엔드포인트 테스트 """
    response = client.post(
        "/api/v1/stocks",
        json=stock_data,
        headers=auth_headers(auth_token)
    )
    assert response.status_code == 201
    assert response.json()["name"] == stock_data["name"]


def test_update_stock_endpoint(create_test_stock, auth_token):
    """ 주식 정보 업데이트 API 엔드포인트 테스트 """
    stock_id = create_test_stock["id"]
    update_data = {"name": "Updated Stock Name"}

    response = client.put(
        f"/api/v1/stocks/{stock_id}",
        json=update_data,
        headers=auth_headers(auth_token)
    )
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]


def test_delete_stock_endpoint(create_test_stock, auth_token):
    """ 주식 삭제 API 엔드포인트 테스트 """
    stock_id = create_test_stock["id"]

    response = client.delete(
        f"/api/v1/stocks/{stock_id}",
        headers=auth_headers(auth_token)
    )
    assert response.status_code == 200
    assert response.json()["message"] == "증권이 삭제되었습니다."


def test_get_stocks_endpoint(auth_token):
    """ 주식 목록 조회 API 엔드포인트 테스트 """
    response = client.get("/api/v1/stocks", headers=auth_headers(auth_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_audit_logs_endpoint(auth_token):
    """ 감사 로그 조회 API 엔드포인트 테스트 """
    response = client.get("/api/v1/audit-logs", headers=auth_headers(auth_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)