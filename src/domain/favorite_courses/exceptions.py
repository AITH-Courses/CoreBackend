from src.domain.base_exceptions import DomainError


class CourseAlreadyExistsInFavoritesError(DomainError):

    """Course is already exists in favorites."""

    @property
    def message(self) -> str:
        return "Курс уже добавлен в избранное"
