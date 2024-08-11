import datetime
import uuid

import pytest

from src.domain.base_value_objects import UUID
from src.domain.timetable.entities import DayRuleEntity, WeekRuleEntity, TimetableEntity
from src.domain.timetable.value_objects import Weekday


def test_day_rule_lessons():
    year, month, day = 2024, 12, 1
    h1, m1 = 17, 0
    h2, m2 = 18, 30
    rule = DayRuleEntity(
        id=UUID(str(uuid.uuid4())),
        start_time=datetime.time(h1, m1),
        end_time=datetime.time(h2, m2),
        date=datetime.date(year, month, day),
    )
    rule_lessons = rule.lessons
    assert len(rule_lessons) == 1
    assert rule_lessons[0].start_time == datetime.datetime(year, month, day, h1, m1)
    assert rule_lessons[0].end_time == datetime.datetime(year, month, day, h2, m2)


def test_week_rule_lessons_no_weekdays():
    year, month, d1, d2 = 2024, 12, 1, 10
    h1, m1, s = 17, 0, 0
    h2, m2, s = 18, 30, 0
    rule = WeekRuleEntity(
        id=UUID(str(uuid.uuid4())),
        start_time=datetime.time(h1, m1, s),
        end_time=datetime.time(h2, m2, s),
        start_period_date=datetime.date(year, month, d1),
        end_period_date=datetime.date(year, month, d2),
        weekdays=[]
    )
    rule_lessons = rule.lessons
    assert len(rule_lessons) == 0


def test_week_rule_lessons_one_weekday():
    year, month, d1, d2 = 2024, 12, 1, 10
    h1, m1, s = 17, 0, 0
    h2, m2, s = 18, 30, 0
    rule = WeekRuleEntity(
        id=UUID(str(uuid.uuid4())),
        start_time=datetime.time(h1, m1, s),
        end_time=datetime.time(h2, m2, s),
        start_period_date=datetime.date(year, month, d1),
        end_period_date=datetime.date(year, month, d2),
        weekdays=[Weekday("пн")]
    )
    rule_lessons = rule.lessons
    assert len(rule_lessons) == 2
    assert rule_lessons[0].start_time == datetime.datetime(2024, 12, 2, h1, m1, s)
    assert rule_lessons[0].end_time == datetime.datetime(2024, 12, 2, h2, m2, s)
    assert rule_lessons[1].start_time == datetime.datetime(2024, 12, 9, h1, m1, s)
    assert rule_lessons[1].end_time == datetime.datetime(2024, 12, 9, h2, m2, s)


def test_week_rule_lessons_two_weekdays():
    year, month, d1, d2 = 2024, 12, 1, 10
    h1, m1, s = 17, 0, 0
    h2, m2, s = 18, 30, 0
    rule = WeekRuleEntity(
        id=UUID(str(uuid.uuid4())),
        start_time=datetime.time(h1, m1, s),
        end_time=datetime.time(h2, m2, s),
        start_period_date=datetime.date(year, month, d1),
        end_period_date=datetime.date(year, month, d2),
        weekdays=[Weekday("пн"), Weekday("ср")]
    )
    rule_lessons = rule.lessons
    assert len(rule_lessons) == 3
    assert rule_lessons[0].start_time.time() == datetime.time(h1, m1, s)
    assert rule_lessons[0].end_time.time() == datetime.time(h2, m2, s)


def test_timetable_no_warnings():
    year, month, day = 2024, 12, 1
    h1, m1 = 17, 0
    h2, m2 = 18, 30
    rule = DayRuleEntity(
        id=UUID(str(uuid.uuid4())),
        start_time=datetime.time(h1, m1),
        end_time=datetime.time(h2, m2),
        date=datetime.date(year, month, day),
    )
    timetable = TimetableEntity(
        id=UUID(str(uuid.uuid4())),
        course_run_id=UUID(str(uuid.uuid4())),
        rules=[rule]
    )
    assert len(timetable.rules) == 1
    assert len(timetable.lessons) == 1
    assert len(timetable.warnings) == 0


def test_timetable_with_warnings():
    year, month, day = 2024, 12, 1
    h1, m1 = 17, 0
    h2, m2 = 18, 30
    rule = DayRuleEntity(
        id=UUID(str(uuid.uuid4())),
        start_time=datetime.time(h1, m1),
        end_time=datetime.time(h2, m2),
        date=datetime.date(year, month, day),
    )
    timetable = TimetableEntity(
        id=UUID(str(uuid.uuid4())),
        course_run_id=UUID(str(uuid.uuid4())),
        rules=[rule, rule]
    )
    assert len(timetable.rules) == 2
    assert len(timetable.lessons) == 2
    assert len(timetable.warnings) == 1
