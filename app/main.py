# fastapi 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, account, advisory, admin
from app.core.settings import settings


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description="FastAPI 기반의 증권 자문 시스템 API",
        version=settings.VERSION,
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # CORS 설정
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app_.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
    app_.include_router(account.router, prefix=f"{settings.API_V1_STR}/account", tags=["account"])
    app_.include_router(advisory.router, prefix=f"{settings.API_V1_STR}/advisory", tags=["advisory"])
    app_.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

    return app_


app = create_app()


@app.get("/")
async def root():
    return {
        "message": "Welcome to Balance One API"
    }
