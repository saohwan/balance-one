import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.settings import settings
from app.models.user import User
from app.models.stock import Stock
from app.models.stock import UserStock
from app.models.audit import AuditLog
from app.utils.constant.globals import UserRole

# MySQL 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# MySQL 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,  # 1시간마다 연결 재생성
    echo=True  # SQL 쿼리 로깅
)

# 세션 생성
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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


@pytest.fixture(scope="session")
def db_engine():
    """테스트용 데이터베이스 엔진 생성"""
    # 테스트용 테이블 생성
    Base.metadata.create_all(bind=engine)
    yield engine
    # 테스트 종료 후 테이블 정리
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """테스트용 데이터베이스 세션 생성"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    # 테스트 종료 후 롤백 및 연결 정리
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def override_get_current_admin_user():
    """테스트용 관리자 사용자 의존성 오버라이드"""
    return test_admin_user
