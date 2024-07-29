from __future__ import annotations

import datetime
import json
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING

from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.value_objects import FeedbackText, Vote
from src.infrastructure.redis.feedback.constants import TIME_TO_LIVE_FEEDBACKS
from src.services.feedback.feedback_cache_service import FeedbackCacheService

if TYPE_CHECKING:
    from redis.asyncio import Redis


class RedisFeedbackCacheService(FeedbackCacheService):

    """Redis implementation class for cache of course as service."""

    def __init__(self, session: Redis) -> None:
        self.session = session

    @staticmethod
    def feedback_key(course_id: str) -> str:
        return "course_" + course_id + "_feedbacks"

    @staticmethod
    def __from_domain_to_dict(feedback: FeedbackEntity) -> dict:
        return {
            "id": feedback.id,
            "course_id": feedback.course_id,
            "author_id": feedback.author_id,
            "text": feedback.text.value,
            "votes": [{"user_id": vote.user_id, "vote_type": vote.vote_type} for vote in feedback.votes],
            "date": feedback.date.strftime("%Y-%m-%d"),
        }

    @staticmethod
    def __from_dict_to_domain(feedback_: dict) -> FeedbackEntity:
        return FeedbackEntity(
            id=feedback_["id"],
            course_id=feedback_["course_id"],
            author_id=feedback_["author_id"],
            text=FeedbackText(feedback_["text"]),
            votes={Vote(vote["user_id"], vote["vote_type"]) for vote in feedback_["votes"]},
            date=datetime.date.fromisoformat(feedback_["date"]),
        )

    async def get_many_by_course_id(self, course_id: str) -> list[FeedbackEntity]:
        try:
            feedbacks_key = self.feedback_key(course_id)
            feedbacks_data_string = await self.session.get(feedbacks_key)
            feedbacks_data = json.loads(feedbacks_data_string)
            return [self.__from_dict_to_domain(feedback) for feedback in feedbacks_data]
        except (TypeError, JSONDecodeError):  # no such key in Redis
            return []

    async def delete_many(self, course_id: str) -> None:
        feedbacks_key = self.feedback_key(course_id)
        await self.session.delete(feedbacks_key)

    async def set_many(self, course_id: str, feedbacks: list[FeedbackEntity]) -> None:
        feedbacks_key = self.feedback_key(course_id)
        feedbacks_data = [self.__from_domain_to_dict(feedback) for feedback in feedbacks]
        course_data_string = json.dumps(feedbacks_data)
        await self.session.setex(feedbacks_key, TIME_TO_LIVE_FEEDBACKS, course_data_string)
