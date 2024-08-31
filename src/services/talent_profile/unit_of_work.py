from abc import ABC

from src.domain.auth.user_repository import IUserRepository
from src.domain.talent_profile.profile_repository import ITalentProfileRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class TalentProfileUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    user_repo: IUserRepository
    profile_repo: ITalentProfileRepository
