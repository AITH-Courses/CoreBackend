from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.feedback.entities import FeedbackEntity


class IFeedbackRepository(ABC):

    """Interface of Repository for Feedback."""

    @abstractmethod
    async def create(self, feedback: FeedbackEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, feedback_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_votes(self, feedback: FeedbackEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_id(self, feedback_id: str) -> FeedbackEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_course_id(self, course_id: str) -> list[FeedbackEntity]:
        raise NotImplementedError
