from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.domain.timetable.exceptions import TimetableError
from src.domain.timetable.constants import WEEKDAYS
from src.domain.timetable.value_objects import Weekday, TimetableWarning
from src.domain.timetable.value_objects import LessonTimeDuration

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID


@dataclass
class DayRuleEntity:

    """Entity of timetable rule for day."""

    id: UUID
    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date

    @property
    def lessons(self) -> list[LessonTimeDuration]:
        year, month, day = self.date.year, self.date.month, self.date.day
        return [LessonTimeDuration(
            datetime.datetime(year, month, day, self.start_time.hour, self.start_time.minute, self.start_time.second),
            datetime.datetime(year, month, day, self.end_time.hour, self.end_time.minute, self.end_time.second),
        )]


@dataclass
class WeekRuleEntity:

    """Entity of timetable rule for week."""

    id: UUID
    start_time: datetime.time
    end_time: datetime.time
    start_period_date: datetime.date
    end_period_date: datetime.date
    weekdays: list[Weekday]

    @property
    def lessons(self) -> list[LessonTimeDuration]:
        current_lessons: list[LessonTimeDuration] = []
        current_date = self.start_period_date
        while current_date <= self.end_period_date:
            weekday = Weekday(WEEKDAYS[current_date.weekday()])
            if weekday not in self.weekdays:
                current_date = current_date + datetime.timedelta(days=1)
                continue
            year, month, day = current_date.year, current_date.month, current_date.day
            lesson = LessonTimeDuration(
                datetime.datetime(year, month, day, self.start_time.hour, self.start_time.minute, self.start_time.second),
                datetime.datetime(year, month, day, self.end_time.hour, self.end_time.minute, self.end_time.second),
            )
            current_lessons.append(lesson)
            current_date = current_date + datetime.timedelta(days=1)
        current_lessons.sort(key=lambda lesson: lesson.start_time)
        return current_lessons


@dataclass
class TimetableEntity:

    """Entity of timetable."""

    id: UUID
    course_run_id: UUID
    rules: list[DayRuleEntity | WeekRuleEntity]

    @property
    def lessons(self) -> list[LessonTimeDuration]:
        current_lessons: list[LessonTimeDuration] = []
        for rule in self.rules:
            current_lessons.extend(rule.lessons)
        current_lessons.sort(key=lambda lesson: lesson.start_time)
        return current_lessons

    @property
    def warnings(self) -> set[TimetableWarning]:
        current_lessons = self.lessons
        current_warnings = set()
        for i in range(len(current_lessons)):
            for j in range(i+1, len(current_lessons)):
                if current_lessons[i].start_time.date() != current_lessons[j].start_time.date():
                    continue
                if current_lessons[i].start_time < current_lessons[j].end_time and current_lessons[j].start_time < current_lessons[i].end_time:
                    warning = TimetableWarning(current_lessons[i].start_time.date(), "Пересечение занятий в этот день")
                    current_warnings.add(warning)
        return current_warnings

    def check_lesson_intersection(self, other: TimetableEntity) -> None:
        lesson_intersection_error = TimetableError("Курсы имеют пересечения по времени проведения занятий")
        other_lessons = set(other.lessons)
        current_lessons = set(self.lessons)
        if current_lessons.intersection(other_lessons):
            raise lesson_intersection_error
        for current_lesson in current_lessons:
            for other_lesson in other_lessons:
                if current_lesson.start_time.date() != other_lesson.start_time.date():
                    continue
                elif current_lesson.start_time < other_lesson.end_time and other_lesson.start_time < current_lesson.end_time:
                    raise lesson_intersection_error
