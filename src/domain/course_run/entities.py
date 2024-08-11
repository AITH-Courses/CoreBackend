from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.courses.value_objects import CourseRun


@dataclass
class CourseRunEntity:

    """Entity of timetable."""

    id: UUID
    course_id: UUID
    name: CourseRun
