from __future__ import annotations

import datetime
import uuid

from sqlalchemy import Date, ForeignKey, Integer, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.base_value_objects import UUID
from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.value_objects import FeedbackText, Rating, Vote
from src.infrastructure.sqlalchemy.session import Base


class Feedback(Base):

    """SQLAlchemy model of Feedback."""

    __tablename__ = "feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    course_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, server_default="5", nullable=False)
    votes: Mapped[list[VoteForFeedback]] = relationship(back_populates="feedback")
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    is_archive: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(feedback: FeedbackEntity) -> Feedback:
        return Feedback(
            id=uuid.UUID(feedback.id.value),
            course_id=uuid.UUID(feedback.course_id.value),
            author_id=uuid.UUID(feedback.author_id.value),
            content=feedback.text.value,
            rating=feedback.rating.value,
            date=feedback.date,
            votes=[
                VoteForFeedback(
                    feedback_id=uuid.UUID(feedback.id.value),
                    user_id=uuid.UUID(vote.user_id.value),
                    vote_type=vote.vote_type,
                )
                for vote in feedback.votes
            ],
        )

    def to_domain(self) -> FeedbackEntity:
        return FeedbackEntity(
            id=UUID(str(self.id)),
            course_id=UUID(str(self.course_id)),
            author_id=UUID(str(self.author_id)),
            text=FeedbackText(self.content),
            rating=Rating(self.rating),
            votes={Vote(user_id=UUID(str(vote.user_id)), vote_type=vote.vote_type) for vote in self.votes},
            date=self.date,
        )


class VoteForFeedback(Base):

    """SQLAlchemy model of Vote for feedback."""

    __tablename__ = "feedback_votes"

    feedback_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("feedbacks.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    vote_type: Mapped[str] = mapped_column(nullable=False)
    feedback: Mapped[Feedback] = relationship(back_populates="votes")
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )

    @staticmethod
    def from_domain(vote: Vote, feedback_id: UUID) -> VoteForFeedback:
        return VoteForFeedback(
           feedback_id=uuid.UUID(feedback_id.value),
           user_id=uuid.UUID(vote.user_id.value),
           vote_type=vote.vote_type,
        )
