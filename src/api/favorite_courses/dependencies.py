from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.favorite_courses.unit_of_work import SQLAlchemyFavoritesUnitOfWork
from src.infrastructure.sqlalchemy.session import get_async_session
from src.services.favorite_courses.command_service import FavoriteCoursesCommandService


def get_favorite_courses_command_service(
    db_session: AsyncSession = Depends(get_async_session),
) -> FavoriteCoursesCommandService:
    """Get favorite courses on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyFavoritesUnitOfWork(db_session)
    return FavoriteCoursesCommandService(unit_of_work)
