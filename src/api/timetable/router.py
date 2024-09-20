from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.admin.course_run.dependencies import get_admin_course_run_command_service
from src.api.base_schemas import ErrorResponse
from src.api.timetable.schemas import TimetableDTO
from src.domain.course_run.exceptions import NoActualCourseRunError
from src.domain.timetable.exceptions import NoActualTimetableError
from src.services.course_run.command_service import CourseRunCommandService

router = APIRouter(prefix="/courses/{course_id}", tags=["courses"])


@router.get(
    "/timetable",
    status_code=status.HTTP_200_OK,
    description="Get actual timetable for course",
    summary="Get actual timetable",
    responses={
        status.HTTP_200_OK: {
            "model": TimetableDTO,
            "description": "Get actual timetable for course",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=TimetableDTO,
)
async def get_timetable_for_course(
    course_id: str,
    command_service: CourseRunCommandService = Depends(get_admin_course_run_command_service),
) -> JSONResponse:
    """Delete course run.

    :return:
    """
    try:
        timetable, course_run, google_calendar_groups = await command_service.get_actual_timetable_by_id(course_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=TimetableDTO.from_domain(
                timetable, course_run.name.value, google_calendar_groups,
            ).model_dump(mode="json"),
        )
    except (NoActualTimetableError, NoActualCourseRunError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
