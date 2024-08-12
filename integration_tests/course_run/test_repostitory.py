import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.base_value_objects import UUID
from src.domain.course_run.entities import CourseRunEntity
from src.domain.course_run.exceptions import CourseRunNotFoundError
from src.domain.courses.value_objects import CourseRun
from src.infrastructure.sqlalchemy.course_run.repository import SQLAlchemyCourseRunRepository


async def create_course_run(async_session: AsyncSession, course_id: UUID, name: str) -> tuple[UUID, SQLAlchemyCourseRunRepository]:
    repo = SQLAlchemyCourseRunRepository(async_session)
    course_run_id = UUID(str(uuid.uuid4()))
    await repo.create(CourseRunEntity(
        id=course_run_id,
        course_id=course_id,
        name=CourseRun(name)
    ))
    await async_session.commit()
    return course_run_id, repo


async def test_create_course_run(test_async_session: AsyncSession):
    course_id = UUID(str(uuid.uuid4()))
    course_run_id, repo = await create_course_run(test_async_session, course_id, "Весна 2024")
    course_run = await repo.get_by_id(course_run_id)
    assert course_run.id == course_run_id
    assert course_run.course_id == course_id
    assert course_run.name == CourseRun("Весна 2024")


async def test_get_all_course_runs(test_async_session: AsyncSession):
    course_id = UUID(str(uuid.uuid4()))
    course_run_1_id, _ = await create_course_run(test_async_session, course_id, "Весна 2024")
    course_run_2_id, repo = await create_course_run(test_async_session, course_id, "Весна 2025")
    courses = await repo.get_all_by_course_id(course_id)
    assert len(courses) == 2
    assert courses[0].id == course_run_2_id
    assert courses[1].id == course_run_1_id


async def test_delete_course_run(test_async_session: AsyncSession):
    course_id = UUID(str(uuid.uuid4()))
    course_run_1_id, repo = await create_course_run(test_async_session, course_id, "Весна 2024")
    await repo.delete(course_run_1_id)
    await test_async_session.commit()
    with pytest.raises(CourseRunNotFoundError):
        await repo.get_by_id(course_run_1_id)
