from src.domain.base_exceptions import DomainError


class CourseRunNotFoundError(DomainError):

    """Course run is not found."""

    @property
    def message(self) -> str:
        return "Запуск курса не найден"


class CourseRunAlreadyExistsError(DomainError):

    """Course run is already exists."""

    @property
    def message(self) -> str:
        return "Запуск курса уже существует"


class NoActualCourseRunError(DomainError):

    """Course run doesnt exist."""

    @property
    def message(self) -> str:
        return "Для курса еще не создан актуальный запуск"
