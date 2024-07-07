from abc import ABC, abstractmethod

from src.domain.courses.entities import CourseEntity


class ICourseRepository(ABC):

    """Interface of Repository for Course."""

    @abstractmethod
    async def create(self, course: CourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, course: CourseEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, course_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, course_id: str) -> CourseEntity:
        raise NotImplementedError
