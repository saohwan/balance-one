import os
from enum import Enum
from typing import List

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

# .env 파일 로드
load_dotenv()


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    """
    TODO: 운영 단계에서는 환경 변수 항목들
    """
    # 프로젝트 기본 설정
    PROJECT_NAME: str = "Balance One"
    DESCRIPTION: str = "Balance One API Server"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT

    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://user:password@db:3306/balance_one"
    )

    # JWT 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key-here")

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_EXPIRE_DAYS: int = 1  # 기존 ACCESS_TOKEN_EXPIRE_DAYS 대체
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # 보안 설정
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_TIMEOUT_MINUTES: int = 30

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"  # 추가 필드 허용
    )


# 전역 설정 객체 생성
settings = Settings()
