from abc import ABC, abstractmethod

from src.domain.auth.user_repository import UserRepository


class AuthUnitOfWork(ABC):
    user_repo: UserRepository

    @abstractmethod
    async def begin(self):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
