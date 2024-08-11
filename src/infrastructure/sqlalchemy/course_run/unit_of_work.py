from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.course_run.repository import SQLAlchemyCourseRunRepository
from src.services.courses.unit_of_work import CoursesUnitOfWork


class SQLAlchemyCourseRunUnitOfWork(CoursesUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        self.session = sqla_session
        self.course_run_repo = SQLAlchemyCourseRunRepository(sqla_session)

    async def begin(self) -> None:
        await self.session.begin()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
