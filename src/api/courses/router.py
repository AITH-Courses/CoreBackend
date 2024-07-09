from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.api.base_schemas import ErrorResponse
from src.api.courses.dependencies import get_talent_courses_query_service
from src.api.courses.schemas import CourseShortDTO, CourseFullDTO
from src.domain.courses.exceptions import CourseNotFoundError
from src.services.courses.query_service_for_talent import TalentCourseQueryService

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all available courses",
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
    query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> list[CourseShortDTO]:
    """Get courses.

    :param query_service:
    :return:
    """
    courses = await query_service.get_courses()
    return [CourseShortDTO.from_domain(course) for course in courses]


@router.get(
    "/{model_id}",
    status_code=status.HTTP_200_OK,
    description="Get full information about course",
    summary="Get course",
    responses={
        status.HTTP_200_OK: {
            "model": CourseFullDTO,
            "description": "One course",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course with this id",
        },
    },
    response_model=CourseFullDTO,
)
async def get_course(
    course_id: str,
    query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Get courses.

    :param course_id:
    :param query_service:
    :return:
    """
    try:
        course = await query_service.get_course(course_id)
        return JSONResponse(
            content=CourseFullDTO.from_domain(course).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except CourseNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
