from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID


@dataclass
class FavoriteCourseEntity:

    """Entity of talent profile."""

    id: UUID
    user_id: UUID
    course_id: UUID
