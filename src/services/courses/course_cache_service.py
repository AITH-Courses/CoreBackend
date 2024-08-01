from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.courses.entities import CourseEntity


class CourseCacheService(ABC):

    """Base class for cache of course as service."""

    @abstractmethod
    async def get_one(self, course_id: str) -> CourseEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, course_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_one(self, course: CourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self) -> list[CourseEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_many(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_many(self, courses: list[CourseEntity]) -> None:
        raise NotImplementedError
