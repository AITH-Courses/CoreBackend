from fastapi import APIRouter, Depends, status, Body, Path
from fastapi.responses import JSONResponse

from src.api.admin.dependencies import get_admin, get_admin_courses_query_service
from src.api.admin.schemas import CreateCourseRequest, CreateCourseResponse, UpdateCourseRequest
from src.api.auth.schemas import UserDTO
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.api.courses.dependencies import get_courses_command_service
from src.api.courses.schemas import CourseShortDTO, CourseFullDTO
from src.domain.courses.exceptions import CourseNotFoundError, CourseAlreadyExistsError, EmptyPropertyError, \
    IncorrectCourseRunNameError, ValueDoesntExistError
from src.services.courses.command_service import CourseCommandService
from src.services.courses.query_service_for_admin import AdminCourseQueryService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/courses",
    status_code=status.HTTP_201_CREATED,
    description="Create new course",
    summary="Create course",
    responses={
        status.HTTP_201_CREATED: {
            "model": CreateCourseResponse,
            "description": "Course created",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=CreateCourseResponse,
)
async def create_course(
    data: CreateCourseRequest = Body(),
    admin: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> JSONResponse:
    """Create course.

    :param query_service:
    :param admin:
    :param data:
    :param command_service:
    :return:
    """
    try:
        course_id = await command_service.create_course(data.name)
        await query_service.course_cache_service.delete_one(course_id)
        await query_service.course_cache_service.delete_many()
        return JSONResponse(
            content=CreateCourseResponse(course_id=course_id).model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except CourseAlreadyExistsError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except EmptyPropertyError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.put(
    "/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    description="Update course",
    summary="Update course",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Course updated",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
    },
    response_model=SuccessResponse,
)
async def update_course(
    course_id: str = Path(),
    data: UpdateCourseRequest = Body(),
    admin: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> JSONResponse:
    """Create course.

    :param query_service:
    :param admin:
    :param course_id:
    :param data:
    :param command_service:
    :return:
    """
    try:
        await command_service.update_course(
            course_id=course_id, name_=data.name,
            image_url=data.image_url, limits_=data.limits,
            prerequisites_=data.prerequisites,
            description_=data.description, topics_=data.topics,
            assessment_=data.assessment, resources_=data.resources,
            extra_=data.extra, author_=data.author,
            implementer_=data.implementer, format_=data.format,
            terms_=data.terms, roles=data.roles,
            periods=data.periods, runs=data.last_runs,
        )
        await query_service.course_cache_service.delete_one(course_id)
        await query_service.course_cache_service.delete_many()
        return JSONResponse(
            content=SuccessResponse(message="Course has updated").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except CourseAlreadyExistsError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except (EmptyPropertyError, IncorrectCourseRunNameError, ValueDoesntExistError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except CourseNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.delete(
    "/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    description="Delete course",
    summary="Delete course",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Course deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course",
        },
    },
    response_model=SuccessResponse,
)
async def delete_course(
    course_id: str = Path(),
    admin: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> JSONResponse:
    """Create course.

    :param query_service:
    :param admin:
    :param course_id:
    :param command_service:
    :return:
    """
    try:
        await command_service.delete_course(course_id)
        await query_service.course_cache_service.delete_one(course_id)
        await query_service.course_cache_service.delete_many()
        return JSONResponse(
            content=SuccessResponse(message="Course has deleted").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except CourseNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.get(
    "/courses/{course_id}",
    status_code=status.HTTP_200_OK,
    description="Get course",
    summary="Get course",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Course deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course",
        },
    },
    response_model=SuccessResponse,
)
async def get_course(
    course_id: str = Path(),
    admin: UserDTO = Depends(get_admin),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> JSONResponse:
    """Get course.

    :param admin:
    :param course_id:
    :param query_service:
    :return:
    """
    try:
        course = await query_service.get_course(course_id)
        return JSONResponse(
            content=CourseFullDTO.from_domain(course).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except CourseNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.get(
    "/courses",
    status_code=status.HTTP_200_OK,
    description="Get all courses",
    summary="Get courses",
    responses={
        status.HTTP_200_OK: {
            "model": list[CourseShortDTO],
            "description": "All courses",
        },
    },
    response_model=list[CourseShortDTO],
)
async def get_courses(
    admin: UserDTO = Depends(get_admin),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> list[CourseShortDTO]:
    """Get courses.

    :param admin:
    :param query_service:
    :return:
    """
    courses = await query_service.get_courses()
    return [CourseShortDTO.from_domain(course) for course in courses]

