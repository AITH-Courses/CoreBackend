from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.admin.playlists.dependencies import get_playlist_service
from src.api.admin.playlists.schemas import PlaylistDTO
from src.api.base_schemas import ErrorResponse
from src.api.timetable.schemas import TimetableDTO
from src.domain.course_run.exceptions import NoActualCourseRunError
from src.services.playlists.command_service import PlaylistCommandService

router = APIRouter(prefix="/courses/{course_id}", tags=["courses"])


@router.get(
    "/playlists",
    status_code=status.HTTP_200_OK,
    description="Get actual playlists for course",
    summary="Get actual playlists",
    responses={
        status.HTTP_200_OK: {
            "model": list[TimetableDTO],
            "description": "Get actual playlists for course",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No actual course run",
        },
    },
    response_model=list[TimetableDTO],
)
async def get_playlists_for_course(
    course_id: str,
    command_service: PlaylistCommandService = Depends(get_playlist_service),
) -> JSONResponse:
    """Delete course run.

    :return:
    """
    try:
        playlists = await command_service.get_actual_playlists(course_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[PlaylistDTO.from_domain(p).model_dump(mode="json") for p in playlists],
        )
    except NoActualCourseRunError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
