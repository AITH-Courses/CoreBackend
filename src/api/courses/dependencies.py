from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.redis.courses.course_cache_service import RedisCourseCacheService
from src.infrastructure.redis.session import get_redis_session
from src.infrastructure.sqlalchemy.courses.repository import SQLAlchemyCourseRepository
from src.infrastructure.sqlalchemy.session import get_async_session
from src.infrastructure.sqlalchemy.courses.unit_of_work import SQLAlchemyCoursesUnitOfWork
from src.services.courses.command_service import CourseCommandService
from src.services.courses.query_service_for_talent import TalentCourseQueryService


def get_talent_courses_query_service(
    db_session: AsyncSession = Depends(get_async_session),
    cache_session: Redis = Depends(get_redis_session),
) -> TalentCourseQueryService:
    """Get courses service on sessions for talent.

    :param db_session:
    :param cache_session:
    :return:
    """
    course_repo = SQLAlchemyCourseRepository(db_session)
    course_cache_service = RedisCourseCacheService(cache_session)
    return TalentCourseQueryService(course_repo, course_cache_service)


def get_courses_command_service(
    db_session: AsyncSession = Depends(get_async_session),
) -> CourseCommandService:
    """Get courses service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyCoursesUnitOfWork(db_session)
    return CourseCommandService(unit_of_work)
