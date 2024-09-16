from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError

from src.domain.base_exceptions import DomainError
from src.domain.base_value_objects import UUID, LinkValueObject
from src.domain.courses.value_objects import CourseName
from src.domain.group_google_calendar.entities import GroupGoogleCalendarEntity
from src.services.group_google_calendar.dto import UpdateGroupDTO, UpdateGroupGoogleCalendarDTO

if TYPE_CHECKING:
    from src.domain.course_run.entities import CourseRunEntity
    from src.services.group_google_calendar.unit_of_work import GroupGoogleCalendarUnitOfWork


class GroupGoogleCalendarCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: GroupGoogleCalendarUnitOfWork) -> None:
        self.uow = uow

    async def create(self, course_run_id: str, name: str, link: str) -> None:
        ggc_id = UUID(str(uuid.uuid4()))
        course_run_id = UUID(course_run_id)
        link = LinkValueObject(link)
        ggc = GroupGoogleCalendarEntity(ggc_id, course_run_id, name, link)
        try:
            await self.uow.ggc_repo.create(ggc)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def delete(self, group_google_calendar_id: str) -> None:
        group_google_calendar_id = UUID(group_google_calendar_id)
        try:
            await self.uow.ggc_repo.delete(group_google_calendar_id)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def get_groups(self, course_run_id: str) -> list[GroupGoogleCalendarEntity]:
        course_run_id = UUID(course_run_id)
        return await self.uow.ggc_repo.get_all_by_course_run_id(course_run_id)

    @staticmethod
    def __get_actual_course_run(course_runs:  list[CourseRunEntity], course_run_name: str) -> CourseRunEntity | None:
        for course_run in course_runs:
            if course_run.name.value == course_run_name:
                return course_run
        return None

    async def update(self, record: UpdateGroupGoogleCalendarDTO, course_run_name: str) -> str:
        updated_groups = set(record.groups)
        try:
            # Курс -> Актуальный запуск курса -> Текущие календари для групп этого запуска
            course_name = CourseName(record.course_name)
            course = await self.uow.course_repo.get_by_name(course_name)
            course_runs = await self.uow.course_run_repo.get_all_by_course_id(course.id)
            actual_course_run = self.__get_actual_course_run(course_runs, course_run_name)
            if not actual_course_run:
                return "Для курса нет запуска с указанным названием"
            ggc_list = await self.uow.ggc_repo.get_all_by_course_run_id(actual_course_run.id)
            current_groups: set[UpdateGroupDTO] = {UpdateGroupDTO(g.name, g.link.value) for g in ggc_list}
            # Добавляем новые группы
            to_add_groups: set[UpdateGroupDTO] = updated_groups - current_groups
            for g in to_add_groups:
                ggc_id = UUID(str(uuid.uuid4()))
                link = LinkValueObject(g.link)
                group = GroupGoogleCalendarEntity(ggc_id, actual_course_run.id, g.name, link)
                await self.uow.ggc_repo.create(group)
            # Удаляем старые группы
            to_remove_groups = current_groups - updated_groups
            for g in to_remove_groups:
                for current_group in ggc_list:
                    if current_group.link.value == g.link:
                        await self.uow.ggc_repo.delete(current_group.id)
            # Фиксируем изменения
            await self.uow.commit()
        except DomainError as e:
            await self.uow.rollback()
            return e.message
        except SQLAlchemyError as e:
            await self.uow.rollback()
            return str(e)
        else:
            return "OK"
