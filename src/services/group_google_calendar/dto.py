from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CreateGroupGoogleCalendarDTO:

    """DTO to create one group."""

    course_run_id: str
    name: str
    link: str


@dataclass(frozen=True)
class UpdateGroupDTO:

    """DTO to update one group."""

    name: str
    link: str


@dataclass
class UpdateGroupGoogleCalendarDTO:

    """DTO to update many groups."""

    course_name: str
    groups: list[UpdateGroupDTO]
