from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update

from src.domain.playlists.exceptions import PlaylistNotFoundError
from src.domain.playlists.playlist_repository import IPlaylistRepository
from src.infrastructure.sqlalchemy.playlists.models import Playlist

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.base_value_objects import UUID
    from src.domain.playlists.entities import PlaylistEntity


class SQLAlchemyPlaylistRepository(IPlaylistRepository):

    """SQLAlchemy's implementation of Repository for Playlist."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, playlist: PlaylistEntity) -> None:
        playlist_ = Playlist.from_domain(playlist)
        self.session.add(playlist_)

    async def update(self, playlist: PlaylistEntity) -> None:
        playlist_ = Playlist.from_domain(playlist)
        update_statement = (
            update(Playlist)
            .where(Playlist.id == playlist_.id)
            .values(name=playlist_.name, link=playlist_.link, type=playlist_.type)
        )
        result = await self.session.execute(update_statement)
        if result.rowcount == 0:
            raise PlaylistNotFoundError

    async def delete(self, playlist_id: UUID) -> None:
        delete_statement = (
            delete(Playlist)
            .where(Playlist.id == playlist_id.value)
        )
        result = await self.session.execute(delete_statement)
        if result.rowcount == 0:
            raise PlaylistNotFoundError

    async def get_all_by_course_run_id(self, course_run_id: UUID) -> list[PlaylistEntity]:
        query = (
            select(Playlist)
            .filter_by(course_run_id=course_run_id.value)
            .order_by(Playlist.created_at.desc())
        )
        result = await self.session.execute(query)
        playlists = result.unique().scalars().all()
        return [playlist.to_domain() for playlist in playlists]
