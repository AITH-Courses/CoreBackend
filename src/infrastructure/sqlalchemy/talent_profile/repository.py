from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.domain.talent_profile.exceptions import TalentProfileNotFoundError
from src.domain.talent_profile.profile_repository import ITalentProfileRepository
from src.infrastructure.sqlalchemy.talent_profile.models import TalentProfile

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID
    from src.domain.talent_profile.entities import TalentProfileEntity


class SQLAlchemyTalentProfileRepository(ITalentProfileRepository):

    """SQLAlchemy's implementation of Repository for talent profile."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, profile: TalentProfileEntity) -> None:
        profile_ = TalentProfile.from_domain(profile)
        self.session.add(profile_)

    async def update(self, profile: TalentProfileEntity) -> None:
        profile_ = await self.__get_by_id(profile.id)
        profile_.location = profile.location
        profile_.position = profile.position
        profile_.company = profile.company
        profile_.link_ru_resume = profile.link_ru_resume.value
        profile_.link_eng_resume = profile.link_eng_resume.value
        profile_.link_tg_personal = profile.link_tg_personal.value
        profile_.link_linkedin = profile.link_linkedin.value

    async def delete(self, user_id: UUID) -> None:
        profile_ = await self.__get_by_id(user_id)
        await self.session.delete(profile_)

    async def get_by_user_id(self, user_id: UUID) -> TalentProfileEntity:
        profile_ = await self.__get_by_id(user_id)
        return profile_.to_domain()

    async def __get_by_id(self, user_id: UUID) -> TalentProfile:
        query = (
            select(TalentProfile)
            .filter_by(id=user_id.value)
        )
        try:
            result = await self.session.execute(query)
            return result.unique().scalars().one()
        except NoResultFound as ex:
            raise TalentProfileNotFoundError from ex
