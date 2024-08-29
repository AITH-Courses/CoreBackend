from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from src.api.auth.dependencies import get_auth_service, get_auth_token, get_user
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.api.talent_profile.dependencies import get_talent_profile_service
from src.api.talent_profile.schemas import ProfileGeneralUpdateRequest, ProfileLinksUpdateRequest, TalentProfileDTO
from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import (
    EmptyPartOfNameError,
)
from src.domain.auth.value_objects import PartOfName
from src.domain.base_exceptions import InvalidLinkError
from src.domain.talent_profile.exceptions import (
    TalentProfileAlreadyExistsError,
    TalentProfileForOnlyTalentError,
    TalentProfileNotFoundError,
)
from src.services.auth.command_service import AuthCommandService
from src.services.talent_profile.command_service import TalentProfileCommandService

router = APIRouter(prefix="/talent", tags=["talent"])


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    description="Get profile of current user talent",
    summary="Getting profile",
    responses={
        status.HTTP_200_OK: {
            "model": TalentProfileDTO,
            "description": "Getting profile for current user is successful",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No profile",
        },
    },
    response_model=TalentProfileDTO,
)
async def get_current_user(
        user: UserEntity = Depends(get_user),
        profile_service: TalentProfileCommandService = Depends(get_talent_profile_service),
) -> JSONResponse:
    """Get current user on auth token.

    :param profile_service:
    :param user:
    :return:
    """
    try:
        profile = await profile_service.get_profile(user.id.value)
    except TalentProfileNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return JSONResponse(
        content=TalentProfileDTO.from_entity(profile, user.firstname.value, user.lastname.value).model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.put(
    "/profile/general",
    status_code=status.HTTP_200_OK,
    description="Update general part in profile",
    summary="Update profile",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Profile has been updated",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No profile",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "invalid data",
        },
    },
    response_model=SuccessResponse,
)
async def update_profile_general(
        user: UserEntity = Depends(get_user),
        auth_token: str = Depends(get_auth_token),
        data: ProfileGeneralUpdateRequest = Body(),
        profile_service: TalentProfileCommandService = Depends(get_talent_profile_service),
        auth_service: AuthCommandService = Depends(get_auth_service),
) -> JSONResponse:
    """Update general part of profile.

    :param auth_service:
    :param auth_token:
    :param data:
    :param profile_service:
    :param user:
    :return:
    """
    try:
        await profile_service.update_profile(
            user.id.value, data.firstname, data.lastname,
            data.image_url, data.location, data.position, data.company,
        )
        if data.firstname != user.firstname or data.lastname != user.lastname:
            user.firstname = PartOfName(data.firstname)
            user.lastname = PartOfName(data.lastname)
            await auth_service.session_service.update(auth_token, user)
    except TalentProfileNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except EmptyPartOfNameError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return JSONResponse(
        content=SuccessResponse(message="Профиль успешно обновлен").model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.put(
    "/profile/links",
    status_code=status.HTTP_200_OK,
    description="Update links part in profile",
    summary="Update links",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Profile has been updated",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "No profile",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "invalid data",
        },
    },
    response_model=SuccessResponse,
)
async def update_profile_links(
        user: UserEntity = Depends(get_user),
        data: ProfileLinksUpdateRequest = Body(),
        profile_service: TalentProfileCommandService = Depends(get_talent_profile_service),
) -> JSONResponse:
    """Update general part of profile.

    :param data:
    :param profile_service:
    :param user:
    :return:
    """
    try:
        await profile_service.update_links(
            user.id.value, data.link_ru_resume, data.link_eng_resume,
            data.link_tg_personal, data.link_linkedin,
        )
    except TalentProfileNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except InvalidLinkError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return JSONResponse(
        content=SuccessResponse(message="Ссылки в профиле успешно обновлены").model_dump(),
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/profile",
    status_code=status.HTTP_201_CREATED,
    description="Create profile",
    summary="Create profile",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Profile has been created",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Error",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "No rights",
        },
    },
    response_model=SuccessResponse,
)
async def create_profile(
        user: UserEntity = Depends(get_user),
        profile_service: TalentProfileCommandService = Depends(get_talent_profile_service),
) -> JSONResponse:
    """Update general part of profile.

    :param profile_service:
    :param user:
    :return:
    """
    try:
        await profile_service.create_profile(user.id.value, user.role.value)
    except TalentProfileForOnlyTalentError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_403_FORBIDDEN,
        )
    except TalentProfileAlreadyExistsError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content=SuccessResponse(message="Профиль успешно создан").model_dump(),
        status_code=status.HTTP_200_OK,
    )
