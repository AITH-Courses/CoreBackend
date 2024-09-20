from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.base_unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.sqlalchemy.course_run.repository import SQLAlchemyCourseRunRepository
from src.infrastructure.sqlalchemy.playlists.repository import SQLAlchemyPlaylistRepository
from src.services.playlists.unit_of_work import PlaylistUnitOfWork


class SQLAlchemyPlaylistUnitOfWork(SQLAlchemyUnitOfWork, PlaylistUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        super().__init__(sqla_session)
        self.playlist_repo = SQLAlchemyPlaylistRepository(sqla_session)
        self.course_run_repo = SQLAlchemyCourseRunRepository(sqla_session)
