# fastapi 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.models import *  # 모든 모델 import
from app.api.endpoints import auth, account, advisory, admin


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # CORS 설정
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app_.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
    app_.include_router(account.router, prefix=settings.API_V1_STR, tags=["account"])
    app_.include_router(advisory.router, prefix=settings.API_V1_STR, tags=["advisory"])
    app_.include_router(admin.router, prefix=settings.API_V1_STR, tags=["admin"])

    return app_


app = create_app()


@app.get("/")
async def root():
    return {
        "message": "Welcome to Balance One API"
    }
