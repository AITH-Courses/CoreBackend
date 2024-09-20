from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID, LinkValueObject
    from src.domain.playlists.value_objects import VideoResourceType


@dataclass
class PlaylistEntity:

    """Entity of group timetable for day."""

    id: UUID
    course_run_id: UUID
    name: str  # name of resource, optional
    type: VideoResourceType
    link: LinkValueObject
