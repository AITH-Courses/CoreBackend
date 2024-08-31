from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from src.domain.auth.value_objects import PartOfName
from src.domain.base_value_objects import UUID, EmptyLinkValueObject
from src.domain.talent_profile.entities import TalentProfileEntity
from src.domain.talent_profile.exceptions import TalentProfileAlreadyExistsError, TalentProfileForOnlyTalentError

if TYPE_CHECKING:
    from src.services.talent_profile.unit_of_work import TalentProfileUnitOfWork


class TalentProfileCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: TalentProfileUnitOfWork) -> None:
        self.uow = uow

    async def create_profile(self, user_id: str, role: str) -> None:
        if role != "talent":
            raise TalentProfileForOnlyTalentError
        user_id = UUID(str(user_id))
        try:
            profile = TalentProfileEntity(user_id)
            await self.uow.profile_repo.create(profile)
            await self.uow.commit()
        except IntegrityError as ex:
            await self.uow.rollback()
            raise TalentProfileAlreadyExistsError from ex
        except Exception:
            await self.uow.rollback()
            raise

    async def update_profile(
            self, user_id: str, firstname: str, lastname: str, image_url: str | None,
            location: str, position: str, company: str,
    ) -> None:
        user_id = UUID(str(user_id))
        try:
            user = await self.uow.user_repo.get_by_id(user_id)
            user.firstname = PartOfName(firstname)
            user.lastname = PartOfName(lastname)
            await self.uow.user_repo.update(user)
            profile = await self.uow.profile_repo.get_by_user_id(user_id)
            profile.update_profile(image_url, location, position, company)
            await self.uow.profile_repo.update(profile)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def update_links(
            self, user_id: str, link_ru_resume: str, link_eng_resume: str,
            link_tg_personal: str, link_linkedin: str,
    ) -> None:
        user_id = UUID(str(user_id))
        link_ru_resume = EmptyLinkValueObject(link_ru_resume)
        link_eng_resume = EmptyLinkValueObject(link_eng_resume)
        link_tg_personal = EmptyLinkValueObject(link_tg_personal)
        link_linkedin = EmptyLinkValueObject(link_linkedin)
        try:
            profile = await self.uow.profile_repo.get_by_user_id(user_id)
            profile.update_links(link_ru_resume, link_eng_resume, link_tg_personal, link_linkedin)
            await self.uow.profile_repo.update(profile)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def delete(self, user_id: str) -> None:
        user_id = UUID(user_id)
        try:
            await self.uow.profile_repo.delete(user_id)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def get_profile(self, user_id: str) -> TalentProfileEntity:
        """Get firstname, lastname and talent profile information.

        :param user_id:
        :return:
        """
        user_id = UUID(user_id)
        return await self.uow.profile_repo.get_by_user_id(user_id)
