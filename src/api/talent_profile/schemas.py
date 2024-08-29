from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.talent_profile.entities import TalentProfileEntity


class ProfileGeneralUpdateRequest(BaseModel):

    """Schema of profile general information."""

    firstname: str = Field("Johny")
    lastname: str = Field("Stark")
    image_url: str | None = Field("image url")
    location: str = Field("Russia/Moscow")
    position: str = Field("ML Engineer")
    company: str = Field("Yandex")


class ProfileLinksUpdateRequest(BaseModel):

    """Schema of profile links."""

    link_ru_resume: str = Field("url")
    link_eng_resume: str = Field("url")
    link_tg_personal: str = Field("url")
    link_linkedin: str = Field("url")


class TalentProfileDTO(BaseModel):

    """Schema of talent profile."""

    user_id: str = Field("05219d1a-e1ef-4c8e-b307-89d41df8ec7b")
    firstname: str = Field("Johny")
    lastname: str = Field("Stark")
    image_url: str | None = Field("image url")
    location: str = Field("Russia/Moscow")
    position: str = Field("ML Engineer")
    company: str = Field("Yandex")
    link_ru_resume: str = Field("url")
    link_eng_resume: str = Field("url")
    link_tg_personal: str = Field("url")
    link_linkedin: str = Field("url")

    @staticmethod
    def from_entity(profile: TalentProfileEntity, firstname: str, lastname: str) -> TalentProfileDTO:
        return TalentProfileDTO(
            user_id=profile.id.value,
            firstname=firstname,
            lastname=lastname,
            image_url=profile.image_url,
            location=profile.location,
            position=profile.position,
            company=profile.company,
            link_ru_resume=profile.link_ru_resume.value,
            link_eng_resume=profile.link_eng_resume.value,
            link_tg_personal=profile.link_tg_personal.value,
            link_linkedin=profile.link_linkedin.value,
        )
