from src.domain.base_exceptions import DomainError


class PlaylistNotFoundError(DomainError):

    """Video playlist is not found."""

    @property
    def message(self) -> str:
        return "Плейлист не существует"
