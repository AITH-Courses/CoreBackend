from __future__ import annotations

import datetime
from typing import Literal

from pydantic import BaseModel

from src.domain.timetable.entities import DayRuleEntity, TimetableEntity, WeekRuleEntity


class DayRuleDTO(BaseModel):

    """Schema for day rule."""

    id: str
    timetable_id: str
    type: str
    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date

    @staticmethod
    def from_domain(rule: DayRuleEntity) -> DayRuleDTO:
        return DayRuleDTO(
            id=rule.id.value,
            timetable_id=rule.timetable_id.value,
            type="day",
            start_time=rule.start_time,
            end_time=rule.end_time,
            date=rule.date,
        )


class CreateOrUpdateRuleDayDTO(BaseModel):

    """Schema for create or update day rule."""

    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date


class WeekRuleDTO(BaseModel):

    """Schema for week rule."""

    id: str
    timetable_id: str
    type: str
    start_time: datetime.time
    end_time: datetime.time
    start_period_date: datetime.date
    end_period_date: datetime.date
    weekdays: list[str]

    @staticmethod
    def from_domain(rule: WeekRuleEntity) -> WeekRuleDTO:
        return WeekRuleDTO(
            id=rule.id.value,
            timetable_id=rule.timetable_id.value,
            type="week",
            start_time=rule.start_time,
            end_time=rule.end_time,
            start_period_date=rule.start_period_date,
            end_period_date=rule.end_period_date,
            weekdays=[w.value for w in rule.weekdays],
        )


class CreateOrUpdateWeekRuleDTO(BaseModel):

    """Schema for create or update week rule."""

    start_time: datetime.time
    end_time: datetime.time
    start_period_date: datetime.date
    end_period_date: datetime.date
    weekdays: list[str]


class CreateRuleResponse(BaseModel):

    """Schema of create rule response."""

    rule_id: str


class CreateOrUpdateRuleRequest(BaseModel):

    """Schema of create or update rule request."""

    type: Literal["day", "week"]
    rule: CreateOrUpdateRuleDayDTO | CreateOrUpdateWeekRuleDTO


class LessonDTO(BaseModel):

    """Schema of lesson."""

    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date
    warning_messages: list[str]


class TimetableDTO(BaseModel):

    """Schema of timetable."""

    id: str
    rules: list[DayRuleDTO | WeekRuleDTO]
    lessons: list[LessonDTO]

    @staticmethod
    def from_domain(timetable: TimetableEntity) -> TimetableDTO:
        current_lessons = timetable.lessons
        warnings = timetable.warnings
        return TimetableDTO(
            id=timetable.id.value,
            lessons=[
                LessonDTO(
                    start_time=lesson.start_time.time(),
                    end_time=lesson.end_time.time(),
                    date=lesson.start_time.date(),
                    warning_messages=[w.message for w in warnings if w.day == lesson.start_time.date()],
                ) for lesson in current_lessons
            ],
            rules=[
                (WeekRuleDTO.from_domain(rule) if isinstance(rule, WeekRuleEntity) else DayRuleDTO.from_domain(rule))
                for rule in timetable.rules
            ],
        )
