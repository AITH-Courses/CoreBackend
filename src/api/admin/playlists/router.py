from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from src.api.admin.courses.dependencies import get_admin
from src.api.admin.playlists.dependencies import get_playlist_service
from src.api.admin.playlists.schemas import CreateOrUpdatePlaylistRequest, PlaylistDTO
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.domain.auth.entities import UserEntity
from src.domain.base_exceptions import InvalidLinkError
from src.domain.courses.exceptions import ValueDoesntExistError
from src.domain.playlists.exceptions import PlaylistNotFoundError
from src.services.playlists.command_service import PlaylistCommandService

router = APIRouter(
    prefix="/admin/courses/{course_id}/runs/{course_run_id}/playlists",
    tags=["admin"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Create playlist",
    summary="Create playlist",
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse,
            "description": "Playlist has been created",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Invalid data",
        },
    },
    response_model=SuccessResponse,
)
async def create_group_google_calendar(
    course_id: str,
    course_run_id: str,
    data: CreateOrUpdatePlaylistRequest = Body(),
    _: UserEntity = Depends(get_admin),
    command_service: PlaylistCommandService = Depends(get_playlist_service),
) -> JSONResponse:
    """Create playlist.

    :return:
    """
    try:
        await command_service.create_playlist(course_run_id, data.name, data.type, data.link)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=SuccessResponse(message="Плейлист успешно создан").model_dump(mode="json"),
        )
    except (InvalidLinkError, ValueDoesntExistError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Get playlists by course run",
    summary="Get playlists",
    responses={
        status.HTTP_200_OK: {
            "model": list[PlaylistDTO],
            "description": "Playlists",
        },
    },
    response_model=list[PlaylistDTO],
)
async def get_playlists(
    course_id: str,
    course_run_id: str,
    _: UserEntity = Depends(get_admin),
    command_service: PlaylistCommandService = Depends(get_playlist_service),
) -> JSONResponse:
    """Get google calendar links.

    :return:
    """
    playlists = await command_service.get_playlists_by_course_run_id(course_run_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[PlaylistDTO.from_domain(p).model_dump(mode="json") for p in playlists],
    )


@router.delete(
    "/{playlist_id}",
    status_code=status.HTTP_200_OK,
    description="Delete playlist",
    summary="Delete playlist",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Playlist has been deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No such playlist",
        },
    },
    response_model=SuccessResponse,
)
async def delete_playlist(
    course_id: str,
    course_run_id: str,
    playlist_id: str,
    _: UserEntity = Depends(get_admin),
    command_service: PlaylistCommandService = Depends(get_playlist_service),
) -> JSONResponse:
    """Delete playlist.

    :return:
    """
    try:
        await command_service.delete_playlist(playlist_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(message="Плейлист успешно удален").model_dump(mode="json"),
        )
    except PlaylistNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.put(
    "/{playlist_id}",
    status_code=status.HTTP_200_OK,
    description="Update playlist",
    summary="Update playlist",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Playlist has been updated",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No such playlist",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Invalid data",
        },
    },
    response_model=SuccessResponse,
)
async def update_playlist(
    course_id: str,
    course_run_id: str,
    playlist_id: str,
    data: CreateOrUpdatePlaylistRequest = Body(),
    _: UserEntity = Depends(get_admin),
    command_service: PlaylistCommandService = Depends(get_playlist_service),
) -> JSONResponse:
    """Update playlist.

    :return:
    """
    try:
        await command_service.update_playlist(playlist_id, course_run_id, data.name, data.type, data.link)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(message="Плейлист успешно обновлен").model_dump(mode="json"),
        )
    except PlaylistNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except (InvalidLinkError, ValueDoesntExistError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
