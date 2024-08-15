from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from src.api.admin.course_run.dependencies import get_admin_course_run_command_service
from src.api.admin.course_run.schemas import CourseRunDTO, CreateCourseRunRequest, CreateCourseRunResponse
from src.api.admin.courses.dependencies import get_admin
from src.api.auth.schemas import UserDTO
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.domain.course_run.exceptions import CourseRunAlreadyExistsError, CourseRunNotFoundError
from src.domain.courses.exceptions import IncorrectCourseRunNameError
from src.services.course_run.command_service import CourseRunCommandService

router = APIRouter(prefix="/admin/courses/{course_id}/runs", tags=["admin"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Get all runs for course",
    summary="Get course runs",
    responses={
        status.HTTP_200_OK: {
            "model": list[CourseRunDTO],
            "description": "All course runs",
        },
    },
    response_model=list[CourseRunDTO],
)
async def get_all_course_runs(
    course_id: str,
    _: UserDTO = Depends(get_admin),
    command_service: CourseRunCommandService = Depends(get_admin_course_run_command_service),
) -> JSONResponse:
    """Get course runs.

    :return:
    """
    course_runs = await command_service.get_all_course_runs_by_id(course_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=([CourseRunDTO.from_domain(run).model_dump() for run in course_runs]),
    )


@router.get(
    "/{course_run_id}",
    status_code=status.HTTP_200_OK,
    description="Get course run",
    summary="Get course run",
    responses={
        status.HTTP_200_OK: {
            "model": list[CourseRunDTO],
            "description": "One course run",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error with page",
        },
    },
    response_model=list[CourseRunDTO],
)
async def get_one_course_run(
    course_id: str,
    course_run_id: str,
    _: UserDTO = Depends(get_admin),
    command_service: CourseRunCommandService = Depends(get_admin_course_run_command_service),
) -> JSONResponse:
    """Get course run.

    :return:
    """
    try:
        course_run = await command_service.get_course_run_by_id(course_run_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=CourseRunDTO.from_domain(course_run).model_dump(),
        )
    except CourseRunNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    description="Create course run",
    summary="Create course run",
    responses={
        status.HTTP_201_CREATED: {
            "model": CreateCourseRunResponse,
            "description": "Course run has been created",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=CreateCourseRunResponse,
)
async def create_course_run(
    course_id: str,
    data: CreateCourseRunRequest = Body(),
    _: UserDTO = Depends(get_admin),
    command_service: CourseRunCommandService = Depends(get_admin_course_run_command_service),
) -> JSONResponse:
    """Create course run.

    :return:
    """
    try:
        course_run_id = await command_service.create_course_run(course_id, data.season, data.year)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=CreateCourseRunResponse(course_run_id=course_run_id).model_dump(),
        )
    except IncorrectCourseRunNameError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except CourseRunAlreadyExistsError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.delete(
    "/{course_run_id}",
    status_code=status.HTTP_200_OK,
    description="Delete course run",
    summary="Delete course run",
    responses={
        status.HTTP_200_OK: {
            "model": CreateCourseRunResponse,
            "description": "Course run has been deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=SuccessResponse,
)
async def delete_course_run(
    course_id: str,
    course_run_id: str,
    _: UserDTO = Depends(get_admin),
    command_service: CourseRunCommandService = Depends(get_admin_course_run_command_service),
) -> JSONResponse:
    """Delete course run.

    :return:
    """
    try:
        await command_service.delete_course_run(course_run_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(message="Запуск курса успешно удален").model_dump(),
        )
    except CourseRunNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
