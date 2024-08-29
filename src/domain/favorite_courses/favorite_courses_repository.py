from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.favorite_courses.entities import FavoriteCourseEntity


class IFavoriteCourseRepository(ABC):

    """Interface of Repository for favorite course."""

    @abstractmethod
    async def add_one(self, favorite_course: FavoriteCourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, favorite_course_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user_id(self, user_id: UUID) -> list[FavoriteCourseEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_course_id_and_user_id(self, course_id: UUID, user_id: UUID) -> FavoriteCourseEntity:
        raise NotImplementedError
