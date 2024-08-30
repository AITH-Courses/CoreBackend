from __future__ import annotations

import datetime
import uuid

from sqlalchemy import UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base_value_objects import UUID
from src.domain.favorite_courses.entities import FavoriteCourseEntity
from src.infrastructure.sqlalchemy.session import Base


class FavoriteCourse(Base):

    """SQLAlchemy model of Course."""

    __tablename__ = "favorite_courses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    course_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uix_course_id_user_id"),)

    @staticmethod
    def from_domain(favorite_course: FavoriteCourseEntity) -> FavoriteCourse:
        return FavoriteCourse(
            id=favorite_course.id.value,
            user_id=favorite_course.user_id.value,
            course_id=favorite_course.course_id.value,
        )

    def to_domain(self) -> FavoriteCourseEntity:
        return FavoriteCourseEntity(
            id=UUID(str(self.id)),
            user_id=UUID(str(self.user_id)),
            course_id=UUID(str(self.course_id)),
        )
