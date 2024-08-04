import datetime
import uuid

import pytest

from src.domain.base_value_objects import UUID
from src.domain.feedback.entities import FeedbackEntity
from src.domain.feedback.exceptions import FeedbackLikeError
from src.domain.feedback.value_objects import FeedbackText, Vote, Rating


@pytest.fixture
def correct_feedback() -> FeedbackEntity:
    feedback_id = UUID(str(uuid.uuid4()))
    course_id = UUID(str(uuid.uuid4()))
    author_id = UUID(str(uuid.uuid4()))
    text = FeedbackText("Cool!")
    rating = Rating(5)
    date = datetime.date(year=2024, month=12, day=1)
    return FeedbackEntity(feedback_id, course_id, author_id, text, rating, set(), date)


def test_correct_feedback(correct_feedback):
    assert correct_feedback.text == FeedbackText("Cool!")
    assert correct_feedback.date == datetime.date(year=2024, month=12, day=1)


def test_no_votes(correct_feedback):
    assert correct_feedback.reputation == 0
    assert len(correct_feedback.votes) == 0


def test_add_votes(correct_feedback):
    user_id, vote_type = UUID(str(uuid.uuid4())), "like"
    correct_feedback.vote(user_id, vote_type)
    assert correct_feedback.reputation == 1
    assert len(correct_feedback.votes) == 1
    alternative_vote_type = "dislike"
    correct_feedback.vote(user_id, alternative_vote_type)
    assert correct_feedback.reputation == -1
    assert len(correct_feedback.votes) == 1


def test_add_votes_many_users(correct_feedback):
    user_1_id, vote_1_type = UUID(str(uuid.uuid4())), "like"
    user_2_id, vote_2_type = UUID(str(uuid.uuid4())), "dislike"
    correct_feedback.vote(user_1_id, vote_1_type)
    correct_feedback.vote(user_2_id, vote_2_type)
    assert correct_feedback.reputation == 0
    assert len(correct_feedback.votes) == 2


def test_add_same_vote_from_one_user(correct_feedback):
    user_id, vote_type = UUID(str(uuid.uuid4())), "like"
    correct_feedback.vote(user_id, vote_type)
    with pytest.raises(FeedbackLikeError):
        correct_feedback.vote(user_id, vote_type)


def test_add_vote_from_author(correct_feedback):
    with pytest.raises(FeedbackLikeError):
        correct_feedback.vote(correct_feedback.author_id, "like")


def test_unvote(correct_feedback):
    user_id, vote_type = UUID(str(uuid.uuid4())), "like"
    correct_feedback.unvote(user_id)
    correct_feedback.vote(user_id, vote_type)
    correct_feedback.unvote(user_id)
