from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.domain.base_value_objects import EmptyLinkValueObject

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID


@dataclass
class TalentProfileEntity:

    """Entity of talent profile."""

    id: UUID
    image_url: str | None = field(default=None)
    location: str = field(default="")
    position: str = field(default="")
    company: str = field(default="")
    link_ru_resume: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
    link_eng_resume: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
    link_tg_personal: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
    link_linkedin: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))

    def update_profile(self, image_url: str | None, location: str, position: str, company: str) -> None:
        self.image_url = image_url
        self.location = location
        self.position = position
        self.company = company

    def update_links(
            self, link_ru_resume: EmptyLinkValueObject, link_eng_resume: EmptyLinkValueObject,
            link_tg_personal: EmptyLinkValueObject, link_linkedin: EmptyLinkValueObject,
    ) -> None:
        self.link_ru_resume = link_ru_resume
        self.link_eng_resume = link_eng_resume
        self.link_tg_personal = link_tg_personal
        self.link_linkedin = link_linkedin
