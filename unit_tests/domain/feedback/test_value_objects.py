import pytest

from src.domain.courses.exceptions import EmptyPropertyError, ValueDoesntExistError
from src.domain.feedback.value_objects import FeedbackText, Vote


def test_correct_feedback_text():
    feedback_text_string = "Good course!"
    feedback_text = FeedbackText(feedback_text_string)
    assert feedback_text.value == feedback_text_string


def test_incorrect_feedback_text():
    with pytest.raises(EmptyPropertyError):
        FeedbackText("")


def test_correct_vote():
    user_id_string = "32424151"
    vote_type_string = "like"
    vote = Vote(user_id_string, vote_type_string)
    assert vote.vote_type == vote_type_string
    assert vote.user_id == user_id_string


def test_incorrect_vote():
    with pytest.raises(ValueDoesntExistError):
        Vote("324234", "unlike")
