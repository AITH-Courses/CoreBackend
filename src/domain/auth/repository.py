from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.auth.entities import UserEntity
from src.domain.auth.value_objects import Email


class UserRepository(ABC):

    """Interface of Repository for User."""

    @abstractmethod
    async def create(self, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> UserEntity:
        raise NotImplementedError
