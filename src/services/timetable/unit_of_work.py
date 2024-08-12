from abc import ABC

from src.domain.timetable.timetable_repository import ITimetableRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class TimetableUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    timetable_repo: ITimetableRepository
