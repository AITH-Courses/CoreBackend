from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.talent_profile.entities import TalentProfileEntity


class ITalentProfileRepository(ABC):

    """Interface of Repository for Course."""

    @abstractmethod
    async def create(self, profile: TalentProfileEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, profile: TalentProfileEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> TalentProfileEntity:
        raise NotImplementedError
