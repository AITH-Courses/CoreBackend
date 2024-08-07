from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.responses import JSONResponse

from src.api.admin.dependencies import get_admin, get_admin_courses_query_service
from src.api.admin.schemas import CreateCourseRequest, CreateCourseResponse, UpdateCourseRequest
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.api.courses.dependencies import get_courses_command_service, get_talent_courses_query_service
from src.api.courses.schemas import CourseFullDTO, CourseShortDTO
from src.domain.courses.exceptions import (
    CourseAlreadyExistsError,
    CourseNotFoundError,
    CoursePublishError,
    EmptyPropertyError,
    IncorrectCourseRunNameError,
    ValueDoesntExistError,
)

if TYPE_CHECKING:
    from src.api.auth.schemas import UserDTO
    from src.services.courses.command_service import CourseCommandService
    from src.services.courses.query_service_for_admin import AdminCourseQueryService
    from src.services.courses.query_service_for_talent import TalentCourseQueryService


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
    _: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    admin_query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
    talent_query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Create course.

    :param admin_query_service:
    :param talent_query_service:
    :param _:
    :param query_service:
    :param data:
    :param command_service:
    :return:
    """
    try:
        course_id = await command_service.create_course(data.name)
        await admin_query_service.course_cache_service.delete_many()
        await talent_query_service.course_cache_service.delete_many()
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
    _: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    admin_query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
    talent_query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Create course.

    :param talent_query_service:
    :param admin_query_service:
    :param _:
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
            assessment_=data.assessment, resources_=[res.model_dump() for res in data.resources],
            extra_=data.extra, author_=data.author,
            implementer_=data.implementer, format_=data.format,
            terms_=data.terms, roles=data.roles,
            periods=data.periods, runs=data.last_runs,
        )
        await admin_query_service.invalidate_course(course_id)
        await talent_query_service.invalidate_course(course_id)
        await admin_query_service.course_cache_service.delete_many()
        await talent_query_service.course_cache_service.delete_many()
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
    _: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    admin_query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
    talent_query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Create course.

    :param talent_query_service:
    :param admin_query_service:
    :param _:
    :param course_id:
    :param command_service:
    :return:
    """
    try:
        await command_service.delete_course(course_id)
        await admin_query_service.invalidate_course(course_id)
        await talent_query_service.invalidate_course(course_id)
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
    _: UserDTO = Depends(get_admin),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> JSONResponse:
    """Get course.

    :param _:
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
    _: UserDTO = Depends(get_admin),
    query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
) -> list[CourseShortDTO]:
    """Get courses.

    :param _:
    :param query_service:
    :return:
    """
    courses = await query_service.get_courses()
    return [CourseShortDTO.from_domain(course) for course in courses]


@router.post(
    "/courses/{course_id}/published",
    status_code=status.HTTP_200_OK,
    description="Publish course",
    summary="Publish course",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Course published",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "No course",
        },
    },
    response_model=SuccessResponse,
)
async def publish_course(
    course_id: str = Path(),
    _: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    admin_query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
    talent_query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Publish course.

    :param talent_query_service:
    :param admin_query_service:
    :param _:
    :param course_id:
    :param command_service:
    :return:
    """
    try:
        await command_service.publish_course(course_id)
        await admin_query_service.invalidate_course(course_id)
        await talent_query_service.invalidate_course(course_id)
        return JSONResponse(
            content=SuccessResponse(message="Course has published").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except CourseNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except CoursePublishError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )


@router.delete(
    "/courses/{course_id}/published",
    status_code=status.HTTP_200_OK,
    description="Hide course",
    summary="Hide course",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Course unpublished",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "No course",
        },
    },
    response_model=SuccessResponse,
)
async def hide_course(
    course_id: str = Path(),
    _: UserDTO = Depends(get_admin),
    command_service: CourseCommandService = Depends(get_courses_command_service),
    admin_query_service: AdminCourseQueryService = Depends(get_admin_courses_query_service),
    talent_query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Hide/unpublish course.

    :param talent_query_service:
    :param admin_query_service:
    :param _:
    :param course_id:
    :param command_service:
    :return:
    """
    try:
        await command_service.hide_course(course_id)
        await admin_query_service.invalidate_course(course_id)
        await talent_query_service.invalidate_course(course_id)
        return JSONResponse(
            content=SuccessResponse(message="Course has unpublished").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except CourseNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except CoursePublishError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_409_CONFLICT,
        )
