from pydantic import BaseModel, Field

from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.value_objects import Vote


class FeedbackDTO(BaseModel):
    id: str = Field("c5a4bfb7-0349-4d07-b6d8-b21c8777602b")
    text: str = Field("Cool course!")
    is_author: bool = Field(False)
    liked_by_user: bool = Field(True)
    disliked_by_user: bool = Field(False)
    date: str = Field("2024-09-24")
    reputation: int = Field(3)

    @staticmethod
    def from_domain(feedback: FeedbackEntity, user_id: str):
        return FeedbackDTO(
            id=feedback.id,
            text=feedback.text.value,
            is_author=feedback.author_id == user_id,
            liked_by_user=Vote(user_id, "like") in feedback.votes,
            disliked_by_user=Vote(user_id, "dislike") in feedback.votes,
            date=feedback.date.strftime("%Y-%m-%d"),
            reputation=feedback.reputation
        )


class CreateFeedbackDTO(BaseModel):
    text: str = Field("Cool course!")


class CreateFeedbackResponse(BaseModel):
    feedback_id: str = Field("c5a4bfb7-0349-4d07-b6d8-b21c8777602b")


class VoteDTO(BaseModel):
    vote_type: str = Field("like")
