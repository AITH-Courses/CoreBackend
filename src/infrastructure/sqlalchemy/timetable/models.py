from __future__ import annotations

import datetime
import uuid

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.base_value_objects import UUID
from src.domain.timetable.entities import DayRuleEntity, WeekRuleEntity, TimetableEntity
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

    timetable_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("course_run_timetables.id"), primary_key=True)
    timetable: Mapped[Timetable] = relationship(back_populates="rules")

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
                timetable_id=rule.timetable_id.value,
                rule_type="day",
                start_time=rule.start_time,
                end_time=rule.end_time,
                start_period_date=rule.date,
                end_period_date=rule.date,
                weekdays=""
            )
        return TimetableRule(
            id=rule.id.value,
            timetable_id=rule.timetable_id.value,
            rule_type="week",
            start_time=rule.start_time,
            end_time=rule.end_time,
            start_period_date=rule.start_period_date,
            end_period_date=rule.end_period_date,
            weekdays=",".join([weekday.value for weekday in rule.weekdays])
        )

    def to_domain(self) -> DayRuleEntity | WeekRuleEntity:
        if self.rule_type == "day":
            return DayRuleEntity(
                id=UUID(str(self.id)),
                timetable_id=UUID(str(self.timetable_id)),
                start_time=self.start_time,
                end_time=self.end_time,
                date=self.start_period_date
            )
        return WeekRuleEntity(
            id=UUID(str(self.id)),
            timetable_id=UUID(str(self.timetable_id)),
            start_time=self.start_time,
            end_time=self.end_time,
            start_period_date=self.start_period_date,
            end_period_date=self.end_period_date,
            weekdays=[Weekday(weekday) for weekday in self.weekdays.split(",")],
        )


class Timetable(Base):

    """SQLAlchemy model of Timetable."""

    __tablename__ = "course_run_timetables"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    course_run_id: Mapped[uuid.UUID] = mapped_column(unique=True, nullable=False)
    is_archive: Mapped[bool] = mapped_column(nullable=False, default=False)

    rules: Mapped[list[TimetableRule]] = relationship(back_populates="timetable")

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(timetable: TimetableEntity) -> Timetable:
        return Timetable(
            id=timetable.id.value,
            course_run_id=timetable.course_run_id.value,
            rules=[TimetableRule.from_domain(rule) for rule in timetable.rules]
        )

    def to_domain(self) -> TimetableEntity:
        return TimetableEntity(
            id=UUID(str(self.id)),
            course_run_id=UUID(str(self.course_run_id)),
            rules=[rule.to_domain() for rule in self.rules]
        )
