from src.domain.base_exceptions import DomainError


class CourseAlreadyExistsInFavoritesError(DomainError):

    """Course is already exists in favorites."""

    @property
    def message(self) -> str:
        return "Курс уже добавлен в избранное"


class CourseDoesntExistInFavoritesError(DomainError):

    """Course doesnt exist in favorites."""

    @property
    def message(self) -> str:
        return "Курс не добавлен в избранное"
