from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.feedback.entities import FeedbackEntity
    from src.domain.feedback.feedback_repository import IFeedbackRepository
    from src.services.feedback.feedback_cache_service import FeedbackCacheService


class FeedbackQueryService:

    """Class implemented CQRS pattern, query class."""

    def __init__(self, feedback_repo: IFeedbackRepository, feedback_cache_service: FeedbackCacheService) -> None:
        self.feedback_repo = feedback_repo
        self.feedback_cache_service = feedback_cache_service

    async def get_feedbacks_by_course_id(self, course_id: str) -> list[FeedbackEntity]:
        feedbacks_from_cache = await self.feedback_cache_service.get_many_by_course_id(course_id)
        if feedbacks_from_cache:
            return feedbacks_from_cache
        feedbacks = await self.feedback_repo.get_all_by_course_id(course_id)
        await self.feedback_cache_service.set_many(course_id, feedbacks)
        return feedbacks
