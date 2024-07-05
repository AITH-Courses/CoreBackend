from src.domain.auth.constants import PASSWORD_MIN_LENGTH
from src.domain.base_exceptions import DomainError


class EmailNotValidError(DomainError):

    """Email is not valid."""

    @property
    def message(self) -> str:
        return "Email is not valid"


class RoleDoesntExistError(DomainError):

    """Role does not exist."""

    @property
    def message(self) -> str:
        return "Role does not exist"


class EmptyPartOfNameError(DomainError):

    """Part of name is empty."""

    @property
    def message(self) -> str:
        return "Part of name is empty"


class UserWithEmailExistsError(DomainError):

    """User with this email already exists."""

    @property
    def message(self) -> str:
        return "User with this email already exists"


class UserNotFoundError(DomainError):

    """User is not found."""

    @property
    def message(self) -> str:
        return "User is not found"


class PasswordTooShortError(DomainError):

    """Password length must be greater than or equal to <> characters."""

    @property
    def message(self) -> str:
        return f"Password length must be greater than or equal to {PASSWORD_MIN_LENGTH} characters"


class WrongPasswordError(DomainError):

    """It is a wrong password."""

    @property
    def message(self) -> str:
        return "It is a wrong password"


class UserBySessionNotFoundError(DomainError):

    """User is not found by session."""

    @property
    def message(self) -> str:
        return "User is not found by session"
