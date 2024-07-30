from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.exceptions import FeedbackBelongsToAnotherUserError, FeedbackNotFoundError
from src.domain.feedback.value_objects import FeedbackText, Rating

if TYPE_CHECKING:
    from src.services.feedback.unit_of_work import FeedbackUnitOfWork


class FeedbackCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: FeedbackUnitOfWork) -> None:
        self.uow = uow

    async def create_feedback(self, course_id: str, author_id: str, text_: str, rating_: int) -> str:
        feedback_id = str(uuid.uuid4())
        text = FeedbackText(text_)
        rating = Rating(rating_)
        feedback = FeedbackEntity(feedback_id, course_id, author_id, text, rating)
        try:
            await self.uow.feedback_repo.create(feedback)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise
        return feedback_id

    async def vote(self, feedback_id: str, user_id: str, vote_type: str) -> None:
        try:
            feedback = await self.uow.feedback_repo.get_one_by_id(feedback_id)
            feedback.vote(user_id, vote_type)
            await self.uow.feedback_repo.update_votes(feedback)
            await self.uow.commit()
        except FeedbackNotFoundError:
            await self.uow.rollback()
            raise

    async def unvote(self, feedback_id: str, user_id: str) -> None:
        try:
            feedback = await self.uow.feedback_repo.get_one_by_id(feedback_id)
            feedback.unvote(user_id)
            await self.uow.feedback_repo.update_votes(feedback)
            await self.uow.commit()
        except FeedbackNotFoundError:
            await self.uow.rollback()
            raise

    async def delete_feedback(self, feedback_id: str, user_id: str) -> None:
        try:
            feedback = await self.uow.feedback_repo.get_one_by_id(feedback_id)
            if feedback.author_id != user_id:
                raise FeedbackBelongsToAnotherUserError
            await self.uow.feedback_repo.delete(feedback_id)
            await self.uow.commit()
        except FeedbackNotFoundError:
            await self.uow.rollback()
            raise
