from src.domain.base_exceptions import DomainError


class GroupGoogleCalendarNotFoundError(DomainError):

    """Group google calendar is not found."""

    @property
    def message(self) -> str:
        return "Расписание в Google-календаре не существует"
