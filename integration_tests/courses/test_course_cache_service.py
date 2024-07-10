import pytest

from src.domain.courses.entities import CourseEntity
from src.domain.auth.exceptions import UserBySessionNotFoundError
from src.domain.courses.value_objects import CourseName, CourseRun
from src.infrastructure.redis.courses.course_cache_service import RedisCourseCacheService


@pytest.fixture(scope='function')
def redis_course_cache_service(test_cache_session):
    return RedisCourseCacheService(test_cache_session)


async def test_operations_with_one_course(redis_course_cache_service):
    course_id = "ds3ffa4fs5dgw3r"
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
        id="24fsf4sg5ghs",
        name=CourseName("Алгоритмизация")
    )
    course_2 = CourseEntity(
        id="gd4fga3d5afa1f",
        name=CourseName("Java")
    )
    await redis_course_cache_service.set_many([course_1, course_2])

    getting_courses = await redis_course_cache_service.get_many()
    assert len(getting_courses) == 2
    assert getting_courses[0].name == CourseName("Алгоритмизация")
    assert getting_courses[1].name == CourseName("Java")

    await redis_course_cache_service.delete_many()

    deleted_courses = await redis_course_cache_service.get_many()
    assert len(deleted_courses) ==0
