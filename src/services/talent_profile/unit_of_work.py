from abc import ABC, abstractmethod

from src.domain.auth.user_repository import IUserRepository
from src.domain.talent_profile.profile_repository import ITalentProfileRepository


class TalentProfileUnitOfWork(ABC):

    """Base class implemented pattern Unit of Work."""

    user_repo: IUserRepository
    profile_repo: ITalentProfileRepository

    @abstractmethod
    async def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
