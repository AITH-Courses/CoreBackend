from __future__ import annotations

import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base_value_objects import UUID, LinkValueObject
from src.domain.group_google_calendar.entities import GroupGoogleCalendarEntity
from src.infrastructure.sqlalchemy.session import Base


class GroupGoogleCalendar(Base):

    """SQLAlchemy model of group google calendar."""

    __tablename__ = "group_google_calendars"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    course_run_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(group_calendar: GroupGoogleCalendarEntity) -> GroupGoogleCalendar:
        return GroupGoogleCalendar(
            id=uuid.UUID(group_calendar.id.value),
            course_run_id=uuid.UUID(group_calendar.course_run_id.value),
            name=group_calendar.name,
            link=group_calendar.link.value,
        )

    def to_domain(self) -> GroupGoogleCalendarEntity:
        return GroupGoogleCalendarEntity(
            id=UUID(str(self.id)),
            course_run_id=UUID(str(self.course_run_id)),
            name=self.name,
            link=LinkValueObject(self.link),
        )
