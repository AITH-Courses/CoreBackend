from dataclasses import dataclass


@dataclass
class CreateGroupGoogleCalendarDTO:
    course_run_id: str
    name: str
    link: str


@dataclass(frozen=True)
class UpdateGroupDTO:
    name: str
    link: str


@dataclass
class UpdateGroupGoogleCalendarDTO:
    course_name: str
    groups: list[UpdateGroupDTO]
