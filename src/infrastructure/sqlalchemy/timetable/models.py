from __future__ import annotations

import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base_value_objects import UUID
from src.domain.timetable.entities import DayRuleEntity, WeekRuleEntity
from src.domain.timetable.value_objects import Weekday
from src.infrastructure.sqlalchemy.session import Base


class TimetableRule(Base):

    """SQLAlchemy model of Rule."""

    __tablename__ = "timetable_rules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    rule_type: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(nullable=False)
    start_period_date: Mapped[datetime.date] = mapped_column(nullable=False)
    end_period_date: Mapped[datetime.date] = mapped_column(nullable=False)
    weekdays: Mapped[str] = mapped_column(nullable=True)

    course_run_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(rule: DayRuleEntity | WeekRuleEntity) -> TimetableRule:
        if isinstance(rule, DayRuleEntity):
            return TimetableRule(
                id=rule.id.value,
                course_run_id=rule.timetable_id.value,
                rule_type="day",
                start_time=rule.start_time,
                end_time=rule.end_time,
                start_period_date=rule.date,
                end_period_date=rule.date,
                weekdays="",
            )
        return TimetableRule(
            id=rule.id.value,
            course_run_id=rule.timetable_id.value,
            rule_type="week",
            start_time=rule.start_time,
            end_time=rule.end_time,
            start_period_date=rule.start_period_date,
            end_period_date=rule.end_period_date,
            weekdays=",".join([weekday.value for weekday in rule.weekdays]),
        )

    def to_domain(self) -> DayRuleEntity | WeekRuleEntity:
        if self.rule_type == "day":
            return DayRuleEntity(
                id=UUID(str(self.id)),
                timetable_id=UUID(str(self.course_run_id)),
                start_time=self.start_time,
                end_time=self.end_time,
                date=self.start_period_date,
            )
        return WeekRuleEntity(
            id=UUID(str(self.id)),
            timetable_id=UUID(str(self.course_run_id)),
            start_time=self.start_time,
            end_time=self.end_time,
            start_period_date=self.start_period_date,
            end_period_date=self.end_period_date,
            weekdays=[Weekday(weekday) for weekday in self.weekdays.split(",") if weekday != ""],
        )
