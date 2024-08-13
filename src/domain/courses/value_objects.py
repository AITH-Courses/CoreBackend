from dataclasses import dataclass

from src.domain.courses.constants import (
    COURSE_RUN_FROM_YEAR,
    COURSE_RUN_SEASONS,
    COURSE_RUN_TO_YEAR,
    FORMATS,
    IMPLEMENTERS,
    PERIODS,
    ROLES,
    TERMS,
)
from src.domain.courses.exceptions import EmptyPropertyError, IncorrectCourseRunNameError, ValueDoesntExistError


@dataclass(init=False, eq=True, frozen=True)
class CourseName:

    """Name of course as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value == "":
            raise EmptyPropertyError(property_name="course")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Author:

    """Author information as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value == "":
            raise EmptyPropertyError(property_name="author")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Implementer:

    """Implementer represents an implementer as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in IMPLEMENTERS:
            raise ValueDoesntExistError(property_name="implementer")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Format:

    """Format represents an format as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in FORMATS:
            raise ValueDoesntExistError(property_name="format")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Terms:

    """Term numbers as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in TERMS:
            raise ValueDoesntExistError(property_name="terms")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Role:

    """Role name as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in ROLES:
            raise ValueDoesntExistError(property_name="role")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Period:

    """Period name as a value object: september, november and other."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in PERIODS:
            raise ValueDoesntExistError(property_name="period")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class CourseRun:

    """Run of course as a value object: Autumn 2023."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        try:
            season, year_string = value.split()
            if season not in COURSE_RUN_SEASONS:
                raise IncorrectCourseRunNameError
            year = int(year_string)
            if year < COURSE_RUN_FROM_YEAR or year > COURSE_RUN_TO_YEAR:
                raise IncorrectCourseRunNameError
        except ValueError as ex:
            raise IncorrectCourseRunNameError from ex
        object.__setattr__(self, "value", value)

    @property
    def year(self):
        return int(self.value.split(" ")[1])

    @property
    def season(self):
        return self.value.split(" ")[0]


@dataclass(init=True, eq=True, frozen=True)
class Resource:

    """Resource of course as a value object."""

    title: str
    link: str
