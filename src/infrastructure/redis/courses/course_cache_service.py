import json
from json.decoder import JSONDecodeError

from redis.asyncio import Redis

from src.domain.courses.entities import CourseEntity
from src.domain.courses.value_objects import CourseName, Author, Implementer, CourseRun, Period, Role, Format, Terms
from src.infrastructure.redis.courses.constants import TIME_TO_LIVE_ONE_COURSE, TIME_TO_LIVE_ALL_COURSES
from src.services.courses.course_cache_service import CourseCacheService


COURSES_KEY = "courses"
COURSE_KEY = "course_"


class RedisCourseCacheService(CourseCacheService):

    """Redis implementation class for cache of course as service."""

    def __init__(self, session: Redis) -> None:
        self.session = session

    @staticmethod
    def __from_domain_to_dict(course: CourseEntity) -> dict:
        return {
            "id": course.id,
            "name": course.name.value,
            "image_url": course.image_url,
            "limits": course.limits,
            "is_draft": course.is_draft,
            "prerequisites": course.prerequisites,
            "description": course.description,
            "topics": course.topics,
            "assessment": course.assessment,
            "resources": course.resources,
            "extra": course.extra,
            "author": course.author.value if course.author else None,
            "implementer": course.implementer.value if course.implementer else None,
            "format": course.format.value if course.format else None,
            "terms": course.terms.value if course.terms else None,
            "roles": [item.value for item in course.roles],
            "periods": [item.value for item in course.periods],
            "last_runs": [item.value for item in course.last_runs],
        }

    @staticmethod
    def __from_dict_to_domain(course_: dict) -> CourseEntity:
        return CourseEntity(
            id=str(course_["id"]),
            name=CourseName(course_["name"]),
            image_url=course_["image_url"],
            limits=course_["limits"],
            is_draft=course_["is_draft"],
            prerequisites=course_["prerequisites"],
            description=course_["description"],
            topics=course_["topics"],
            assessment=course_["assessment"],
            resources=course_["resources"],
            extra=course_["extra"],
            author=Author(course_["author"]) if course_["author"] else None,
            implementer=Implementer(course_["implementer"]) if course_["implementer"] else None,
            format=Format(course_["format"]) if course_["format"] else None,
            terms=Terms(course_["terms"]) if course_["terms"] else None,
            roles=[Role(role) for role in course_["roles"]],
            periods=[Period(period) for period in course_["periods"]],
            last_runs=[CourseRun(run) for run in course_["last_runs"]],
        )

    async def get_one(self, course_id: str) -> CourseEntity | None:
        try:
            course_data_string = await self.session.get(COURSE_KEY + course_id)
            course_dict = json.loads(course_data_string)
            return self.__from_dict_to_domain(course_dict)
        except (TypeError, JSONDecodeError):  # no such key in Redis
            return None

    async def delete_one(self, course_id: str) -> None:
        await self.session.delete(COURSE_KEY + course_id)

    async def set_one(self, course: CourseEntity) -> None:
        course_dict = self.__from_domain_to_dict(course)
        course_data_string = json.dumps(course_dict)
        await self.session.set(COURSE_KEY + course.id, course_data_string, keepttl=TIME_TO_LIVE_ONE_COURSE)

    async def get_many(self) -> list[CourseEntity]:
        try:
            courses_data_string = await self.session.get(COURSES_KEY)
            courses_dict = json.loads(courses_data_string)
            return [self.__from_dict_to_domain(course_dict) for course_dict in courses_dict]
        except (TypeError, JSONDecodeError):  # no such key in Redis
            return []

    async def delete_many(self) -> None:
        await self.session.delete(COURSES_KEY)

    async def set_many(self, courses: list[CourseEntity]) -> None:
        courses_dict = [self.__from_domain_to_dict(course) for course in courses]
        courses_data_string = json.dumps(courses_dict)
        await self.session.set(COURSES_KEY, courses_data_string, keepttl=TIME_TO_LIVE_ALL_COURSES)
