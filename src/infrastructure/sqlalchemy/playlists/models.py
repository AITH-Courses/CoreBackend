from __future__ import annotations

import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base_value_objects import UUID, LinkValueObject
from src.domain.playlists.entities import PlaylistEntity
from src.domain.playlists.value_objects import VideoResourceType
from src.infrastructure.sqlalchemy.session import Base


class Playlist(Base):

    """SQLAlchemy model of Playlist."""

    __tablename__ = "playlists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    course_run_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    @staticmethod
    def from_domain(playlist: PlaylistEntity) -> Playlist:
        return Playlist(
            id=uuid.UUID(playlist.id.value),
            course_run_id=uuid.UUID(playlist.course_run_id.value),
            name=playlist.name,
            type=playlist.type.value,
            link=playlist.link.value,
        )

    def to_domain(self) -> PlaylistEntity:
        return PlaylistEntity(
            id=UUID(str(self.id)),
            course_run_id=UUID(str(self.course_run_id)),
            name=self.name,
            type=VideoResourceType(self.type),
            link=LinkValueObject(self.link),
        )
