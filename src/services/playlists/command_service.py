from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from src.domain.base_value_objects import UUID, LinkValueObject
from src.domain.playlists.entities import PlaylistEntity
from src.domain.playlists.value_objects import VideoResourceType

if TYPE_CHECKING:
    from src.services.playlists.unit_of_work import PlaylistUnitOfWork


class PlaylistCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: PlaylistUnitOfWork) -> None:
        self.uow = uow

    async def get_playlists_by_course_run_id(self, course_run_id: str) -> list[PlaylistEntity]:
        course_run_id = UUID(course_run_id)
        return await self.uow.playlist_repo.get_all_by_course_run_id(course_run_id)

    async def create_playlist(self, course_run_id: str, name: str, playlist_type: str, link: str) -> None:
        playlist_id = UUID(str(uuid.uuid4()))
        course_run_id = UUID(course_run_id)
        playlist_type = VideoResourceType(playlist_type)
        link = LinkValueObject(link)
        playlist = PlaylistEntity(playlist_id, course_run_id, name, playlist_type, link)
        try:
            await self.uow.playlist_repo.create(playlist)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def update_playlist(self, playlist_id: str, course_run_id: str, name: str, playlist_type: str, link: str) -> None:
        playlist_id = UUID(playlist_id)
        course_run_id = UUID(course_run_id)
        playlist_type = VideoResourceType(playlist_type)
        link = LinkValueObject(link)
        playlist = PlaylistEntity(playlist_id, course_run_id, name, playlist_type, link)
        try:
            await self.uow.playlist_repo.update(playlist)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise

    async def delete_playlist(self, playlist_id: str) -> None:
        playlist_id = UUID(playlist_id)
        try:
            await self.uow.playlist_repo.delete(playlist_id)
            await self.uow.commit()
        except Exception:
            await self.uow.rollback()
            raise
