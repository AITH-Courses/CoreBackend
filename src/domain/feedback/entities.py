import datetime
from dataclasses import dataclass, field

from src.domain.feedback.exceptions import FeedbackLikeError
from src.domain.feedback.value_objects import Vote, FeedbackText


@dataclass
class FeedbackEntity:

    """Entity of feedback."""

    id: str
    course_id: str
    author_id: str
    text: FeedbackText
    votes: set[Vote] = field(default_factory=list)
    date: datetime.date = field(default_factory=datetime.date.today)

    def unvote(self, user_id: str, vote_type: str) -> None:
        vote = Vote(user_id, vote_type)
        self.votes.discard(vote)

    def vote(self, user_id: str, vote_type: str) -> None:
        alternative_vote_type = "dislike" if vote_type == "like" else "like"
        alternative_vote = Vote(user_id, alternative_vote_type)
        vote = Vote(user_id, vote_type)
        if self.author_id == user_id:
            raise FeedbackLikeError(error_message="Невозможно оценивать свой отзыв")
        elif vote in self.votes:
            raise FeedbackLikeError(error_message="Отзыв уже оценен")
        elif alternative_vote in self.votes:
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
