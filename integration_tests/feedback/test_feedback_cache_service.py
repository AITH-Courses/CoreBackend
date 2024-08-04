import datetime
import uuid

import pytest

from src.domain.base_value_objects import UUID
from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.value_objects import FeedbackText, Vote, Rating
from src.infrastructure.redis.feedback.feedback_cache_service import RedisFeedbackCacheService


@pytest.fixture(scope='function')
def redis_feedback_cache_service(test_cache_session):
    return RedisFeedbackCacheService(test_cache_session)


async def test_operations_with_one_course(redis_feedback_cache_service):
    feedback_id = UUID(str(uuid.uuid4()))
    course_id = UUID(str(uuid.uuid4()))
    author_id = UUID(str(uuid.uuid4()))
    feedbacks = [FeedbackEntity(
        id=feedback_id,
        course_id=course_id,
        author_id=author_id,
        text=FeedbackText("Cool"),
        rating=Rating(5),
        votes={Vote(UUID(str(uuid.uuid4())), "like")},
        date=datetime.date.today()
    )]
    await redis_feedback_cache_service.set_many(course_id, feedbacks)

    getting_feedbacks = await redis_feedback_cache_service.get_many_by_course_id(course_id)
    assert len(getting_feedbacks) == 1
    assert len(getting_feedbacks[0].votes) == 1
    assert getting_feedbacks[0].text.value == "Cool"
    assert getting_feedbacks[0].rating.value == 5

    await redis_feedback_cache_service.delete_many(course_id)

    deleted_course = await redis_feedback_cache_service.get_many_by_course_id(course_id)
    assert deleted_course is None
