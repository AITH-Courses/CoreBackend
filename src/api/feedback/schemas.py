from pydantic import BaseModel

from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.value_objects import Vote


class FeedbackDTO(BaseModel):
    id: str
    text: str
    is_author: bool
    liked_by_user: bool
    disliked_by_user: bool
    date: str
    reputation: int

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
    text: str


class CreateFeedbackResponse(BaseModel):
    feedback_id: str
