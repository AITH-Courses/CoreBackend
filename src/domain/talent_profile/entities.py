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
    location: str = field(default="")
    position: str = field(default="")
    company: str = field(default="")
    link_ru_resume: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
    link_eng_resume: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
    link_tg_personal: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
    link_linkedin: EmptyLinkValueObject = field(default=EmptyLinkValueObject(""))
