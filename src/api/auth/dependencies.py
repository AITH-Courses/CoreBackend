from fastapi import Header, Depends, HTTPException, status
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
    unit_of_work = SQLAlchemyAuthUnitOfWork(db_session)
    session_service = RedisSessionService(cache_session)
    command_service = AuthCommandService(unit_of_work, session_service)
    return command_service


def get_auth_token(authentication: str = Header(default="Bearer token")) -> str:
    _, auth_token = authentication.split()  # skip "bearer" part
    return auth_token


async def get_user(
    auth_token: str = Depends(get_auth_token),
    auth_service: AuthCommandService = Depends(get_auth_service),
) -> UserDTO:
    try:
        user = await auth_service.me(auth_token)
        return UserDTO(id=user.id, firstname=user.firstname.value, lastname=user.lastname.value, email=user.email.value)
    except UserBySessionNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(message="You need to login to your account").model_dump(),
        )
