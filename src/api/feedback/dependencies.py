from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.redis.feedback.feedback_cache_service import RedisFeedbackCacheService
from src.infrastructure.redis.session import get_redis_session
from src.infrastructure.sqlalchemy.feedback.repository import SQLAlchemyFeedbackRepository
from src.infrastructure.sqlalchemy.feedback.unit_of_work import SQLAlchemyFeedbackUnitOfWork
from src.infrastructure.sqlalchemy.session import get_async_session
from src.services.feedback.command_service import FeedbackCommandService
from src.services.feedback.query_service import FeedbackQueryService


def get_feedback_query_service(
    db_session: AsyncSession = Depends(get_async_session),
    cache_session: Redis = Depends(get_redis_session),
) -> FeedbackQueryService:
    """Get feedback service on sessions.

    :param db_session:
    :param cache_session:
    :return:
    """
    feedback_repo = SQLAlchemyFeedbackRepository(db_session)
    feedback_cache_service = RedisFeedbackCacheService(cache_session)
    return FeedbackQueryService(feedback_repo, feedback_cache_service)


def get_feedback_command_service(
    db_session: AsyncSession = Depends(get_async_session),
) -> FeedbackCommandService:
    """Get feedback service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyFeedbackUnitOfWork(db_session)
    return FeedbackCommandService(unit_of_work)
