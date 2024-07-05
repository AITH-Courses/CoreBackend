from fastapi import APIRouter, Depends, HTTPException, status
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
    status_code=status.HTTP_200_OK,
    description="Register talent in system",
    summary="Registration",
    responses={
        status.HTTP_200_OK: {
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
)
async def register_talent(
    data: RegisterRequest,
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> AuthTokenResponse:
    """Register new user.

    :param data:
    :param auth_service:
    :return:
    """
    try:
        auth_token = await auth_service.register_talent(
            data.firstname, data.lastname, data.email, data.password,
        )
    except (EmailNotValidError, EmptyPartOfNameError) as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ErrorResponse(message=ex.message).model_dump(),
        ) from ex
    except PasswordTooShortError as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ErrorResponse(message=ex.message).model_dump(),
        ) from ex
    except UserWithEmailExistsError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(message=ex.message).model_dump(),
        ) from ex
    return AuthTokenResponse(auth_token=auth_token)


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
)
async def login_user(
    data: LoginRequest,
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> AuthTokenResponse:
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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ErrorResponse(message=ex.message).model_dump(),
        ) from ex
    except (WrongPasswordError, UserNotFoundError) as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(message=ex.message).model_dump(),
        ) from ex
    return AuthTokenResponse(auth_token=auth_token)


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
)
async def logout_user(
    auth_token: str = Depends(get_auth_token),
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> SuccessResponse:
    """Logout current user.

    :param auth_token:
    :param auth_service:
    :return:
    """
    await auth_service.logout(auth_token)
    return SuccessResponse(message="Log out is successful")


@router.post(
    "/me",
    status_code=status.HTTP_200_OK,
    description="Logout user in system",
    summary="Log out",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Getting current user is successful",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "No session",
        },
    },
)
async def get_current_user(
    user: UserDTO = Depends(get_user),
) -> UserDTO:
    """Get current user on auth token.

    :param user:
    :return:
    """
    return user
