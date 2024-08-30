from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.base_unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.sqlalchemy.courses.repository import SQLAlchemyCourseRepository
from src.infrastructure.sqlalchemy.favorite_courses.repository import SQLAlchemyFavoriteCourseRepository
from src.services.favorite_courses.unit_of_work import FavoriteCoursesUnitOfWork


class SQLAlchemyFavoritesUnitOfWork(SQLAlchemyUnitOfWork, FavoriteCoursesUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        super().__init__(sqla_session)
        self.course_repo = SQLAlchemyCourseRepository(sqla_session)
        self.favorites_repo = SQLAlchemyFavoriteCourseRepository(sqla_session)
