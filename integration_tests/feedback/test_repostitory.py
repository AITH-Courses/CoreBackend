import datetime
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.exceptions import FeedbackNotFoundError
from src.domain.feedback.value_objects import FeedbackText, Rating
from src.infrastructure.sqlalchemy.feedback.repository import SQLAlchemyFeedbackRepository


async def create_feedback(async_session: AsyncSession) -> tuple[str, str, str, SQLAlchemyFeedbackRepository]:
    repo = SQLAlchemyFeedbackRepository(async_session)
    feedback_id = str(uuid.uuid4())
    course_id = str(uuid.uuid4())
    author_id = str(uuid.uuid4())
    await repo.create(FeedbackEntity(
        id=feedback_id,
        course_id=course_id,
        author_id=author_id,
        text=FeedbackText("Cool"),
        rating=Rating(5)
    ))
    await async_session.commit()
    return feedback_id, course_id, author_id, repo


async def test_create_feedback(test_async_session: AsyncSession):
    feedback_id, course_id, author_id, repo = await create_feedback(test_async_session)
    feedback = await repo.get_one_by_id(feedback_id)
    assert feedback.id == feedback_id
    assert feedback.course_id == course_id
    assert feedback.author_id == author_id
    assert len(feedback.votes) == 0
    assert feedback.date == datetime.date.today()


async def test_get_many_feedbacks(test_async_session: AsyncSession):
    feedback_1_id, course_id, author_id, repo = await create_feedback(test_async_session)
    feedback_2_id = str(uuid.uuid4())
    await repo.create(FeedbackEntity(
        id=feedback_2_id,
        course_id=course_id,
        author_id=author_id,
        text=FeedbackText("Cool 2"),
        rating=Rating(5),
        date=datetime.date.today() + datetime.timedelta(days=1)
    ))
    await test_async_session.commit()
    feedbacks = await repo.get_all_by_course_id(course_id)
    assert len(feedbacks) == 2
    assert feedbacks[0].id == feedback_2_id
    assert feedbacks[1].id == feedback_1_id


async def test_add_votes(test_async_session: AsyncSession):
    feedback_id, _, _, repo = await create_feedback(test_async_session)
    feedback = await repo.get_one_by_id(feedback_id)
    feedback.vote(str(uuid.uuid4()), "like")
    feedback.vote(str(uuid.uuid4()), "dislike")
    await repo.update_votes(feedback)
    await test_async_session.commit()

    updated_feedback = await repo.get_one_by_id(feedback_id)
    assert updated_feedback.id == feedback_id
    assert len(updated_feedback.votes) == 2
    assert updated_feedback.reputation == 0


async def test_delete_feedback(test_async_session: AsyncSession):
    feedback_id, _, _, repo = await create_feedback(test_async_session)
    await repo.delete(feedback_id)
    await test_async_session.commit()
    with pytest.raises(FeedbackNotFoundError):
        await repo.get_one_by_id(feedback_id)
