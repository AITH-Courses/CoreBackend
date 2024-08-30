from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from src.domain.base_value_objects import UUID
from src.domain.favorite_courses.entities import FavoriteCourseEntity
from src.domain.favorite_courses.exceptions import (
    CourseAlreadyExistsInFavoritesError,
    CourseDoesntExistInFavoritesError,
)

if TYPE_CHECKING:
    from src.services.favorite_courses.unit_of_work import FavoriteCoursesUnitOfWork


class FavoriteCoursesCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: FavoriteCoursesUnitOfWork) -> None:
        self.uow = uow

    async def add_course_to_favorites(self, user_id: str, course_id: str) -> None:
        favorite_course_id = UUID(str(uuid.uuid4()))
        user_id = UUID(user_id)
        course_id = UUID(course_id)
        favorite_course = FavoriteCourseEntity(favorite_course_id, user_id, course_id)
        try:
            await self.uow.favorites_repo.add_one(favorite_course)
            await self.uow.commit()
        except IntegrityError as ex:
            await self.uow.rollback()
            raise CourseAlreadyExistsInFavoritesError from ex
        except Exception:
            await self.uow.rollback()
            raise

    async def remove_course_from_favorites(self, favorite_course_id: str) -> None:
        favorite_course_id = UUID(favorite_course_id)
        try:
            await self.uow.favorites_repo.delete_one(favorite_course_id)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def course_in_favorites(self, course_id: str, user_id: str) -> bool:
        course_id = UUID(course_id)
        user_id = UUID(user_id)
        try:
            await self.uow.favorites_repo.get_one_by_course_id_and_user_id(course_id, user_id)
        except CourseDoesntExistInFavoritesError:
            return False
        else:
            return True

    async def get_favorite_courses(self, user_id: str) -> list[FavoriteCourseEntity]:
        user_id = UUID(user_id)
        return await self.uow.favorites_repo.get_all_by_user_id(user_id)
