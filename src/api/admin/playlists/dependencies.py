from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends

from src.infrastructure.sqlalchemy.playlists.unit_of_work import SQLAlchemyPlaylistUnitOfWork
from src.infrastructure.sqlalchemy.session import get_async_session
from src.services.playlists.command_service import PlaylistCommandService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def get_playlist_service(
        db_session: AsyncSession = Depends(get_async_session),
) -> PlaylistCommandService:
    """Get playlist service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyPlaylistUnitOfWork(db_session)
    return PlaylistCommandService(unit_of_work)
