from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING

from src.domain.base_value_objects import UUID, LinkValueObject
from src.domain.course_run.exceptions import NoActualCourseRunError
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

    async def get_actual_playlists(self, course_id: str) -> list[PlaylistEntity]:
        current_date = datetime.datetime.now().date()
        course_id = UUID(course_id)
        course_runs = await self.uow.course_run_repo.get_all_by_course_id(course_id)
        for course_run in course_runs:
            if course_run.is_actual_by_date(current_date):
                return await self.uow.playlist_repo.get_all_by_course_run_id(course_run.id)
        raise NoActualCourseRunError

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

    async def update_playlist(self, playlist_id: str, course_run_id: str, name: str, type_: str, link: str) -> None:
        playlist_id = UUID(playlist_id)
        course_run_id = UUID(course_run_id)
        playlist_type = VideoResourceType(type_)
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
