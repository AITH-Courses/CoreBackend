import uuid
from dataclasses import dataclass

from src.domain.base_exceptions import IncorrectUUIDError


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
