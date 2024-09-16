from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.group_google_calendar.entities import GroupGoogleCalendarEntity


class IGroupGoogleCalendarRepository(ABC):

    """Interface of Repository for Feedback."""

    @abstractmethod
    async def create(self, group_google_calendar: GroupGoogleCalendarEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, group_google_calendar_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_course_run_id(self, course_run_id: UUID) -> list[GroupGoogleCalendarEntity]:
        raise NotImplementedError
