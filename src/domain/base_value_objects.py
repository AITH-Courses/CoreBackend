import re
import uuid
from dataclasses import dataclass

from src.domain.base_exceptions import IncorrectUUIDError, InvalidLinkError


@dataclass(init=False, eq=True, frozen=True)
class UUID:

    """Id for entities as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        try:
            uuid.UUID(value)
            object.__setattr__(self, "value", value)
        except ValueError as ex:
            raise IncorrectUUIDError from ex


@dataclass(init=False, eq=True, frozen=True)
class LinkValueObject:

    """Link as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        pattern = r"^https?://[^\s]+"
        if re.match(pattern, value):
            object.__setattr__(self, "value", value)
        else:
            raise InvalidLinkError


@dataclass(init=False, eq=True, frozen=True)
class EmptyLinkValueObject:

    """Link or Empty string as a value object."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        pattern = r"^https?://[^\s]+"
        if value == "" or re.match(pattern, value):
            object.__setattr__(self, "value", value)
        else:
            raise InvalidLinkError
