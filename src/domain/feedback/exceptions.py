from dataclasses import dataclass

from src.domain.base_exceptions import DomainError


@dataclass
class FeedbackLikeError(DomainError):

    """Error with estimating feedback of course."""

    error_message: str

    @property
    def message(self) -> str:
        return self.error_message


class FeedbackNotFoundError(DomainError):

    """Feedback is not found."""

    @property
    def message(self) -> str:
        return "Отзыв не найден"


class FeedbackBelongsToAnotherUserError(DomainError):

    """Feedback belongs to another author."""

    @property
    def message(self) -> str:
        return "Для удаления отзыва требуется быть автором"
