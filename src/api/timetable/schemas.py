from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.domain.timetable.entities import TimetableEntity


class LessonDTO(BaseModel):

    """Schema for lesson."""

    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date


class TimetableDTO(BaseModel):

    """Schema for timetable."""

    lessons: list[LessonDTO]
    course_run_name: str

    @staticmethod
    def from_domain(timetable: TimetableEntity, course_run_name: str) -> TimetableDTO:
        current_lessons = timetable.lessons
        return TimetableDTO(
            lessons=[
                LessonDTO(
                    start_time=lesson.start_time.time(),
                    end_time=lesson.end_time.time(),
                    date=lesson.start_time.date(),
                ) for lesson in current_lessons],
            course_run_name=course_run_name,
        )
