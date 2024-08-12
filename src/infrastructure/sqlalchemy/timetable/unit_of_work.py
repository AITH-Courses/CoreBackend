from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.base_unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.sqlalchemy.timetable.repository import SQLAlchemyTimetableRepository
from src.services.timetable.unit_of_work import TimetableUnitOfWork


class SQLAlchemyCourseRunUnitOfWork(SQLAlchemyUnitOfWork, TimetableUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        super().__init__(sqla_session)
        self.timetable_repo = SQLAlchemyTimetableRepository(sqla_session)

    async def begin(self) -> None:
        await self.session.begin()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
