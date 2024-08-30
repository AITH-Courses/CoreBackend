from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.domain.favorite_courses.exceptions import CourseDoesntExistInFavoritesError
from src.domain.favorite_courses.favorite_courses_repository import IFavoriteCourseRepository
from src.infrastructure.sqlalchemy.favorite_courses.models import FavoriteCourse

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID
    from src.domain.favorite_courses.entities import FavoriteCourseEntity


class SQLAlchemyFavoriteCourseRepository(IFavoriteCourseRepository):

    """SQLAlchemy's implementation of Repository for Course."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, favorite_course: FavoriteCourseEntity) -> None:
        course_ = FavoriteCourse.from_domain(favorite_course)
        self.session.add(course_)

    async def delete_one(self, favorite_course_id: UUID) -> None:
        favorite_course_ = await self.__get_by_id(favorite_course_id)
        await self.session.delete(favorite_course_)

    async def __get_by_id(self, favorite_course_id: UUID) -> FavoriteCourse:
        query = (
            select(FavoriteCourse)
            .filter_by(id=favorite_course_id.value)
        )
        try:
            result = await self.session.execute(query)
            return result.scalars().one()
        except NoResultFound as ex:
            raise CourseDoesntExistInFavoritesError from ex

    async def get_all_by_user_id(self, user_id: UUID) -> list[FavoriteCourseEntity]:
        query = (
            select(FavoriteCourse)
            .filter_by(user_id=user_id.value)
        )
        result = await self.session.execute(query)
        favorite_courses = result.unique().scalars().all()
        return [course.to_domain() for course in favorite_courses]

    async def get_one_by_course_id_and_user_id(self, course_id: UUID, user_id: UUID) -> FavoriteCourseEntity:
        query = (
            select(FavoriteCourse)
            .filter_by(course_id=course_id.value, user_id=user_id.value)
        )
        try:
            result = await self.session.execute(query)
            favorite_course = result.scalars().one()
            return favorite_course.to_domain()
        except NoResultFound as ex:
            raise CourseDoesntExistInFavoritesError from ex
