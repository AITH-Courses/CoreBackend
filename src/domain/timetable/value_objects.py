import datetime
from dataclasses import dataclass

from src.domain.courses.exceptions import ValueDoesntExistError
from src.domain.timetable.constants import WEEKDAYS


@dataclass(init=True, eq=True, frozen=True)
class LessonTimeDuration:

    """Lesson time duration as value object."""

    start_time: datetime.datetime
    end_time: datetime.datetime


@dataclass(init=False, eq=True, frozen=True)
class Weekday:

    """Weekday as a value object: пн, вт and other."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in WEEKDAYS:
            raise ValueDoesntExistError(property_name="weekday")
        object.__setattr__(self, "value", value)


@dataclass(init=True, eq=True, frozen=True)
class TimetableWarning:

    """Timetable warning as a value object."""

    day: datetime.date
    message: str
