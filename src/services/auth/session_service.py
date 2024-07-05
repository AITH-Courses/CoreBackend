from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.auth.entities import UserEntity


class SessionService(ABC):

    """Base class for session as service."""

    @abstractmethod
    async def get(self, auth_token: str) -> UserEntity:
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
