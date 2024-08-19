from dataclasses import dataclass

from src.domain.base_exceptions import DomainError


@dataclass
class TimetableError(DomainError):

    """Error with timetable."""

    error_message: str

    @property
    def message(self) -> str:
        return self.error_message


class RuleNotFoundError(DomainError):

    """Rule is not found."""

    @property
    def message(self) -> str:
        return "Правило формирования расписания не найдено"


class IncorrectRuleTypeError(DomainError):

    """Rule type is not valid."""

    @property
    def message(self) -> str:
        return "Некорректный или несоответствующий тип правила"


@dataclass
class NoActualTimetableError(DomainError):

    """Timetable is not available for course."""

    error_message: str

    @property
    def message(self) -> str:
        return self.error_message
