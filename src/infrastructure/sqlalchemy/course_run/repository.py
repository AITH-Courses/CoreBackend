from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.domain.course_run.course_run_repository import ICourseRunRepository
from src.domain.course_run.exceptions import CourseRunNotFoundError
from src.infrastructure.sqlalchemy.course_run.models import CourseRun

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID
    from src.domain.course_run.entities import CourseRunEntity


class SQLAlchemyCourseRunRepository(ICourseRunRepository):

    """SQLAlchemy's implementation of Repository for Course."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, course_run: CourseRunEntity) -> None:
        course_run_ = CourseRun.from_domain(course_run)
        self.session.add(course_run_)

    async def delete(self, course_run_id: UUID) -> None:
        course_run_ = await self.__get_by_id(course_run_id)
        course_run_.is_archive = True
        # to avoid unique error after creating new course run
        course_run_.name = f"{course_run_.name} - {course_run_.id}"

    async def get_by_id(self, course_run_id: UUID) -> CourseRunEntity:
        course_run = await self.__get_by_id(course_run_id)
        return course_run.to_domain()

    async def __get_by_id(self, course_run_id: UUID) -> CourseRun:
        query = (
            select(CourseRun)
            .filter_by(id=course_run_id.value, is_archive=False)
        )
        try:
            result = await self.session.execute(query)
            return result.unique().scalars().one()
        except NoResultFound as ex:
            raise CourseRunNotFoundError from ex

    async def get_all_by_course_id(self, course_id: UUID) -> list[CourseRunEntity]:
        query = (
            select(CourseRun)
            .filter_by(course_id=course_id.value, is_archive=False)
            .order_by(CourseRun.created_at.desc())
        )
        result = await self.session.execute(query)
        course_runs = result.unique().scalars().all()
        return [course_run.to_domain() for course_run in course_runs]
