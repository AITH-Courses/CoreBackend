from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.api.base_pagination import PaginationError, Paginator
from src.api.base_schemas import ErrorResponse
from src.api.courses.dependencies import get_talent_courses_query_service
from src.api.courses.schemas import CourseFullDTO, CourseShortDTO, CoursesPaginationResponse
from src.domain.courses.entities import CourseEntity
from src.domain.courses.exceptions import CourseNotFoundError
from src.services.courses.query_service_for_talent import CourseFilter

if TYPE_CHECKING:
    from src.services.courses.query_service_for_talent import TalentCourseQueryService

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Get all available courses",
    summary="Get courses",
    responses={
        status.HTTP_200_OK: {
            "model": list[CourseShortDTO],
            "description": "All courses",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error with page",
        },
    },
    response_model=list[CourseShortDTO],
)
async def get_courses(
    terms: list[str] = Query(None),
    roles: list[str] = Query(None),
    implementers: list[str] = Query(None),
    formats: list[str] = Query(None),
    page: int = Query(1),
    query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Get courses.

    :param page:
    :param terms:
    :param roles:
    :param implementers:
    :param formats:
    :param query_service:
    :return:
    """
    filters = CourseFilter(terms=terms, roles=roles, implementers=implementers, formats=formats)
    courses = await query_service.get_courses(filters)
    paginator = Paginator[CourseEntity](data=courses, page_size=12)
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=CoursesPaginationResponse(
                courses=[CourseShortDTO.from_domain(course) for course in paginator.get_data_by_page(page)],
                max_page=paginator.pages[-1],
            ).model_dump(),
        )
    except PaginationError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


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
