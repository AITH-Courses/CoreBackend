from abc import ABC, abstractmethod

from src.domain.auth.user_repository import IUserRepository
from src.domain.courses.course_repository import ICourseRepository


class CoursesUnitOfWork(ABC):

    """Base class implemented pattern Unit of Work."""

    user_repo: IUserRepository
    course_repo: ICourseRepository

    @abstractmethod
    async def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
