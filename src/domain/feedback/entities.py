from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.domain.feedback.exceptions import FeedbackLikeError
from src.domain.feedback.value_objects import FeedbackText, Rating, Vote

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID

@dataclass
class FeedbackEntity:

    """Entity of feedback."""

    id: UUID
    course_id: UUID
    author_id: UUID
    text: FeedbackText
    rating: Rating
    votes: set[Vote] = field(default_factory=list)
    date: datetime.date = field(default_factory=datetime.date.today)

    def unvote(self, user_id: UUID) -> None:
        vote = Vote(user_id, "like")
        alternative_vote = Vote(user_id, "dislike")
        self.votes.discard(vote)
        self.votes.discard(alternative_vote)

    def vote(self, user_id: UUID, vote_type: str) -> None:
        alternative_vote_type = "dislike" if vote_type == "like" else "like"
        alternative_vote = Vote(user_id, alternative_vote_type)
        vote = Vote(user_id, vote_type)
        if self.author_id == user_id:
            raise FeedbackLikeError(error_message="Невозможно оценивать свой отзыв")
        if vote in self.votes:
            raise FeedbackLikeError(error_message="Отзыв уже оценен")
        if alternative_vote in self.votes:
            self.votes.remove(alternative_vote)
            self.votes.add(vote)
        else:
            self.votes.add(vote)

    @property
    def reputation(self) -> int:
        reputation = 0
        for vote in self.votes:
            signed_vote = 1 if vote.vote_type == "like" else -1
            reputation += signed_vote
        return reputation
