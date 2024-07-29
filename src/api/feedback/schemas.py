from pydantic import BaseModel, Field

from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.value_objects import Vote


class FeedbackDTO(BaseModel):

    """Schema of feedback."""

    id: str = Field("c5a4bfb7-0349-4d07-b6d8-b21c8777602b")
    text: str = Field("Cool course!")
    is_author: bool = Field(default=False)
    liked_by_user: bool = Field(default=True)
    disliked_by_user: bool = Field(default=False)
    date: str = Field("2024-09-24")
    reputation: int = Field(3)

    @staticmethod
    def from_domain(feedback: FeedbackEntity, user_id: str) -> "FeedbackDTO":
        return FeedbackDTO(
            id=feedback.id,
            text=feedback.text.value,
            is_author=feedback.author_id == user_id,
            liked_by_user=Vote(user_id, "like") in feedback.votes,
            disliked_by_user=Vote(user_id, "dislike") in feedback.votes,
            date=feedback.date.strftime("%Y-%m-%d"),
            reputation=feedback.reputation,
        )


class CreateFeedbackRequest(BaseModel):

    """Schema of request for creating feedback."""

    text: str = Field("Cool course!")


class CreateFeedbackResponse(BaseModel):

    """Schema of response for creating feedback."""

    feedback_id: str = Field("c5a4bfb7-0349-4d07-b6d8-b21c8777602b")


class VoteDTO(BaseModel):

    """Schema of create/delete vote."""

    vote_type: str = Field("like")
