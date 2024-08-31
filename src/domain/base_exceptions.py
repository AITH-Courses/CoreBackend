from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):

    """Base domain error."""

    @property
    def message(self) -> str:
        return "Error in application"


class IncorrectUUIDError(DomainError):

    """Error with incorrect identifier."""

    @property
    def message(self) -> str:
        return "Identifier is not valid"


class InvalidLinkError(DomainError):

    """Error with invalid link."""

    @property
    def message(self) -> str:
        return "Link is not valid"
