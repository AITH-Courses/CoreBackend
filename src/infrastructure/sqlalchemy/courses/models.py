from __future__ import annotations

import datetime
import uuid

from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.base_value_objects import UUID
from src.domain.courses.entities import CourseEntity
from src.domain.courses.value_objects import Author, CourseName, CourseRun, Format, Implementer, Period, Role, Terms
from src.infrastructure.sqlalchemy.session import Base


class Course(Base):

    """SQLAlchemy model of Course."""

    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    image_url: Mapped[str] = mapped_column(nullable=True)
    limits: Mapped[int] = mapped_column(nullable=True)
    is_draft: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_archive: Mapped[bool] = mapped_column(nullable=False, default=False)

    prerequisites: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    topics: Mapped[str] = mapped_column(Text, nullable=True)
    assessment: Mapped[str] = mapped_column(Text, nullable=True)
    resources: Mapped[str] = mapped_column(Text, nullable=True)
    extra: Mapped[str] = mapped_column(Text, nullable=True)

    author: Mapped[str] = mapped_column(nullable=True)
    implementer: Mapped[str] = mapped_column(nullable=True)
    format: Mapped[str] = mapped_column(nullable=True)
    terms: Mapped[str] = mapped_column(nullable=True)

    roles: Mapped[list[RoleForCourse]] = relationship(back_populates="course")
    periods: Mapped[list[PeriodForCourse]] = relationship(back_populates="course")
    runs: Mapped[list[RunForCourse]] = relationship(back_populates="course")

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(course: CourseEntity) -> Course:
        return Course(
            id=course.id.value,
            name=course.name.value,
            image_url=course.image_url,
            limits=course.limits,
            prerequisites=course.prerequisites,
            description=course.description,
            topics=course.topics,
            assessment=course.assessment,
            resources=course.resources,
            extra=course.extra,
            author=course.author.value if course.author else None,
            implementer=course.implementer.value if course.implementer else None,
            format=course.format.value if course.format else None,
            terms=course.terms.value if course.terms else None,
            roles=[RoleForCourse(course_id=course.id, role_name=role.value) for role in course.roles],
            periods=[PeriodForCourse(course_id=course.id, period_name=period.value) for period in course.periods],
            runs=[RunForCourse(course_id=course.id, run_name=run.value) for run in course.last_runs],
        )

    def to_domain(self) -> CourseEntity:
        course_ = self
        return CourseEntity(
            id=UUID(str(course_.id)),
            name=CourseName(course_.name),
            image_url=course_.image_url,
            limits=course_.limits,
            is_draft=course_.is_draft,
            prerequisites=course_.prerequisites,
            description=course_.description,
            topics=course_.topics,
            assessment=course_.assessment,
            resources=course_.resources,
            extra=course_.extra,
            author=Author(str(course_.author)) if course_.author else None,
            implementer=Implementer(str(course_.implementer)) if course_.implementer else None,
            format=Format(str(course_.format)) if course_.format else None,
            terms=Terms(str(course_.terms)) if course_.terms else None,
            roles=[Role(role.role_name) for role in course_.roles],
            periods=[Period(period.period_name) for period in course_.periods],
            last_runs=[CourseRun(run.run_name) for run in course_.runs],
        )


class RoleForCourse(Base):

    """SQLAlchemy model of Role for course."""

    __tablename__ = "course_roles"

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    role_name: Mapped[str] = mapped_column(primary_key=True)
    course: Mapped[Course] = relationship(back_populates="roles")


class PeriodForCourse(Base):

    """SQLAlchemy model of Period for course."""

    __tablename__ = "course_periods"

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    period_name: Mapped[str] = mapped_column(primary_key=True)
    course: Mapped[Course] = relationship(back_populates="periods")


class RunForCourse(Base):

    """SQLAlchemy model of Period for course."""

    __tablename__ = "course_runs"

    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    run_name: Mapped[str] = mapped_column(primary_key=True)
    course: Mapped[Course] = relationship(back_populates="runs")
