from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.domain.timetable.entities import DayRuleEntity, TimetableEntity, WeekRuleEntity
from src.domain.timetable.exceptions import IncorrectRuleTypeError, RuleNotFoundError, TimetableNotFoundError
from src.domain.timetable.timetable_repository import ITimetableRepository
from src.infrastructure.sqlalchemy.timetable.models import Timetable, TimetableRule

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID


class SQLAlchemyTimetableRepository(ITimetableRepository):

    """SQLAlchemy's implementation of Repository for Timetable."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, timetable: TimetableEntity) -> None:
        timetable_ = Timetable.from_domain(timetable)
        self.session.add(timetable_)

    async def get_by_id(self, course_run_id: UUID) -> TimetableEntity:
        query = (
            select(Timetable)
            .options(joinedload(Timetable.rules))
            .filter_by(course_run_id=course_run_id.value, is_archive=False)
        )
        try:
            result = await self.session.execute(query)
            timetable_ = result.unique().scalars().one()
            return timetable_.to_domain()
        except NoResultFound as ex:
            raise TimetableNotFoundError from ex

    async def create_rule(self, rule: DayRuleEntity | WeekRuleEntity) -> None:
        rule_ = TimetableRule.from_domain(rule)
        self.session.add(rule_)

    async def update_rule(self, rule: DayRuleEntity | WeekRuleEntity) -> None:
        rule_ = await self.__get_by_rule_id(rule.id)
        rule_.start_time = rule.start_time
        rule_.end_time = rule.end_time
        if isinstance(rule, DayRuleEntity) and rule_.rule_type == "day":
            rule_.start_period_date = rule.date
            rule_.end_period_date = rule.date
            rule_.weekdays = ""
        elif isinstance(rule, WeekRuleEntity) and rule_.rule_type == "week":
            rule_.start_period_date = rule.start_period_date
            rule_.end_period_date = rule.end_period_date
            rule_.weekdays = ",".join([weekday.value for weekday in rule.weekdays])
        else:
            raise IncorrectRuleTypeError

    async def delete_rule(self, rule_id: UUID) -> None:
        rule_ = await self.__get_by_rule_id(rule_id)
        await self.session.delete(rule_)

    async def __get_by_rule_id(self, rule_id: UUID) -> TimetableRule:
        query = (
            select(TimetableRule)
            .filter_by(id=rule_id.value)
        )
        try:
            result = await self.session.execute(query)
            return result.unique().scalars().one()
        except NoResultFound as ex:
            raise RuleNotFoundError from ex
