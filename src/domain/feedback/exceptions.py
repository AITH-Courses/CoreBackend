from dataclasses import dataclass

from src.domain.base_exceptions import DomainError


@dataclass
class FeedbackLikeError(DomainError):

    """Error with estimating feedback of course."""

    error_message: str

    @property
    def message(self) -> str:
        return self.error_message
