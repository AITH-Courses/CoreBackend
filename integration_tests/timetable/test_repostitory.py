import datetime
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.base_value_objects import UUID
from src.domain.course_run.exceptions import CourseRunNotFoundError
from src.domain.courses.value_objects import CourseRun
from src.domain.timetable.entities import TimetableEntity, DayRuleEntity, WeekRuleEntity
from src.domain.timetable.exceptions import RuleNotFoundError
from src.domain.timetable.value_objects import Weekday
from src.infrastructure.sqlalchemy.timetable.repository import SQLAlchemyTimetableRepository


async def test_create_day_rule(test_async_session: AsyncSession):
    repo = SQLAlchemyTimetableRepository(test_async_session)
    year, month, day = 2024, 12, 1
    h1, m1, h2, m2 = 17, 0, 18, 30
    course_run_id = UUID(str(uuid.uuid4()))
    rule = DayRuleEntity(
        id=UUID(str(uuid.uuid4())),
        timetable_id=course_run_id,
        start_time=datetime.time(h1, m1),
        end_time=datetime.time(h2, m2),
        date=datetime.date(year, month, day),
    )
    await repo.create_rule(rule)
    await test_async_session.commit()
    timetable = await repo.get_by_id(course_run_id)
    assert len(timetable.rules) == 1
    assert timetable.rules[0] == rule


async def test_update_day_rule(test_async_session: AsyncSession):
    repo = SQLAlchemyTimetableRepository(test_async_session)
    course_run_id = UUID(str(uuid.uuid4()))
    year, month, day = 2024, 12, 1
    h1, m1, h2, m2 = 17, 0, 18, 30
    rule_id = UUID(str(uuid.uuid4()))
    rule = DayRuleEntity(
        id=rule_id,
        timetable_id=course_run_id,
        start_time=datetime.time(h1, m1),
        end_time=datetime.time(h2, m2),
        date=datetime.date(year, month, day),
    )
    await repo.create_rule(rule)
    await test_async_session.commit()
    new_day, new_h1, new_m2 = 2, 16, 40
    await repo.update_rule(
        DayRuleEntity(
            id=rule_id,
            timetable_id=course_run_id,
            start_time=datetime.time(new_h1, m1),
            end_time=datetime.time(h2, new_m2),
            date=datetime.date(year, month, new_day),
        )
    )
    await test_async_session.commit()
    timetable = await repo.get_by_id(course_run_id)
    assert len(timetable.rules) == 1
    assert timetable.rules[0].date == datetime.date(year, month, new_day)
    assert timetable.rules[0].start_time == datetime.time(new_h1, m1)
    assert timetable.rules[0].end_time == datetime.time(h2, new_m2)


async def test_create_week_rule(test_async_session: AsyncSession):
    repo = SQLAlchemyTimetableRepository(test_async_session)
    course_run_id = UUID(str(uuid.uuid4()))
    year, month, day = 2024, 12, 1
    h1, m1, h2, m2 = 17, 0, 18, 30
    rule = WeekRuleEntity(
        id=UUID(str(uuid.uuid4())),
        timetable_id=course_run_id,
        start_time=datetime.time(h1, m1, 0),
        end_time=datetime.time(h2, m2, 0),
        start_period_date=datetime.date(year, month, day),
        end_period_date=datetime.date(year, month, day),
        weekdays=[Weekday("пн")]
    )
    await repo.create_rule(rule)
    await test_async_session.commit()
    timetable = await repo.get_by_id(course_run_id)
    assert len(timetable.rules) == 1
    assert timetable.rules[0] == rule


async def test_delete_rule(test_async_session: AsyncSession):
    repo = SQLAlchemyTimetableRepository(test_async_session)
    course_run_id = UUID(str(uuid.uuid4()))
    year, month, day = 2024, 12, 1
    h1, m1, h2, m2 = 17, 0, 18, 30
    rule_id = UUID(str(uuid.uuid4()))
    rule = DayRuleEntity(
        id=rule_id,
        timetable_id=course_run_id,
        start_time=datetime.time(h1, m1),
        end_time=datetime.time(h2, m2),
        date=datetime.date(year, month, day),
    )
    await repo.create_rule(rule)
    await test_async_session.commit()
    await repo.delete_rule(rule_id)
    await test_async_session.commit()
    with pytest.raises(RuleNotFoundError):
        await repo.delete_rule(rule_id)
