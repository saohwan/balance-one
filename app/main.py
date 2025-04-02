# fastapi 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, account, advisory, admin

from app.core.modules import init_routers, make_middleware
# import
from app.core.settings import config


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="증권 자문 시스템",
        description="FastAPI 기반의 증권 자문 시스템 API",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        # dependencies=[Depends(Logging)],
        middleware=make_middleware(),
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
    app_.include_router(auth.router, prefix="/api/auth", tags=["인증"])
    app_.include_router(account.router, prefix="/api/account", tags=["계좌"])
    app_.include_router(advisory.router, prefix="/api/advisory", tags=["자문"])
    app_.include_router(admin.router, prefix="/api/admin", tags=["관리자"])

    init_routers(app_=app_)
    # init_listeners(app_=app_)
    # init_cache()
    return app_


app = create_app()

@app.get("/")
async def root():
    return {
        "message": "증권 자문 시스템 API.",
        "version": "1.0.0"
    }
