from __future__ import annotations

import json
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, Literal

from src.domain.base_value_objects import UUID
from src.domain.courses.entities import CourseEntity
from src.domain.courses.value_objects import Author, CourseName, CourseRun, Format, Implementer, Period, Role, Terms
from src.infrastructure.redis.courses.constants import TIME_TO_LIVE_ALL_COURSES, TIME_TO_LIVE_ONE_COURSE
from src.services.courses.course_cache_service import CourseCacheService

if TYPE_CHECKING:
    from redis.asyncio import Redis


class RedisCourseCacheService(CourseCacheService):

    """Redis implementation class for cache of course as service."""

    def __init__(self, session: Redis, prefix: Literal["admin", "talent", "test"]) -> None:
        self.session = session
        self.prefix = prefix

    def __get_course_key(self, course_id: UUID) -> str:
        return self.prefix + "-course-" + course_id.value

    def __get_courses_key(self) -> str:
        return self.prefix + "-courses"

    @staticmethod
    def __from_domain_to_dict(course: CourseEntity) -> dict:
        return {
            "id": course.id.value,
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
            id=UUID(course_["id"]),
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

    async def get_one(self, course_id: UUID) -> CourseEntity | None:
        try:
            course_data_string = await self.session.get(self.__get_course_key(course_id))
            course_dict = json.loads(course_data_string)
            return self.__from_dict_to_domain(course_dict)
        except (TypeError, JSONDecodeError):  # no such key in Redis
            return None

    async def delete_one(self, course_id: UUID) -> None:
        await self.session.delete(self.__get_course_key(course_id))

    async def set_one(self, course: CourseEntity) -> None:
        course_dict = self.__from_domain_to_dict(course)
        course_data_string = json.dumps(course_dict)
        await self.session.setex(self.__get_course_key(course.id), TIME_TO_LIVE_ONE_COURSE, course_data_string)

    async def get_many(self) -> list[CourseEntity] | None:
        try:
            courses_data_string = await self.session.get(self.__get_courses_key())
            courses_dict = json.loads(courses_data_string)
            return [self.__from_dict_to_domain(course_dict) for course_dict in courses_dict]
        except (TypeError, JSONDecodeError):  # no such key in Redis
            return None

    async def delete_many(self) -> None:
        await self.session.delete(self.__get_courses_key())

    async def set_many(self, courses: list[CourseEntity]) -> None:
        courses_dict = [self.__from_domain_to_dict(course) for course in courses]
        courses_data_string = json.dumps(courses_dict)
        await self.session.setex(self.__get_courses_key(), TIME_TO_LIVE_ALL_COURSES, courses_data_string)
