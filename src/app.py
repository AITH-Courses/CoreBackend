from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.config import app_config
from src.exceptions import ApplicationException
from src.infrastructure.fastapi.docs import add_custom_docs_endpoints
from src.api.health_check import router as health_check_router


def add_exception_handler(application: FastAPI) -> None:
    @application.exception_handler(ApplicationException)
    async def unicorn_exception_handler(_: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=exc.status,
            content={"message": exc.message},
        )


def add_routers(application: FastAPI) -> None:
    application.include_router(router=health_check_router)


def create_application() -> FastAPI:
    application = FastAPI(
        title="AITH Courses",
        version="0.0.1",
        docs_url=None,
        redoc_url=None,
    )
    if app_config.is_debug:
        add_custom_docs_endpoints(application)
    add_routers(application)
    add_exception_handler(application)
    return application


app = create_application()
