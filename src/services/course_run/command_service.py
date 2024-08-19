from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from src.domain.base_value_objects import UUID
from src.domain.course_run.entities import CourseRunEntity
from src.domain.course_run.exceptions import CourseRunAlreadyExistsError
from src.domain.courses.value_objects import CourseRun
from src.domain.timetable.entities import TimetableEntity
from src.domain.timetable.exceptions import NoActualTimetableError, TimetableNotFoundError

if TYPE_CHECKING:
    from src.services.course_run.unit_of_work import CourseRunUnitOfWork


class CourseRunCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: CourseRunUnitOfWork) -> None:
        self.uow = uow

    async def create_course_run(self, course_id: str, season: str, year: int) -> str:
        course_run_id = UUID(str(uuid.uuid4()))
        course_id = UUID(course_id)
        course_run_name = CourseRun(f"{season} {year}")
        course_run = CourseRunEntity(course_run_id, course_id, course_run_name)
        timetable_id = UUID(str(uuid.uuid4()))
        timetable = TimetableEntity(timetable_id, course_run_id)
        try:
            await self.uow.course_run_repo.create(course_run)
            await self.uow.timetable_repo.create(timetable)
            await self.uow.commit()
        except IntegrityError as ex:
            await self.uow.rollback()
            raise CourseRunAlreadyExistsError from ex
        except Exception:
            await self.uow.rollback()
            raise
        return course_run_id.value

    async def delete_course_run(self, course_run_id: str) -> None:
        course_run_id = UUID(course_run_id)
        try:
            await self.uow.course_run_repo.delete(course_run_id)
            timetable = await self.uow.timetable_repo.get_by_id(course_run_id)
            for rule in timetable.rules:
                await self.uow.timetable_repo.delete_rule(rule.id)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def get_course_run_by_id(self, course_run_id: str) -> CourseRunEntity:
        course_run_id = UUID(course_run_id)
        return await self.uow.course_run_repo.get_by_id(course_run_id)

    async def get_all_course_runs_by_id(self, course_id: str) -> list[CourseRunEntity]:
        course_id = UUID(course_id)
        return await self.uow.course_run_repo.get_all_by_course_id(course_id)

    async def get_actual_timetable_by_id(self, course_id: str) -> tuple[TimetableEntity, CourseRunEntity]:
        current_date = datetime.datetime.now().date()
        course_id = UUID(course_id)
        course_runs = await self.uow.course_run_repo.get_all_by_course_id(course_id)
        for course_run in course_runs:
            if course_run.is_actual_by_date(current_date):
                error_message = "Для актуального запуска еще не создано расписание"
                try:
                    timetable = await self.uow.timetable_repo.get_by_id(course_run.id)
                    if not timetable.lessons:
                        raise NoActualTimetableError(error_message=error_message)
                except TimetableNotFoundError as ex:
                    raise NoActualTimetableError(error_message=error_message) from ex
                else:
                    return timetable, course_run
        raise NoActualTimetableError(error_message="Для курса еще не создан актуальный запуск")

