import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.courses.constants import PERIODS, ROLES
from src.domain.courses.entities import CourseEntity
from src.domain.courses.exceptions import CourseNotFoundError
from src.domain.courses.value_objects import CourseName, Period, Role, CourseRun
from src.infrastructure.sqlalchemy.courses.repository import SQLAlchemyCourseRepository


async def create_course(async_session: AsyncSession) -> tuple[str, SQLAlchemyCourseRepository]:
    repo = SQLAlchemyCourseRepository(async_session)
    course_id = str(uuid.uuid4())
    await repo.create(CourseEntity(
        id=course_id,
        name=CourseName("Алгоритмизация")
    ))
    await async_session.commit()
    return course_id, repo


async def test_create_course(test_async_session: AsyncSession):
    course_id, repo = await create_course(test_async_session)
    course = await repo.get_by_id(course_id)
    assert course.id == course_id
    assert course.name == CourseName("Алгоритмизация")
    assert course.image_url is None
    assert len(course.roles) == 0
    assert len(course.periods) == 0
    assert len(course.last_runs) == 0


async def test_get_many_courses(test_async_session: AsyncSession):
    course_id, repo = await create_course(test_async_session)
    courses = await repo.get_all()
    assert len(courses) == 1
    assert courses[0].id == course_id
    assert courses[0].name == CourseName("Алгоритмизация")
    assert courses[0].image_url is None
    assert len(courses[0].roles) == 0
    assert len(courses[0].periods) == 0
    assert len(courses[0].last_runs) == 0


async def test_update_course(test_async_session: AsyncSession):
    course_id, repo = await create_course(test_async_session)
    update_course = CourseEntity(
        course_id,
        name=CourseName("Методы алгоритмизации"),
        image_url="image/path-to-file.png",
        roles=[Role(ROLES[0])],
        periods=[Period(PERIODS[0])],
        last_runs=[CourseRun("Весна 2023")],
    )
    await repo.update(update_course)
    await test_async_session.commit()
    course = await repo.get_by_id(course_id)
    assert course.id == course_id
    assert course.name == CourseName("Методы алгоритмизации")
    assert course.image_url == "image/path-to-file.png"
    assert course.implementer is None
    assert course.format is None
    assert course.terms is None
    assert course.author is None
    assert len(course.roles) == len(update_course.roles)
    assert course.roles[0] == update_course.roles[0]
    assert len(course.periods) == len(update_course.periods)
    assert course.periods[0] == update_course.periods[0]
    assert len(course.last_runs) == len(update_course.last_runs)
    assert course.last_runs[0] == update_course.last_runs[0]


async def test_delete_course(test_async_session: AsyncSession):
    course_id, repo = await create_course(test_async_session)
    await repo.delete(course_id)
    await test_async_session.commit()
    with pytest.raises(CourseNotFoundError):
        await repo.get_by_id(course_id)


async def test_update_course_after_delete(test_async_session: AsyncSession):
    course_id, repo = await create_course(test_async_session)
    await repo.delete(course_id)
    await test_async_session.commit()
    with pytest.raises(CourseNotFoundError):
        update_course = CourseEntity(
            course_id,
            name=CourseName("Методы алгоритмизации"),
        )
        await repo.update(update_course)
        await test_async_session.commit()

