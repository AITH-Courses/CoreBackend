import pytest

from src.domain.base_exceptions import InvalidLinkError
from src.domain.base_value_objects import LinkValueObject, EmptyLinkValueObject


def test_correct_link():
    link_string = "https://www.tele-gram.ai"
    link = LinkValueObject(value=link_string)
    assert link.value == link_string


def test_incorrect_link():
    with pytest.raises(InvalidLinkError):
        LinkValueObject(value="www.tele")


def test_correct_empty_link():
    link_string = ""
    link = EmptyLinkValueObject(value=link_string)
    assert link.value == link_string
