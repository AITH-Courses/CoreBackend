from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.domain.courses.exceptions import CoursePublishError

if TYPE_CHECKING:
    from src.domain.courses.value_objects import Implementer, CourseName, Format, Terms, Role, Period, Author, CourseRun


@dataclass
class CourseEntity:

    """Entity of course."""

    id: str
    name: CourseName
    image_url: str | None
    limits: int | None
    is_draft: bool

    prerequisites: str | None
    description: str | None
    topics: str | None
    assessment: str | None
    resources: str | None
    extra: str | None

    author: Author | None
    implementer: Implementer | None
    format: Format | None
    terms: Terms | None
    roles: list[Role]
    periods: list[Period]
    last_runs: list[CourseRun]

    def publish(self):
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
        if self.format is None:
            raise CoursePublishError(error_message="No format for course")
        if self.terms is None:
            raise CoursePublishError(error_message="No format for course")
        if self.roles is None:
            raise CoursePublishError(error_message="No roles for course")
        if self.periods is None:
            raise CoursePublishError(error_message="No time of implementing course")
        self.is_draft = False

    def hide(self):
        if self.is_draft:
            raise CoursePublishError(error_message="Course has already hided")
        self.is_draft = True
