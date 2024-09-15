from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse

from src.api.admin.courses.dependencies import get_admin
from src.api.admin.group_google_calendar.dependencies import get_group_google_calendar_service
from src.api.admin.group_google_calendar.schemas import UpdateManyGroupGoogleCalendarMessage, \
    UpdateManyGroupGoogleCalendarsRequest
from src.domain.auth.entities import UserEntity
from src.services.group_google_calendar.command_service import GroupGoogleCalendarCommandService
from src.services.group_google_calendar.dto import UpdateGroupGoogleCalendarDTO, UpdateGroupDTO

router = APIRouter(prefix="/integrations/google_calendar_links", tags=["integrations"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    description="Add google calendar links for many courses. The group name is optional, it is required if there is "
                "more than one group",
    summary="Add google calendar links",
    responses={
        status.HTTP_200_OK: {
            "model": list[UpdateManyGroupGoogleCalendarMessage],
            "description": "Messages explained processing. OK is standard message after success processing",
        },
    },
    response_model=list[UpdateManyGroupGoogleCalendarMessage],
)
async def update_google_calendar_links(
    _: UserEntity = Depends(get_admin),
    data: UpdateManyGroupGoogleCalendarsRequest = Body(),
    command_service: GroupGoogleCalendarCommandService = Depends(get_group_google_calendar_service),
) -> JSONResponse:
    """Update google calendar links.

    :return:
    """
    courses = [
        UpdateGroupGoogleCalendarDTO(c.name, [UpdateGroupDTO(g.name, g.link) for g in c.groups])
        for c in data.courses]
    messages = await command_service.update_many(courses, data.course_run_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[UpdateManyGroupGoogleCalendarMessage(message=msg).model_dump(mode="json") for msg in messages]
    )
