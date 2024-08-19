from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.domain.timetable.entities import DayRuleEntity, TimetableEntity, WeekRuleEntity
from src.domain.timetable.exceptions import IncorrectRuleTypeError, RuleNotFoundError
from src.domain.timetable.timetable_repository import ITimetableRepository
from src.infrastructure.sqlalchemy.timetable.models import TimetableRule

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID


class SQLAlchemyTimetableRepository(ITimetableRepository):

    """SQLAlchemy's implementation of Repository for Timetable."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, course_run_id: UUID) -> TimetableEntity:
        query = (
            select(TimetableRule)
            .filter_by(course_run_id=course_run_id.value)
        )
        result = await self.session.execute(query)
        timetable_rules = result.scalars().all()
        return TimetableEntity(
            id=course_run_id,
            course_run_id=course_run_id,
            rules=[rule.to_domain() for rule in timetable_rules],
        )

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
