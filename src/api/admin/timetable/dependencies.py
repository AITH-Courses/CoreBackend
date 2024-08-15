from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.timetable.unit_of_work import SQLAlchemyTimetableUnitOfWork
from src.infrastructure.sqlalchemy.session import get_async_session
from src.services.timetable.command_service import TimetableCommandService


def get_admin_timetable_command_service(
    db_session: AsyncSession = Depends(get_async_session),
) -> TimetableCommandService:
    """Get feedback service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyTimetableUnitOfWork(db_session)
    return TimetableCommandService(unit_of_work)
