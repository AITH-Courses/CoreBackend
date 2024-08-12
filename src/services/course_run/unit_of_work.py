from abc import ABC

from src.domain.course_run.course_run_repository import ICourseRunRepository
from src.domain.timetable.timetable_repository import ITimetableRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class CourseRunUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    course_run_repo: ICourseRunRepository
    timetable_repo: ITimetableRepository
