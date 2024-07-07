from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_auth_service, get_auth_token, get_user
from src.api.auth.schemas import (
    AuthTokenResponse,
    ErrorResponse,
    LoginRequest,
    RegisterRequest,
    SuccessResponse,
    UserDTO,
)
from src.domain.auth.exceptions import (
    EmailNotValidError,
    EmptyPartOfNameError,
    PasswordTooShortError,
    UserNotFoundError,
    UserWithEmailExistsError,
    WrongPasswordError,
)
from src.services.auth.command_service import AuthCommandService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    description="Register talent in system",
    summary="Registration",
    responses={
        status.HTTP_201_CREATED: {
            "model": AuthTokenResponse,
            "description": "Registration is successful",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error in registration",
        },
    },
    response_model=AuthTokenResponse,
)
async def register_talent(
    data: RegisterRequest,
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> JSONResponse:
    """Register new user.

    :param data:
    :param auth_service:
    :return:
    """
    try:
        auth_token = await auth_service.register_talent(
            data.firstname, data.lastname, data.email, data.password,
        )
    except (EmailNotValidError, EmptyPartOfNameError, PasswordTooShortError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except UserWithEmailExistsError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content=AuthTokenResponse(auth_token=auth_token).model_dump(),
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Login user in system",
    summary="Log in",
    responses={
        status.HTTP_200_OK: {
            "model": AuthTokenResponse,
            "description": "Log in is successful",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error in login",
        },
    },
    response_model=AuthTokenResponse,
)
async def login_user(
    data: LoginRequest,
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> JSONResponse:
    """Login user.

    :param data:
    :param auth_service:
    :return:
    """
    try:
        auth_token = await auth_service.login(
            data.email, data.password,
        )
    except EmailNotValidError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except (WrongPasswordError, UserNotFoundError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content=AuthTokenResponse(auth_token=auth_token).model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="Logout user in system",
    summary="Log out",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Log out is successful",
        },
    },
    response_model=SuccessResponse,
)
async def logout_user(
    auth_token: str = Depends(get_auth_token),
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> JSONResponse:
    """Logout current user.

    :param auth_token:
    :param auth_service:
    :return:
    """
    await auth_service.logout(auth_token)
    return JSONResponse(
        content=SuccessResponse(message="Log out is successful").model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    description="Get current user",
    summary="Getting user",
    responses={
        status.HTTP_200_OK: {
            "model": UserDTO,
            "description": "Getting current user is successful",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "No session",
        },
    },
    response_model=UserDTO,
)
async def get_current_user(
    user: UserDTO = Depends(get_user),
) -> JSONResponse:
    """Get current user on auth token.

    :param user:
    :return:
    """
    return JSONResponse(
        content=user.model_dump(),
        status_code=status.HTTP_200_OK,
    )
