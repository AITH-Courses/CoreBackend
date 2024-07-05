from fastapi import Depends, Header, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas import ErrorResponse, UserDTO
from src.domain.auth.exceptions import UserBySessionNotFoundError
from src.infrastructure.redis.auth.session_service import RedisSessionService
from src.infrastructure.redis.session import get_redis_session
from src.infrastructure.sqlalchemy.session import get_async_session
from src.infrastructure.sqlalchemy.users.unit_of_work import SQLAlchemyAuthUnitOfWork
from src.services.auth.command_service import AuthCommandService


def get_auth_service(
    db_session: AsyncSession = Depends(get_async_session),
    cache_session: Redis = Depends(get_redis_session),
) -> AuthCommandService:
    """Get auth service on sessions.

    :param db_session:
    :param cache_session:
    :return:
    """
    unit_of_work = SQLAlchemyAuthUnitOfWork(db_session)
    session_service = RedisSessionService(cache_session)
    return AuthCommandService(unit_of_work, session_service)


def get_auth_token(authentication: str = Header(default="Bearer token")) -> str:
    """Get auth token from header.

    :param authentication:
    :return:
    """
    _, auth_token = authentication.split()  # skip "bearer" part
    return auth_token


async def get_user(
    auth_token: str = Depends(get_auth_token),
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> UserDTO:
    """Get user on auth token.

    :param auth_token:
    :param auth_service:
    :return:
    """
    try:
        user = await auth_service.me(auth_token)
        return UserDTO(id=user.id, firstname=user.firstname.value, lastname=user.lastname.value, email=user.email.value)
    except UserBySessionNotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(message="You need to login to your account").model_dump(),
        ) from ex
