from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from src.domain.courses.course_repository import ICourseRepository
from src.domain.courses.exceptions import CourseNotFoundError
from src.infrastructure.sqlalchemy.courses.models import Course, PeriodForCourse, RoleForCourse, RunForCourse

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.courses.entities import CourseEntity


class SQLAlchemyCourseRepository(ICourseRepository):

    """SQLAlchemy's implementation of Repository for Course."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, course: CourseEntity) -> None:
        course_ = Course.from_domain(course)
        self.session.add(course_)

    async def update(self, course: CourseEntity) -> None:
        course_ = await self.__get_by_id(course.id)
        course_.name = course.name.value
        course_.image_url = course.image_url
        course_.limits = course.limits
        course_.prerequisites = course.prerequisites
        course_.description = course.description
        course_.topics = course.topics
        course_.assessment = course.assessment
        course_.resources = course.resources
        course_.extra = course.extra
        course_.author = course.author.value if course.author else None
        course_.implementer = course.implementer.value if course.implementer else None
        course_.format = course.format.value if course.format else None
        course_.terms = course.terms.value if course.terms else None

        for role in course_.roles:
            await self.session.delete(role)

        for period in course_.periods:
            await self.session.delete(period)

        for run in course_.runs:
            await self.session.delete(run)

        course_.roles = [RoleForCourse(course_id=course.id, role_name=role.value) for role in course.roles]
        course_.periods = [PeriodForCourse(course_id=course.id, period_name=period.value) for period in course.periods]
        course_.runs = [RunForCourse(course_id=course.id, run_name=run.value) for run in course.last_runs]

    async def update_draft_status(self, course: CourseEntity) -> None:
        course_ = await self.__get_by_id(course.id)
        course_.is_draft = course.is_draft

    async def delete(self, course_id: str) -> None:
        course_ = await self.__get_by_id(course_id)
        course_.is_archive = True  # many related data
        course_.name = f"{course_.name} - {course_.id}"  # to avoid unique name after creating new course

    async def get_by_id(self, course_id: str) -> CourseEntity:
        try:
            course_ = await self.__get_by_id(course_id)
            return course_.to_domain()
        except NoResultFound as ex:
            raise CourseNotFoundError from ex

    async def __get_by_id(self, course_id: str) -> Course:
        query = (
            select(Course)
            .options(joinedload(Course.roles))
            .options(joinedload(Course.periods))
            .options(joinedload(Course.runs))
            .filter_by(id=course_id, is_archive=False)
        )
        try:
            result = await self.session.execute(query)
            return result.unique().scalars().one()
        except NoResultFound as ex:
            raise CourseNotFoundError from ex

    async def get_all(self) -> list[CourseEntity]:
        query = (
            select(Course)
            .options(joinedload(Course.roles))
            .options(joinedload(Course.periods))
            .options(joinedload(Course.runs))
            .filter_by(is_archive=False)
        )
        result = await self.session.execute(query)
        courses = result.unique().scalars().all()
        return [course.to_domain() for course in courses]
