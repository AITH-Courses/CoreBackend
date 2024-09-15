from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from src.domain.group_google_calendar.entities import GroupGoogleCalendarEntity

if TYPE_CHECKING:
    from src.domain.timetable.entities import TimetableEntity


class LessonDTO(BaseModel):
    """Schema for lesson."""

    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date


class GroupGoogleCalendarDTO(BaseModel):
    """Schema for group google calendar."""

    id: str
    name: str
    link: str

    @staticmethod
    def from_domain(group: GroupGoogleCalendarEntity) -> GroupGoogleCalendarDTO:
        return GroupGoogleCalendarDTO(
            id=group.id.value,
            name=group.name,
            link=group.link.value,
        )


class TimetableDTO(BaseModel):
    """Schema for timetable."""

    lessons: list[LessonDTO]
    course_run_name: str
    group_google_calendars: list[GroupGoogleCalendarDTO]

    @staticmethod
    def from_domain(
            timetable: TimetableEntity, course_run_name: str, google_calendar_groups: list[GroupGoogleCalendarEntity]
    ) -> TimetableDTO:
        current_lessons = timetable.lessons
        return TimetableDTO(
            lessons=[
                LessonDTO(
                    start_time=lesson.start_time.time(),
                    end_time=lesson.end_time.time(),
                    date=lesson.start_time.date(),
                ) for lesson in current_lessons],
            course_run_name=course_run_name,
            group_google_calendars=[GroupGoogleCalendarDTO.from_domain(g) for g in google_calendar_groups]
        )
