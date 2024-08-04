from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.feedback.entities import FeedbackEntity


class FeedbackCacheService(ABC):

    """Base class for cache of feedback as service."""

    @abstractmethod
    async def get_many_by_course_id(self, course_id: UUID) -> list[FeedbackEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self, course_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_many(self, course_id: UUID, feedbacks: list[FeedbackEntity]) -> None:
        raise NotImplementedError
