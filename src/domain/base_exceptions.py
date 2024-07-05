from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):

    """Base domain error."""

    @property
    def message(self) -> str:
        return "Error in application"
