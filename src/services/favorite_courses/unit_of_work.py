from abc import ABC

from src.domain.courses.course_repository import ICourseRepository
from src.domain.favorite_courses.favorite_courses_repository import IFavoriteCourseRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class FavoriteCoursesUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    course_repo: ICourseRepository
    favorites_repo: IFavoriteCourseRepository
