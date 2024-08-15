from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING

from src.domain.base_value_objects import UUID
from src.domain.timetable.entities import TimetableEntity, DayRuleEntity, WeekRuleEntity
from src.domain.timetable.value_objects import Weekday

if TYPE_CHECKING:
    from src.services.timetable.unit_of_work import TimetableUnitOfWork


class TimetableCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: TimetableUnitOfWork) -> None:
        self.uow = uow

    async def get_timetable_by_course_run_id(self, course_run_id: str) -> TimetableEntity:
        course_run_id = UUID(course_run_id)
        return await self.uow.timetable_repo.get_by_id(course_run_id)

    async def create_day_rule(self, timetable_id: str, start_time: datetime.time, end_time: datetime.time, date: datetime.date) -> str:
        rule_id = UUID(str(uuid.uuid4()))
        timetable_id = UUID(timetable_id)
        rule = DayRuleEntity(rule_id, timetable_id, start_time, end_time, date)
        try:
            await self.uow.timetable_repo.create_rule(rule)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise
        return rule_id.value

    async def create_week_rule(self, timetable_id: str, start_time: datetime.time, end_time: datetime.time, start_period_date: datetime.date, end_period_date: datetime.date, weekdays: list[str]) -> str:
        rule_id = UUID(str(uuid.uuid4()))
        timetable_id = UUID(timetable_id)
        weekdays = [Weekday(wd) for wd in weekdays]
        rule = WeekRuleEntity(rule_id, timetable_id, start_time, end_time, start_period_date, end_period_date, weekdays)
        try:
            await self.uow.timetable_repo.create_rule(rule)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise
        return rule_id.value

    async def update_day_rule(self, rule_id: str, timetable_id: str, start_time: datetime.time, end_time: datetime.time, date: datetime.date) -> None:
        rule_id = UUID(rule_id)
        timetable_id = UUID(timetable_id)
        rule = DayRuleEntity(rule_id, timetable_id, start_time, end_time, date)
        try:
            await self.uow.timetable_repo.update_rule(rule)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def update_week_rule(self, rule_id: str, timetable_id: str, start_time: datetime.time, end_time: datetime.time, start_period_date: datetime.date, end_period_date: datetime.date, weekdays: list[str]) -> None:
        rule_id = UUID(rule_id)
        timetable_id = UUID(timetable_id)
        weekdays = [Weekday(wd) for wd in weekdays]
        rule = WeekRuleEntity(rule_id, timetable_id, start_time, end_time, start_period_date, end_period_date, weekdays)
        try:
            await self.uow.timetable_repo.update_rule(rule)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def delete_rule(self, rule_id: str) -> None:
        rule_id = UUID(rule_id)
        try:
            await self.uow.timetable_repo.delete_rule(rule_id)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise
