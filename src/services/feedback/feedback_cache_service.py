from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.feedback.entities import FeedbackEntity


class FeedbackCacheService(ABC):

    """Base class for cache of feedback as service."""

    @abstractmethod
    async def get_many_by_course_id(self, course_id: str) -> list[FeedbackEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self, course_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_many(self, course_id: str, feedbacks: list[FeedbackEntity]) -> None:
        raise NotImplementedError
