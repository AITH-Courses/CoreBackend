from dataclasses import dataclass

from src.domain.auth.constants import EMAIL_PATTERN, USER_ROLES
from src.domain.auth.exceptions import EmailNotValidError, EmptyPartOfNameError, RoleDoesntExistError


@dataclass(init=False, eq=True, frozen=True)
class Email:

    """Email represents an email as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if EMAIL_PATTERN.match(value) is None:
            raise EmailNotValidError
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class UserRole:

    """UserRole represents a role of user as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in USER_ROLES:
            raise RoleDoesntExistError
        object.__setattr__(self, "value", value)


@dataclass(init=False, eq=True, frozen=True)
class PartOfName:

    """PartOfName represents a part of name as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value == "":
            raise EmptyPartOfNameError
        object.__setattr__(self, "value", value)
