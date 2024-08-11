from __future__ import annotations

import datetime
import uuid

from sqlalchemy import text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base_value_objects import UUID
from src.domain.course_run.entities import CourseRunEntity
from src.domain.courses.value_objects import CourseRun as CourseRunName
from src.infrastructure.sqlalchemy.session import Base


class CourseRun(Base):

    """SQLAlchemy model of Course."""

    __tablename__ = "course_runs_"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    course_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    is_archive: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    __table_args__ = (UniqueConstraint('course_id', 'name', name='uix_name_email'),)

    @staticmethod
    def from_domain(course_run: CourseRunEntity) -> CourseRun:
        return CourseRun(
            id=course_run.id.value,
            course_id=course_run.course_id.value,
            name=course_run.name.value,
        )

    def to_domain(self) -> CourseRunEntity:
        return CourseRunEntity(
            id=UUID(str(self.id)),
            course_id=UUID(str(self.course_id)),
            name=CourseRunName(self.name),
        )
