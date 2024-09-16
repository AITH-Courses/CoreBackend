from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, select

from src.domain.group_google_calendar.exceptions import GroupGoogleCalendarNotFoundError
from src.domain.group_google_calendar.ggc_repository import IGroupGoogleCalendarRepository
from src.infrastructure.sqlalchemy.group_google_calendar.models import GroupGoogleCalendar

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID
    from src.domain.group_google_calendar.entities import GroupGoogleCalendarEntity


class SQLAlchemyGroupGoogleCalendarRepository(IGroupGoogleCalendarRepository):

    """SQLAlchemy's implementation of Repository for group google calendar."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, group_google_calendar: GroupGoogleCalendarEntity) -> None:
        calendar_ = GroupGoogleCalendar.from_domain(group_google_calendar)
        self.session.add(calendar_)

    async def delete(self, group_google_calendar_id: UUID) -> None:
        delete_statement = (
            delete(GroupGoogleCalendar)
            .where(GroupGoogleCalendar.id == group_google_calendar_id.value)
        )
        result = await self.session.execute(delete_statement)
        if result.rowcount == 0:
            raise GroupGoogleCalendarNotFoundError

    async def get_all_by_course_run_id(self, course_run_id: UUID) -> list[GroupGoogleCalendarEntity]:
        query = (
            select(GroupGoogleCalendar)
            .filter_by(course_run_id=course_run_id.value)
            .order_by(GroupGoogleCalendar.created_at.desc())
        )
        result = await self.session.execute(query)
        feedbacks = result.unique().scalars().all()
        return [feedback.to_domain() for feedback in feedbacks]
