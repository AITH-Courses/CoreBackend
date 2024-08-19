from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.timetable.entities import DayRuleEntity, TimetableEntity, WeekRuleEntity


class ITimetableRepository(ABC):

    """Interface of Repository for Timetable."""

    @abstractmethod
    async def get_by_id(self, course_run_id: UUID) -> TimetableEntity:
        raise NotImplementedError

    @abstractmethod
    async def create_rule(self, rule: DayRuleEntity | WeekRuleEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_rule(self, rule: DayRuleEntity | WeekRuleEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_rule(self, rule_id: UUID) -> None:
        raise NotImplementedError
