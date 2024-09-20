from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.domain.base_value_objects import UUID
from src.domain.courses.exceptions import CourseNotFoundError

if TYPE_CHECKING:
    from src.domain.courses.course_repository import ICourseRepository
    from src.domain.courses.entities import CourseEntity
    from src.services.courses.course_cache_service import CourseCacheService


@dataclass
class CourseFilter:

    """Class for filters on courses."""

    implementers: list[str] | None = field(default=None)
    formats: list[str] | None = field(default=None)
    terms: list[str] | None = field(default=None)
    roles: list[str] | None = field(default=None)
    query: str | None = field(default=None)
    only_actual: bool = field(default=False)


class TalentCourseQueryService:

    """Class implemented CQRS pattern, query class for talent."""

    def __init__(self, course_repo: ICourseRepository, course_cache_service: CourseCacheService) -> None:
        self.course_repo = course_repo
        self.course_cache_service = course_cache_service

    async def get_course(self, course_id: str) -> CourseEntity:
        course_id = UUID(course_id)
        course_from_cache = await self.course_cache_service.get_one(course_id)
        if course_from_cache and not course_from_cache.is_draft:
            return course_from_cache
        course = await self.course_repo.get_by_id(course_id)
        if course.is_draft:
            raise CourseNotFoundError
        await self.course_cache_service.set_one(course)
        return course

    async def get_courses(self, filters: CourseFilter) -> list[CourseEntity]:
        actual_run = self.__get_actual_run()
        courses_from_cache = await self.course_cache_service.get_many()
        if courses_from_cache:
            return [
                course for course in courses_from_cache
                if not course.is_draft and self.__matched(course, filters, actual_run)
            ]
        courses = await self.course_repo.get_all()
        courses = [course for course in courses if not course.is_draft]
        await self.course_cache_service.set_many(courses)
        return [course for course in courses if self.__matched(course, filters, actual_run)]

    async def invalidate_course(self, course_id: str) -> None:
        await self.course_cache_service.delete_one(UUID(course_id))
        await self.course_cache_service.delete_many()

    @staticmethod
    def __matched(course: CourseEntity, filters: CourseFilter, actual_run: str) -> bool:
        if filters.roles and not set(filters.roles).intersection({r.value for r in course.roles}):
            return False
        if filters.implementers and course.implementer.value not in filters.implementers:
            return False
        if filters.terms and not set(filters.terms).intersection(set(course.terms.value.split(", "))):
            return False
        if filters.formats and course.format.value not in filters.formats:
            return False
        if filters.query and filters.query.lower() not in course.name.value.lower():
            return False
        return not filters.only_actual or actual_run in {run.value for run in course.last_runs}

    @staticmethod
    def __get_actual_run() -> str:
        current_date = datetime.datetime.now().date()
        month, year = current_date.month, current_date.year
        if month in (8, 9, 10, 11, 12):
            return f"{'Осень'} {year}"
        return f"{'Весна'} {year}"
