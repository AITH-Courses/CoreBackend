from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from src.domain.base_value_objects import UUID
from src.domain.feedback.value_objects import Vote

if TYPE_CHECKING:
    from src.domain.feedback.entities import FeedbackEntity

class FeedbackDTO(BaseModel):

    """Schema of feedback."""

    id: str = Field("c5a4bfb7-0349-4d07-b6d8-b21c8777602b")
    text: str = Field("Cool course!")
    rating: int = Field(5)
    is_author: bool = Field(default=False)
    liked_by_user: bool = Field(default=True)
    disliked_by_user: bool = Field(default=False)
    date: str = Field("2024-09-24")
    reputation: int = Field(3)

    @staticmethod
    def from_domain(feedback: FeedbackEntity, user_id: str | None) -> FeedbackDTO:
        return FeedbackDTO(
            id=feedback.id.value,
            text=feedback.text.value,
            rating=feedback.rating.value,
            is_author=False if user_id is None else feedback.author_id == user_id,
            liked_by_user=False if user_id is None else Vote(UUID(user_id), "like") in feedback.votes,
            disliked_by_user=False if user_id is None else Vote(UUID(user_id), "dislike") in feedback.votes,
            date=feedback.date.strftime("%Y-%m-%d"),
            reputation=feedback.reputation,
        )


class CreateFeedbackRequest(BaseModel):

    """Schema of request for creating feedback."""

    text: str = Field("Cool course!")
    rating: int = Field(5)


class CreateFeedbackResponse(BaseModel):

    """Schema of response for creating feedback."""

    feedback_id: str = Field("c5a4bfb7-0349-4d07-b6d8-b21c8777602b")


class VoteDTO(BaseModel):

    """Schema of create/delete vote."""

    vote_type: str = Field("like")
