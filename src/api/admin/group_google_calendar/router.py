from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse

from src.api.admin.courses.dependencies import get_admin
from src.api.admin.group_google_calendar.dependencies import get_group_google_calendar_service
from src.api.admin.group_google_calendar.schemas import CreateGroupGoogleCalendarRequest
from src.api.base_schemas import SuccessResponse, ErrorResponse
from src.api.timetable.schemas import GroupGoogleCalendarDTO
from src.domain.auth.entities import UserEntity
from src.domain.base_exceptions import InvalidLinkError
from src.domain.group_google_calendar.exceptions import GroupGoogleCalendarNotFoundError
from src.services.group_google_calendar.command_service import GroupGoogleCalendarCommandService

router = APIRouter(prefix="/admin/courses/{course_id}/runs/{course_run_id}/timetable/google_calendar_groups", tags=["admin"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Create google calendar link",
    summary="Create google calendar link",
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse,
            "description": "Google calendar has been created",
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
    data: CreateGroupGoogleCalendarRequest = Body(),
    _: UserEntity = Depends(get_admin),
    command_service: GroupGoogleCalendarCommandService = Depends(get_group_google_calendar_service),
) -> JSONResponse:
    """Create google calendar link.

    :return:
    """
    try:
        await command_service.create(course_run_id, data.name, data.link)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=SuccessResponse(message="Ссылка на google calendar успешно создана").model_dump(mode="json")
        )
    except InvalidLinkError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Get google calendar links by course run",
    summary="Get google calendar links",
    responses={
        status.HTTP_200_OK: {
            "model": list[GroupGoogleCalendarDTO],
            "description": "Google calendar has been deleted",
        }
    },
    response_model=list[GroupGoogleCalendarDTO],
)
async def get_group_google_calendars(
    course_id: str,
    course_run_id: str,
    _: UserEntity = Depends(get_admin),
    command_service: GroupGoogleCalendarCommandService = Depends(get_group_google_calendar_service),
) -> JSONResponse:
    """Get google calendar links.

    :return:
    """
    groups = await command_service.get_groups(course_run_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[GroupGoogleCalendarDTO.from_domain(g).model_dump(mode="json") for g in groups]
    )


@router.delete(
    "/{group_google_calendar_id}",
    status_code=status.HTTP_200_OK,
    description="Delete google calendar link",
    summary="Delete google calendar link",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Google calendar has been deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Google calendar has been created",
        },
    },
    response_model=SuccessResponse,
)
async def delete_group_google_calendar(
    course_id: str,
    course_run_id: str,
    group_google_calendar_id: str,
    _: UserEntity = Depends(get_admin),
    command_service: GroupGoogleCalendarCommandService = Depends(get_group_google_calendar_service),
) -> JSONResponse:
    """Delete google calendar link.

    :return:
    """
    try:
        await command_service.delete(group_google_calendar_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(message="Ссылка на google calendar успешно удалена").model_dump(mode="json")
        )
    except GroupGoogleCalendarNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
