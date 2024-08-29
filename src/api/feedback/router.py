from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from src.api.auth.dependencies import get_user, get_user_or_anonym
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.api.feedback.dependencies import get_feedback_command_service, get_feedback_query_service
from src.api.feedback.schemas import CreateFeedbackRequest, CreateFeedbackResponse, FeedbackDTO, VoteDTO
from src.domain.courses.exceptions import EmptyPropertyError, ValueDoesntExistError
from src.domain.feedback.exceptions import (
    FeedbackBelongsToAnotherUserError,
    FeedbackLikeError,
    FeedbackNotFoundError,
    OnlyOneFeedbackForCourseError,
)

if TYPE_CHECKING:
    from src.domain.auth.entities import UserEntity
    from src.services.feedback.command_service import FeedbackCommandService
    from src.services.feedback.query_service import FeedbackQueryService


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "/{course_id}/feedbacks",
    status_code=status.HTTP_200_OK,
    description="Get feedback information about course",
    summary="Get feedbacks for course",
    responses={
        status.HTTP_200_OK: {
            "model": list[FeedbackDTO],
            "description": "Feedbacks for one course",
        },
    },
    response_model=list[FeedbackDTO],
)
async def get_feedbacks(
    course_id: str,
    user: UserEntity | None = Depends(get_user_or_anonym),
    query_service:  FeedbackQueryService = Depends(get_feedback_query_service),
) -> list[FeedbackDTO]:
    """Get feedbacks.

    :param user:
    :param course_id:
    :param query_service:
    :return:
    """
    feedbacks = await query_service.get_feedbacks_by_course_id(course_id)

    return [FeedbackDTO.from_domain(feedback, None if user is None else user.id.value) for feedback in feedbacks]


@router.post(
    "/{course_id}/feedbacks",
    status_code=status.HTTP_201_CREATED,
    description="Create feedback for course",
    summary="Create feedback",
    responses={
        status.HTTP_201_CREATED: {
            "model": list[FeedbackDTO],
            "description": "Feedbacks for one course",
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
    response_model=CreateFeedbackResponse,
)
async def create_feedback(
    course_id: str,
    data: CreateFeedbackRequest = Body(),
    user: UserEntity = Depends(get_user),
    command_service:  FeedbackCommandService = Depends(get_feedback_command_service),
    query_service:  FeedbackQueryService = Depends(get_feedback_query_service),
) -> JSONResponse:
    """Create feedback.

    :param course_id:
    :param data:
    :param user:
    :param command_service:
    :param query_service:
    :return:
    """
    try:
        feedback_id = await command_service.create_feedback(course_id, user.id.value, data.text, data.rating)
        await query_service.invalidate_course(course_id)
        return JSONResponse(
            content=CreateFeedbackResponse(feedback_id=feedback_id).model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except (EmptyPropertyError, ValueDoesntExistError) as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except OnlyOneFeedbackForCourseError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.delete(
    "/{course_id}/feedbacks/{feedback_id}",
    status_code=status.HTTP_200_OK,
    description="Delete feedback for course",
    summary="Delete feedback",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Feedback has been deleted",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=SuccessResponse,
)
async def delete_feedback(
    course_id: str,
    feedback_id: str,
    user: UserEntity = Depends(get_user),
    command_service:  FeedbackCommandService = Depends(get_feedback_command_service),
    query_service:  FeedbackQueryService = Depends(get_feedback_query_service),
) -> JSONResponse:
    """Delete feedback.

    :param course_id:
    :param feedback_id:
    :param user:
    :param command_service:
    :param query_service:
    :return:
    """
    try:
        await command_service.delete_feedback(feedback_id, user.id.value)
        await query_service.invalidate_course(course_id)
        return JSONResponse(
            content=SuccessResponse(message="Отзыв успешно удален").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except FeedbackNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except FeedbackBelongsToAnotherUserError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_403_FORBIDDEN,
        )


@router.delete(
    "/{course_id}/feedbacks/{feedback_id}/vote",
    status_code=status.HTTP_200_OK,
    description="Unvote feedback for course",
    summary="Unvote feedback",
    responses={
        status.HTTP_200_OK: {
            "model": list[FeedbackDTO],
            "description": "Feedback loss estimating",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=SuccessResponse,
)
async def unvote_feedback(
    course_id: str,
    feedback_id: str,
    user: UserEntity = Depends(get_user),
    command_service:  FeedbackCommandService = Depends(get_feedback_command_service),
    query_service:  FeedbackQueryService = Depends(get_feedback_query_service),
) -> JSONResponse:
    """Unvote feedback.

    :param course_id:
    :param feedback_id:
    :param user:
    :param command_service:
    :param query_service:
    :return:
    """
    try:
        await command_service.unvote(feedback_id, user.id.value)
        await query_service.invalidate_course(course_id)
        return JSONResponse(
            content=SuccessResponse(message="Оценка с отзыва убрана").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except FeedbackNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except FeedbackLikeError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except ValueDoesntExistError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@router.post(
    "/{course_id}/feedbacks/{feedback_id}/vote",
    status_code=status.HTTP_201_CREATED,
    description="Vote feedback for course",
    summary="Vote feedback",
    responses={
        status.HTTP_201_CREATED: {
            "model": SuccessResponse,
            "description": "Feedback is rated",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=SuccessResponse,
)
async def vote_feedback(
    course_id: str,
    feedback_id: str,
    data: VoteDTO = Body(),
    user: UserEntity = Depends(get_user),
    command_service:  FeedbackCommandService = Depends(get_feedback_command_service),
    query_service:  FeedbackQueryService = Depends(get_feedback_query_service),
) -> JSONResponse:
    """Add vote for feedback.

    :param course_id:
    :param feedback_id:
    :param data:
    :param user:
    :param command_service:
    :param query_service:
    :return:
    """
    try:
        await command_service.vote(feedback_id, user.id.value, data.vote_type)
        await query_service.invalidate_course(course_id)
        return JSONResponse(
            content=SuccessResponse(message="Оценка отзыва выполнена").model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except FeedbackNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except FeedbackLikeError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except ValueDoesntExistError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
