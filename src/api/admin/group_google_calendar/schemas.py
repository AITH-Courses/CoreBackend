from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field


if TYPE_CHECKING:
    from src.domain.group_google_calendar.entities import GroupGoogleCalendarEntity


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


class CreateGroupGoogleCalendarRequest(BaseModel):

    """Schema for creating group google calendar."""

    name: str
    link: str


class UpdateManyGroupGoogleCalendarsRequest(BaseModel):

    """Schema-request for updating many group google calendars."""

    course_run_name: str = Field("Осень 2024")
    courses: list[CourseDTO]


class UpdateManyGroupGoogleCalendarMessage(BaseModel):

    """Schema-response for updating many group google calendars."""

    message: str = Field("OK")


class CourseDTO(BaseModel):
    name: str = Field("A/B тестирование")
    groups: list[CourseGroupDTO]


class CourseGroupDTO(BaseModel):
    name: str = Field("Группа в 17:00")
    link: str = Field("https://calendar.google.com/calendar/...")
