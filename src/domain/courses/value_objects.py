from dataclasses import dataclass

from src.domain.courses.exceptions import EmptyPropertyError, ValueDoesntExistError, IncorrectCourseRunNameError
from src.domain.courses.constants import IMPLEMENTERS, FORMATS, TERMS, ROLES, PERIODS


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
            raise ValueDoesntExistError("implementer")
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
            raise ValueDoesntExistError("format")
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
            raise ValueDoesntExistError("terms")
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
            raise ValueDoesntExistError("role")
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
            raise ValueDoesntExistError("period")
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
            if season not in ("Осень", "Весна"):
                raise IncorrectCourseRunNameError
            year = int(year_string)
            if year < 2020:
                raise IncorrectCourseRunNameError
        except ValueError as ex:
            raise IncorrectCourseRunNameError from ex
        object.__setattr__(self, "value", value)
