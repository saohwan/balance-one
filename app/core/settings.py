from pydantic_settings import BaseSettings
from enum import Enum
from typing import Optional, List
import os
from dotenv import load_dotenv

from app.utils.env import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

# .env 파일 로드
load_dotenv()


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    # 프로젝트 기본 설정
    PROJECT_NAME: str = "Balance One"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 데이터베이스 설정
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://user:password@db:3306/balance_one"
    )

    # JWT 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # 보안 설정
    PASSWORD_MIN_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOGIN_TIMEOUT_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"


# 전역 설정 객체 생성
settings = Settings()
