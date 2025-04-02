# fastapi 
from fastapi import FastAPI

from app.core.modules import init_routers, make_middleware
# import
from app.core.settings import config


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Balance One App API",
        description="잔고(Balance)를 중심으로 자문을 제공하는 시스템 API 문서입니다.",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        # dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    # init_listeners(app_=app_)
    # init_cache()
    return app_


app = create_app()
