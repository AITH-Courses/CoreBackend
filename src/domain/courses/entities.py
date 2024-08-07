from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.domain.courses.exceptions import CoursePublishError

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.courses.value_objects import (
        Author,
        CourseName,
        CourseRun,
        Format,
        Implementer,
        Period,
        Resource,
        Role,
        Terms,
    )


@dataclass
class CourseEntity:

    """Entity of course."""

    id: UUID
    name: CourseName
    image_url: str | None = field(default=None)
    limits: int | None = field(default=None)
    is_draft: bool = field(default=True)

    prerequisites: str | None = field(default=None)
    description: str | None = field(default=None)
    topics: str | None = field(default=None)
    assessment: str | None = field(default=None)
    resources: list[Resource] = field(default_factory=list)
    extra: str | None = field(default=None)

    author: Author | None = field(default=None)
    implementer: Implementer | None = field(default=None)
    format: Format | None = field(default=None)
    terms: Terms | None = field(default=None)
    roles: list[Role] = field(default_factory=list)
    periods: list[Period] = field(default_factory=list)
    last_runs: list[CourseRun] = field(default_factory=list)

    def publish(self) -> None:
        if not self.is_draft:
            raise CoursePublishError(error_message="Course has already published")
        if self.image_url is None:
            raise CoursePublishError(error_message="No image for course")
        if self.author is None:
            raise CoursePublishError(error_message="No author for course")
        if self.implementer is None:
            raise CoursePublishError(error_message="No implementer for course")
        if self.format is None:
            raise CoursePublishError(error_message="No format for course")
        if self.terms is None:
            raise CoursePublishError(error_message="No terms for course")
        if self.roles is None:
            raise CoursePublishError(error_message="No roles for course")
        if self.periods is None:
            raise CoursePublishError(error_message="No time of implementing course")
        self.is_draft = False

    def hide(self) -> None:
        if self.is_draft:
            raise CoursePublishError(error_message="Course has already hided")
        self.is_draft = True
