from src.domain.courses.course_repository import ICourseRepository
from src.domain.courses.entities import CourseEntity
from src.services.courses.course_cache_service import CourseCacheService


class CourseQueryService:

    """Class implemented CQRS pattern, query class."""

    def __init__(self, course_repo: ICourseRepository, course_cache_service: CourseCacheService) -> None:
        self.course_repo = course_repo
        self.course_cache_service = course_cache_service

    async def get_course(self, course_id: str) -> CourseEntity:
        course_from_cache = await self.course_cache_service.get_one(course_id)
        if course_from_cache:
            return course_from_cache
        course = await self.course_repo.get_by_id(course_id)
        await self.course_cache_service.set_one(course)
        return course

    async def get_courses(self) -> list[CourseEntity]:
        courses_from_cache = await self.course_cache_service.get_many()
        if courses_from_cache:
            return courses_from_cache
        courses = await self.course_repo.get_all()
        await self.course_cache_service.set_many(courses)
        return courses
