import uuid

import pytest

from src.domain.base_value_objects import UUID
from src.domain.courses.entities import CourseEntity
from src.domain.courses.value_objects import CourseName, CourseRun
from src.infrastructure.redis.courses.course_cache_service import RedisCourseCacheService


@pytest.fixture(scope='function')
def redis_course_cache_service(test_cache_session):
    return RedisCourseCacheService(test_cache_session, "test")


async def test_operations_with_one_course(redis_course_cache_service):
    course_id = UUID(str(uuid.uuid4()))
    course = CourseEntity(
        id=course_id,
        name=CourseName("Алгоритмизация"),
        last_runs=[CourseRun("Весна 2023"), CourseRun("Осень 2024")]
    )
    await redis_course_cache_service.set_one(course)

    getting_course = await redis_course_cache_service.get_one(course_id)
    assert getting_course.id == course.id
    assert getting_course.name == course.name
    assert getting_course.limits == course.limits
    assert len(getting_course.roles) == 0
    assert len(getting_course.last_runs) == 2
    assert getting_course.last_runs[0] == course.last_runs[0]
    assert getting_course.last_runs[1] == course.last_runs[1]

    await redis_course_cache_service.delete_one(course_id)

    deleted_course = await redis_course_cache_service.get_one(course_id)
    assert deleted_course is None


async def test_operations_with_all_courses(redis_course_cache_service):
    course_1 = CourseEntity(
        id=UUID(str(uuid.uuid4())),
        name=CourseName("Алгоритмизация")
    )
    course_2 = CourseEntity(
        id=UUID(str(uuid.uuid4())),
        name=CourseName("Java")
    )
    await redis_course_cache_service.set_many([course_1, course_2])

    getting_courses = await redis_course_cache_service.get_many()
    assert len(getting_courses) == 2
    assert getting_courses[0].name == CourseName("Алгоритмизация")
    assert getting_courses[1].name == CourseName("Java")

    await redis_course_cache_service.delete_many()

    deleted_courses = await redis_course_cache_service.get_many()
    assert deleted_courses is None
