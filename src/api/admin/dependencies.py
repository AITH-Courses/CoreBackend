from fastapi import Depends, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.dependencies import get_user
from src.api.auth.schemas import UserDTO
from src.exceptions import ApplicationError
from src.infrastructure.redis.courses.course_cache_service import RedisCourseCacheService
from src.infrastructure.redis.session import get_redis_session
from src.infrastructure.sqlalchemy.courses.repository import SQLAlchemyCourseRepository
from src.infrastructure.sqlalchemy.session import get_async_session
from src.services.courses.query_service_for_admin import AdminCourseQueryService


async def get_admin(
    user: UserDTO = Depends(get_user),
) -> UserDTO:
    """Get admin.

    :param user:
    :return:
    """
    if user.role != "admin":
        raise ApplicationError(
            message="Недостаточно прав для совершения операции",
            status=status.HTTP_403_FORBIDDEN,
        )
    return user


def get_admin_courses_query_service(
    db_session: AsyncSession = Depends(get_async_session),
    cache_session: Redis = Depends(get_redis_session),
) -> AdminCourseQueryService:
    """Get courses service on sessions for admin.

    :param db_session:
    :param cache_session:
    :return:
    """
    course_repo = SQLAlchemyCourseRepository(db_session)
    course_cache_service = RedisCourseCacheService(cache_session, "admin")
    return AdminCourseQueryService(course_repo, course_cache_service)
