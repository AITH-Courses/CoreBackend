from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.domain.playlists.entities import PlaylistEntity


class PlaylistDTO(BaseModel):

    """Schema for playlist."""

    id: str
    name: str
    type: str
    link: str

    @staticmethod
    def from_domain(playlist: PlaylistEntity) -> PlaylistDTO:
        return PlaylistDTO(
            id=playlist.id.value,
            name=playlist.name,
            type=playlist.type.value,
            link=playlist.link.value,
        )


class CreateOrUpdatePlaylistRequest(BaseModel):

    """Schema for creating or updating playlist."""

    name: str
    type: str
    link: str
