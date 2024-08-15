from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.course_run.entities import CourseRunEntity


class ICourseRunRepository(ABC):

    """Interface of Repository for Course run."""

    @abstractmethod
    async def create(self, course_run: CourseRunEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, course_run_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, course_run_id: UUID) -> CourseRunEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_course_id(self, course_id: UUID) -> list[CourseRunEntity]:
        raise NotImplementedError
