from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.courses.entities import CourseEntity
    from src.domain.courses.value_objects import CourseName

class ICourseRepository(ABC):

    """Interface of Repository for Course."""

    @abstractmethod
    async def create(self, course: CourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, course: CourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_draft_status(self, course: CourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, course_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, course_id: UUID) -> CourseEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, course_name: CourseName) -> CourseEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[CourseEntity]:
        raise NotImplementedError
