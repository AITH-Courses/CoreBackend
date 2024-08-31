from src.domain.base_exceptions import DomainError


class TalentProfileNotFoundError(DomainError):

    """Talent profile is not found."""

    @property
    def message(self) -> str:
        return "Профиль таланта не существует"


class TalentProfileAlreadyExistsError(DomainError):

    """Talent profile already exists."""

    @property
    def message(self) -> str:
        return "Профиль таланта уже существует"


class TalentProfileForOnlyTalentError(DomainError):

    """Talent profile is only for talent."""

    @property
    def message(self) -> str:
        return "Профиль таланта можно создать только для таланта"
