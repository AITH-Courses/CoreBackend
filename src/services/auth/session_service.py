from abc import ABC, abstractmethod
from typing import Optional

from src.domain.auth.entities import UserEntity


class SessionService(ABC):
    @abstractmethod
    async def get(self, auth_token: str) -> Optional[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, auth_token: str, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, auth_token: str, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, auth_token: str) -> None:
        raise NotImplementedError
