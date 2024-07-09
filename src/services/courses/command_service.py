import uuid

from sqlalchemy.exc import IntegrityError

from src.domain.courses.entities import CourseEntity
from src.domain.courses.exceptions import CourseAlreadyExistsError, CourseNotFoundError
from src.domain.courses.value_objects import CourseName, CourseRun, Period, Implementer, Author, Format, Terms, Role
from src.services.courses.unit_of_work import CoursesUnitOfWork


class CourseCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: CoursesUnitOfWork) -> None:
        self.uow = uow

    async def create_course(self, name_: str) -> str:
        course_id = str(uuid.uuid4())
        name = CourseName(name_)
        course = CourseEntity(course_id, name)
        try:
            await self.uow.course_repo.create(course)
            await self.uow.commit()
        except IntegrityError as ex:
            await self.uow.rollback()
            raise CourseAlreadyExistsError from ex
        except Exception as ex:
            await self.uow.rollback()
            raise ex
        return course_id

    async def update_course(
            self, course_id: str, name_: str, image_url: str | None, limits_: int | None,
            prerequisites_: str | None, description_: str | None, topics_: str | None,
            assessment_: str | None, resources_: str | None, extra_: str | None,
            author_: str | None, implementer_: str | None, format_: str | None,
            terms_: str | None, roles: list[str], periods: list[str], runs: list[str]
    ) -> None:
        course = CourseEntity(
            id=str(course_id),
            name=CourseName(name_),
            image_url=image_url,
            limits=limits_,
            prerequisites=prerequisites_,
            description=description_,
            topics=topics_,
            assessment=assessment_,
            resources=resources_,
            extra=extra_,
            author=Author(author_) if author_ else None,
            implementer=Implementer(implementer_) if implementer_ else None,
            format=Format(format_) if format_ else None,
            terms=Terms(terms_) if terms_ else None,
            roles=[Role(role) for role in roles],
            periods=[Period(period) for period in periods],
            last_runs=[CourseRun(run) for run in runs],
        )
        try:
            await self.uow.course_repo.update(course)
            await self.uow.commit()
        except IntegrityError as ex:
            await self.uow.rollback()
            raise CourseAlreadyExistsError from ex
        except CourseNotFoundError as ex:
            await self.uow.rollback()
            raise ex

    async def delete_course(self, course_id: str) -> None:
        try:
            await self.uow.course_repo.delete(course_id)
            await self.uow.commit()
        except CourseNotFoundError as ex:
            await self.uow.rollback()
            raise ex

    async def publish_course(self, course_id: str) -> None:
        try:
            course = await self.uow.course_repo.get_by_id(course_id)
            course.publish()
            await self.uow.course_repo.update(course)
            await self.uow.commit()
        except CourseNotFoundError as ex:
            await self.uow.rollback()
            raise ex

    async def hide_course(self, course_id: str) -> None:
        try:
            course = await self.uow.course_repo.get_by_id(course_id)
            course.hide()
            await self.uow.course_repo.update(course)
            await self.uow.commit()
        except CourseNotFoundError as ex:
            await self.uow.rollback()
            raise ex
