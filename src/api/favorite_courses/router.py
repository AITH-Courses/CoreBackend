from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from src.api.auth.dependencies import get_user
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.api.courses.dependencies import get_talent_courses_query_service
from src.api.favorite_courses.dependencies import get_favorite_courses_command_service
from src.api.favorite_courses.schemas import AddFavoriteCourseRequest, FavoriteCourseDTO
from src.domain.favorite_courses.exceptions import (
    CourseAlreadyExistsInFavoritesError,
    CourseDoesntExistInFavoritesError,
)
from src.services.courses.query_service_for_talent import CourseFilter

if TYPE_CHECKING:
    from src.domain.auth.entities import UserEntity
    from src.services.courses.query_service_for_talent import TalentCourseQueryService
    from src.services.favorite_courses.command_service import FavoriteCoursesCommandService

router = APIRouter(prefix="/talent/profile/favorites", tags=["talent"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Get all favorite courses",
    summary="Get favorites",
    responses={
        status.HTTP_200_OK: {
            "model": list[FavoriteCourseDTO],
            "description": "All favorites",
        },
    },
    response_model=list[FavoriteCourseDTO],
)
async def get_favorite_courses(
    user: UserEntity = Depends(get_user),
    favorites_command_service: FavoriteCoursesCommandService = Depends(get_favorite_courses_command_service),
    query_service: TalentCourseQueryService = Depends(get_talent_courses_query_service),
) -> JSONResponse:
    """Get favorite courses.

    :param user:
    :param favorites_command_service:
    :param query_service:
    :return:
    """
    favorites = await favorites_command_service.get_favorite_courses(user.id.value)
    courses = await query_service.get_courses(CourseFilter())
    courses = {course.id: course for course in courses}
    results = []
    for favorite in favorites:
        if favorite.course_id not in courses:
            continue
        favorite_dto = FavoriteCourseDTO.from_domain(courses[favorite.course_id], favorite)
        results.append(favorite_dto.model_dump())
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=results,
    )


@router.delete(
    "/{favorite_course_id}",
    status_code=status.HTTP_200_OK,
    description="Delete course from favorites",
    summary="Delete favorite",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Course has been removed from favorites",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No course with this id",
        },
    },
    response_model=SuccessResponse,
)
async def remove_course_from_favorites(
    favorite_course_id: str,
    _: UserEntity = Depends(get_user),
    favorites_command_service: FavoriteCoursesCommandService = Depends(get_favorite_courses_command_service),
) -> JSONResponse:
    """Get courses.

    :param _:
    :param favorite_course_id:
    :param favorites_command_service:
    :return:
    """
    try:
        await favorites_command_service.remove_course_from_favorites(favorite_course_id)
        return JSONResponse(
            content=SuccessResponse(message="Курс успешно убран из избранного").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except CourseDoesntExistInFavoritesError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Add to favorites",
    summary="Add favorite course",
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse,
            "description": "Course has been added to favorites",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error with course",
        },
    },
    response_model=SuccessResponse,
)
async def add_course_to_favorites(
    data: AddFavoriteCourseRequest = Body(),
    user: UserEntity = Depends(get_user),
    favorites_command_service: FavoriteCoursesCommandService = Depends(get_favorite_courses_command_service),
) -> JSONResponse:
    """Get courses.

    :param user:
    :param data:
    :param favorites_command_service:
    :return:
    """
    try:
        await favorites_command_service.add_course_to_favorites(user.id.value, data.course_id)
        return JSONResponse(
            content=SuccessResponse(message="Курс успешно добавлен в избранное").model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except CourseAlreadyExistsInFavoritesError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
