from dataclasses import dataclass

from src.domain.base_exceptions import DomainError


@dataclass
class TimetableError(DomainError):

    """Error with timetable."""

    error_message: str

    @property
    def message(self) -> str:
        return self.error_message


class TimetableNotFoundError(DomainError):

    """Timetable is not found."""

    @property
    def message(self) -> str:
        return "Расписание не найдено"
