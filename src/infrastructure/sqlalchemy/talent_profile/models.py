from __future__ import annotations

import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base_value_objects import UUID, EmptyLinkValueObject
from src.domain.talent_profile.entities import TalentProfileEntity
from src.infrastructure.sqlalchemy.session import Base


class TalentProfile(Base):

    """SQLAlchemy model of Talent profile."""

    __tablename__ = "talent_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)
    company: Mapped[str] = mapped_column(nullable=False)
    link_ru_resume: Mapped[str] = mapped_column(nullable=False)
    link_eng_resume: Mapped[str] = mapped_column(nullable=False)
    link_tg_personal: Mapped[str] = mapped_column(nullable=False)
    link_linkedin: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(profile: TalentProfileEntity) -> TalentProfile:
        return TalentProfile(
            id=uuid.UUID(profile.id.value),
            image_url=profile.image_url,
            location=profile.location,
            position=profile.position,
            company=profile.company,
            link_ru_resume=profile.link_ru_resume.value,
            link_eng_resume=profile.link_eng_resume.value,
            link_tg_personal=profile.link_tg_personal.value,
            link_linkedin=profile.link_linkedin.value,
        )

    def to_domain(self) -> TalentProfileEntity:
        return TalentProfileEntity(
            id=UUID(str(self.id)),
            image_url=self.image_url,
            location=self.location,
            position=self.position,
            company=self.company,
            link_ru_resume=EmptyLinkValueObject(self.link_ru_resume),
            link_eng_resume=EmptyLinkValueObject(self.link_eng_resume),
            link_tg_personal=EmptyLinkValueObject(self.link_tg_personal),
            link_linkedin=EmptyLinkValueObject(self.link_linkedin),
        )
