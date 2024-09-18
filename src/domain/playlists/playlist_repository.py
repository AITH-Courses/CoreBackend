from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.playlists.entities import PlaylistEntity


class IVideoPlaylistRepository(ABC):

    """Interface of Repository for Video playlist."""

    @abstractmethod
    async def create(self, video_playlist: PlaylistEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, video_playlist: PlaylistEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, video_playlist_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_course_run_id(self, course_run_id: UUID) -> list[PlaylistEntity]:
        raise NotImplementedError
