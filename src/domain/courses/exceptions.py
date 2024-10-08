from dataclasses import dataclass

from src.domain.base_exceptions import DomainError


@dataclass
class ValueDoesntExistError(DomainError):

    """Value of property does not exist."""

    property_name: str

    @property
    def message(self) -> str:
        return f"Такой {self.property_name} не существует"


@dataclass
class EmptyPropertyError(DomainError):

    """Property is empty."""

    property_name: str

    @property
    def message(self) -> str:
        return f"{self.property_name.capitalize()} is empty"


class IncorrectCourseRunNameError(DomainError):

    """Course run has incorrect name."""

    @property
    def message(self) -> str:
        return "Course run has incorrect name"


@dataclass
class CoursePublishError(DomainError):

    """Course run has incorrect name."""

    error_message: str

    @property
    def message(self) -> str:
        return self.error_message


class CourseNotFoundError(DomainError):

    """Course is not found."""

    @property
    def message(self) -> str:
        return "Course is not found"


class CourseAlreadyExistsError(DomainError):

    """Course with this name already exists."""

    @property
    def message(self) -> str:
        return "Course with this name already exists"
