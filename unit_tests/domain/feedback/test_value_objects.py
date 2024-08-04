import uuid

import pytest

from src.domain.base_value_objects import UUID
from src.domain.courses.exceptions import EmptyPropertyError, ValueDoesntExistError
from src.domain.feedback.value_objects import FeedbackText, Vote, Rating


def test_correct_feedback_text():
    feedback_text_string = "Good course!"
    feedback_text = FeedbackText(feedback_text_string)
    assert feedback_text.value == feedback_text_string


def test_incorrect_feedback_text():
    with pytest.raises(EmptyPropertyError):
        FeedbackText("")


def test_correct_feedback_rating():
    feedback_rating_number = 1
    feedback_rating = Rating(feedback_rating_number)
    assert feedback_rating.value == feedback_rating_number


def test_incorrect_feedback_rating():
    with pytest.raises(ValueDoesntExistError):
        Rating(-1)


def test_correct_vote():
    user_id = UUID(str(uuid.uuid4()))
    vote_type_string = "like"
    vote = Vote(user_id, vote_type_string)
    assert vote.vote_type == vote_type_string
    assert vote.user_id == user_id


def test_incorrect_vote():
    with pytest.raises(ValueDoesntExistError):
        Vote(UUID(str(uuid.uuid4())), "unlike")
