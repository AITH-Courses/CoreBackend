from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.domain.courses.exceptions import CourseNotFoundError

if TYPE_CHECKING:
    from src.domain.courses.course_repository import ICourseRepository
    from src.domain.courses.entities import CourseEntity
    from src.services.courses.course_cache_service import CourseCacheService


@dataclass
class CourseFilter:

    """Class for filters on courses."""

    implementers: list[str] | None
    formats: list[str] | None
    terms: list[str] | None
    roles: list[str] | None


class TalentCourseQueryService:

    """Class implemented CQRS pattern, query class for talent."""

    def __init__(self, course_repo: ICourseRepository, course_cache_service: CourseCacheService) -> None:
        self.course_repo = course_repo
        self.course_cache_service = course_cache_service

    async def get_course(self, course_id: str) -> CourseEntity:
        course_from_cache = await self.course_cache_service.get_one(course_id)
        if course_from_cache and not course_from_cache.is_draft:
            return course_from_cache
        course = await self.course_repo.get_by_id(course_id)
        if course.is_draft:
            raise CourseNotFoundError
        await self.course_cache_service.set_one(course)
        return course

    async def get_courses(self, filters: CourseFilter) -> list[CourseEntity]:
        courses_from_cache = await self.course_cache_service.get_many()
        if courses_from_cache:
            return [course for course in courses_from_cache if not course.is_draft and self.__matched(course, filters)]
        courses = await self.course_repo.get_all()
        courses = [course for course in courses if not course.is_draft]
        await self.course_cache_service.set_many(courses)
        return [course for course in courses if self.__matched(course, filters)]

    @staticmethod
    def __matched(course: CourseEntity, filters: CourseFilter) -> bool:
        if filters.roles:
            course_roles = [r.value for r in course.roles]
            if not set(filters.roles).intersection(set(course_roles)):
                return False
        if filters.implementers:
            course_implementer = course.implementer.value
            if course_implementer not in filters.implementers:
                return False
        if filters.terms:
            course_terms = course.terms.value.split(", ")
            if not set(filters.terms).intersection(set(course_terms)):
                return False
        if filters.formats:
            course_format = course.format.value
            if course_format not in filters.formats:
                return False
        return True
