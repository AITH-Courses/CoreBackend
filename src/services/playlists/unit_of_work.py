from abc import ABC

from src.domain.playlists.playlist_repository import IPlaylistRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class PlaylistUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    playlist_repo: IPlaylistRepository
