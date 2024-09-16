from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.base_unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.sqlalchemy.course_run.repository import SQLAlchemyCourseRunRepository
from src.infrastructure.sqlalchemy.courses.repository import SQLAlchemyCourseRepository
from src.infrastructure.sqlalchemy.group_google_calendar.repository import SQLAlchemyGroupGoogleCalendarRepository
from src.services.group_google_calendar.unit_of_work import GroupGoogleCalendarUnitOfWork


class SQLAlchemyGGCUnitOfWork(SQLAlchemyUnitOfWork, GroupGoogleCalendarUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        super().__init__(sqla_session)
        self.ggc_repo = SQLAlchemyGroupGoogleCalendarRepository(sqla_session)
        self.course_repo = SQLAlchemyCourseRepository(sqla_session)
        self.course_run_repo = SQLAlchemyCourseRunRepository(sqla_session)
