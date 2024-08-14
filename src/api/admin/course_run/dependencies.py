from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.course_run.unit_of_work import SQLAlchemyCourseRunUnitOfWork
from src.infrastructure.sqlalchemy.session import get_async_session
from src.services.course_run.command_service import CourseRunCommandService


def get_admin_course_run_command_service(
    db_session: AsyncSession = Depends(get_async_session),
) -> CourseRunCommandService:
    """Get feedback service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyCourseRunUnitOfWork(db_session)
    return CourseRunCommandService(unit_of_work)
