from abc import ABC

from src.domain.playlists.playlist_repository import IPlaylistRepository
from src.domain.course_run.course_run_repository import ICourseRunRepository
from src.services.base_unit_of_work import ServiceUnitOfWork


class PlaylistUnitOfWork(ServiceUnitOfWork, ABC):

    """Base class implemented pattern Unit of Work."""

    playlist_repo: IPlaylistRepository
    course_run_repo: ICourseRunRepository
