from dataclasses import dataclass

from src.domain.courses.exceptions import EmptyPropertyError, ValueDoesntExistError
from src.domain.feedback.contants import MAX_RATING_VALUE, MIN_RATING_VALUE, VOTE_TYPES


@dataclass(init=False, eq=True, frozen=True)
class Vote:

    """Name of course as a value object."""

    user_id: str
    vote_type: str

    def __init__(self, user_id: str, vote_type: str) -> None:
        """Initialize object."""
        if vote_type not in VOTE_TYPES:
            raise ValueDoesntExistError(property_name="vote type")
        object.__setattr__(self, "user_id", user_id)
        object.__setattr__(self, "vote_type", vote_type)


@dataclass(init=False, eq=True, frozen=True)
class FeedbackText:

    """Content of feedback as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value == "":
            raise EmptyPropertyError(property_name="text")
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class Rating:

    """Rating of course in feedback as a value object."""

    value: int

    def __init__(self, value: int) -> None:
        """Initialize object.

        :param value:
        """
        if value < MIN_RATING_VALUE or value > MAX_RATING_VALUE:
            raise ValueDoesntExistError(property_name="rating")
        object.__setattr__(self, "value", value)
