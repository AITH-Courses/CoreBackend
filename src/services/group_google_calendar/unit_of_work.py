from abc import ABC

from src.domain.course_run.course_run_repository import ICourseRunRepository
from src.domain.courses.course_repository import ICourseRepository
from src.domain.group_google_calendar.ggc_repository import IGroupGoogleCalendarRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class GroupGoogleCalendarUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    ggc_repo: IGroupGoogleCalendarRepository
    course_repo: ICourseRepository
    course_run_repo: ICourseRunRepository
