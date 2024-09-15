from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends

from src.infrastructure.sqlalchemy.session import get_async_session
from src.infrastructure.sqlalchemy.group_google_calendar.unit_of_work import SQLAlchemyGGCUnitOfWork
from src.services.group_google_calendar.command_service import GroupGoogleCalendarCommandService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def get_group_google_calendar_service(
        db_session: AsyncSession = Depends(get_async_session),
) -> GroupGoogleCalendarCommandService:
    """Get group google calendar service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyGGCUnitOfWork(db_session)
    return GroupGoogleCalendarCommandService(unit_of_work)
