from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.domain.feedback.exceptions import FeedbackNotFoundError
from src.domain.feedback.feedback_repository import IFeedbackRepository
from src.infrastructure.sqlalchemy.feedback.models import Feedback, VoteForFeedback

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.feedback.entities import FeedbackEntity


class SQLAlchemyFeedbackRepository(IFeedbackRepository):

    """SQLAlchemy's implementation of Repository for Course."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, feedback: FeedbackEntity) -> None:
        feedback_ = Feedback.from_domain(feedback)
        self.session.add(feedback_)

    async def update_votes(self, feedback: FeedbackEntity) -> None:
        feedback_ = await self.__get_by_id(feedback.id)
        for vote in feedback_.votes:
            await self.session.delete(vote)
        for vote in feedback.votes:
            self.session.add(VoteForFeedback.from_domain(vote, feedback.id))

    async def delete(self, feedback_id: str) -> None:
        feedback_ = await self.__get_by_id(feedback_id)
        feedback_.is_archive = True  # to avoid cascade deleting

    async def get_one_by_id(self, feedback_id: str) -> FeedbackEntity:
        feedback_ = await self.__get_by_id(feedback_id)
        return feedback_.to_domain()

    async def __get_by_id(self, feedback_id: str) -> Feedback:
        query = (
            select(Feedback)
            .options(joinedload(Feedback.votes))
            .filter_by(id=feedback_id, is_archive=False)
        )
        try:
            result = await self.session.execute(query)
            return result.unique().scalars().one()
        except NoResultFound as ex:
            raise FeedbackNotFoundError from ex

    async def get_all_by_course_id(self, course_id: str) -> list[FeedbackEntity]:
        query = (
            select(Feedback)
            .options(joinedload(Feedback.votes))
            .filter_by(course_id=course_id, is_archive=False)
            .order_by(Feedback.date.desc())
        )
        result = await self.session.execute(query)
        feedbacks = result.unique().scalars().all()
        return [feedback.to_domain() for feedback in feedbacks]
