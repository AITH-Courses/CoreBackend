from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.auth.schemas import UserDTO
from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserBySessionNotFoundError
from src.exceptions import ApplicationError
from src.infrastructure.redis.auth.session_service import RedisSessionService
from src.infrastructure.redis.session import get_redis_session
from src.infrastructure.sqlalchemy.session import get_async_session
from src.infrastructure.sqlalchemy.users.unit_of_work import SQLAlchemyAuthUnitOfWork
from src.services.auth.command_service import AuthCommandService

if TYPE_CHECKING:
    from redis.asyncio import Redis
    from sqlalchemy.ext.asyncio import AsyncSession


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


def get_auth_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> str:
    """Get auth token from header.

    :param credentials:
    :return:
    """
    if not credentials:
        raise ApplicationError(
            message="Требуется войти в аккаунт",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return credentials.credentials


async def get_user(
        auth_token: str = Depends(get_auth_token),
        auth_service: AuthCommandService = Depends(get_auth_service),
) -> UserEntity:
    """Get user on auth token.

    :param auth_token:
    :param auth_service:
    :return:
    """
    try:
        user = await auth_service.me(auth_token)
        return user
    except UserBySessionNotFoundError as ex:
        raise ApplicationError(
            message="Требуется перезайти в аккаунт",
            status=status.HTTP_401_UNAUTHORIZED,
        ) from ex


async def get_user_or_anonym(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        auth_service: AuthCommandService = Depends(get_auth_service),
) -> UserEntity | None:
    """Get user on auth token or anonym.

    :param credentials:
    :param auth_service:
    :return:
    """
    anonym = None
    try:
        if not credentials:
            return anonym
        user = await auth_service.me(credentials.credentials)
        return user
    except UserBySessionNotFoundError:
        return anonym
