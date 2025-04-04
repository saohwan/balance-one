# fastapi 
from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
# sqlalchemy
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.api.routers.main_router import router
# import
from app.core.database import engine
from app.core.settings import settings
from app.utils.env import SECRET_KEY


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)
    admin = Admin(app_, engine)
    # 필요한 경우 다른 Admin 뷰 추가


origins = [
    "*",
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            SessionMiddleware,
            secret_key=SECRET_KEY
        ),
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # Middleware(SQLAlchemyMiddleware),
    ]
    return middleware

# def init_cache() -> None:
#     Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

# def init_listeners(app_: FastAPI) -> None:
#     @app_.exception_handler(CustomException)
#     async def custom_exception_handler(request: Request, exc: CustomException):
#         return JSONResponse(
#             status_code=exc.code,
#             content={"error_code": exc.error_code, "message": exc.message},
#         )
