from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.base_unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.sqlalchemy.course_run.repository import SQLAlchemyCourseRunRepository
from src.infrastructure.sqlalchemy.timetable.repository import SQLAlchemyTimetableRepository
from src.services.course_run.unit_of_work import CourseRunUnitOfWork


class SQLAlchemyCourseRunUnitOfWork(SQLAlchemyUnitOfWork, CourseRunUnitOfWork):
    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        super().__init__(sqla_session)
        self.course_run_repo = SQLAlchemyCourseRunRepository(sqla_session)
        self.timetable_repo = SQLAlchemyTimetableRepository(sqla_session)
