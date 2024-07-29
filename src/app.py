from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.admin.course_router import router as admin_course_router
from src.api.auth.router import router as auth_router
from src.api.courses.router import router as course_router
from src.api.feedback.router import router as feedback_router
from src.api.health_check import router as health_check_router
from src.config import app_config
from src.exceptions import ApplicationError
from src.infrastructure.fastapi.docs import add_custom_docs_endpoints


def add_exception_handler(application: FastAPI) -> None:
    """Add exception handlers into FastAPI-application.

    :param application:
    :return:
    """

    @application.exception_handler(ApplicationError)
    async def unicorn_exception_handler(_: Request, exc: ApplicationError) -> JSONResponse:
        """Handle application error.

        :param _:
        :param exc:
        :return: JSONResponse
        """
        return JSONResponse(
            status_code=exc.status,
            content={"message": exc.message},
        )


def add_routers(application: FastAPI) -> None:
    """Add routers into FastAPI-application.

    :param application:
    :return: nothing
    """
    application.include_router(router=health_check_router)
    application.include_router(router=auth_router)
    application.include_router(router=course_router)
    application.include_router(router=feedback_router)
    application.include_router(router=admin_course_router)


def add_cors(application: FastAPI) -> None:
    """Add routers into FastAPI-application.

    :param application:
    :return: nothing
    """
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_application() -> FastAPI:
    """Create FastAPI-application.

    :return: FastAPI
    """
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
    if app_config.is_debug:
        add_cors(application)
    return application


app = create_application()
