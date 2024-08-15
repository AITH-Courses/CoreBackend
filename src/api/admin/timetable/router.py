from fastapi import status, APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.api.admin.timetable.dependencies import get_admin_timetable_command_service
from src.api.admin.courses.dependencies import get_admin
from src.api.admin.timetable.schemas import TimetableDTO, CreateRuleResponse, CreateOrUpdateRuleRequest
from src.api.auth.schemas import UserDTO
from src.api.base_schemas import ErrorResponse, SuccessResponse
from src.domain.timetable.exceptions import TimetableNotFoundError, RuleNotFoundError, IncorrectRuleTypeError
from src.services.timetable.command_service import TimetableCommandService

router = APIRouter(prefix="/admin/courses/{course_id}/runs/{course_run_id}/timetable", tags=["admin"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Get timetable for course run",
    summary="Get timetable",
    responses={
        status.HTTP_200_OK: {
            "model": TimetableDTO,
            "description": "Get timetable",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=TimetableDTO,
)
async def get_timetable(
    course_id: str,
    course_run_id: str,
    _: UserDTO = Depends(get_admin),
    command_service: TimetableCommandService = Depends(get_admin_timetable_command_service),
) -> JSONResponse:
    """Get timetable.

    :return:
    """
    try:
        timetable = await command_service.get_timetable_by_course_run_id(course_run_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=TimetableDTO.from_domain(timetable).model_dump(mode="json"),
        )
    except TimetableNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post(
    "/{timetable_id}/rules",
    status_code=status.HTTP_201_CREATED,
    description="Create rule",
    summary="Create rule",
    responses={
        status.HTTP_201_CREATED: {
            "model": CreateRuleResponse,
            "description": "Rule has been created",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
    },
    response_model=CreateRuleResponse,
)
async def create_rule(
    course_id: str,
    course_run_id: str,
    timetable_id: str,
    data: CreateOrUpdateRuleRequest = Body(),
    _: UserDTO = Depends(get_admin),
    command_service: TimetableCommandService = Depends(get_admin_timetable_command_service),
) -> JSONResponse:
    """Create rule.

    :return:
    """
    try:
        if data.type == "day":
            rule_id = await command_service.create_day_rule(
                timetable_id, data.rule.start_time, data.rule.end_time, data.rule.date
            )
        elif data.type == "week":
            rule_id = await command_service.create_week_rule(
                timetable_id, data.rule.start_time, data.rule.end_time,
                data.rule.start_period_date, data.rule.end_period_date, data.rule.weekdays
            )
        else:
            raise IncorrectRuleTypeError
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=CreateRuleResponse(rule_id=rule_id).model_dump(),
        )
    except (AttributeError, IncorrectRuleTypeError):
        return JSONResponse(
            content=ErrorResponse(message=IncorrectRuleTypeError().message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.delete(
    "/{timetable_id}/rules/{rule_id}",
    status_code=status.HTTP_200_OK,
    description="Delete rule",
    summary="Delete rule",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Rule run has been deleted",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Error",
        },
    },
    response_model=SuccessResponse,
)
async def delete_rule(
    course_id: str,
    course_run_id: str,
    timetable_id: str,
    rule_id: str,
    _: UserDTO = Depends(get_admin),
    command_service: TimetableCommandService = Depends(get_admin_timetable_command_service),
) -> JSONResponse:
    """Delete rule.

    :return:
    """
    try:
        await command_service.delete_rule(rule_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(message="Правило успешно удалено").model_dump(),
        )
    except RuleNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.put(
    "/{timetable_id}/rules/{rule_id}",
    status_code=status.HTTP_200_OK,
    description="Update rule",
    summary="Update rule",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Rule run has been updated",
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
async def update_rule(
    course_id: str,
    course_run_id: str,
    timetable_id: str,
    rule_id: str,
    data: CreateOrUpdateRuleRequest = Body(),
    _: UserDTO = Depends(get_admin),
    command_service: TimetableCommandService = Depends(get_admin_timetable_command_service),
) -> JSONResponse:
    """Update rule.

    :return:
    """
    try:
        if data.type == "day":
            await command_service.update_day_rule(
                rule_id, timetable_id, data.rule.start_time, data.rule.end_time, data.rule.date
            )
        elif data.type == "week":
            await command_service.update_week_rule(
                rule_id, timetable_id, data.rule.start_time, data.rule.end_time,
                data.rule.start_period_date, data.rule.end_period_date, data.rule.weekdays
            )
        else:
            raise IncorrectRuleTypeError
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=SuccessResponse(message="Правило успешно обновлено").model_dump(),
        )
    except RuleNotFoundError as ex:
        return JSONResponse(
            content=ErrorResponse(message=ex.message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except (AttributeError, IncorrectRuleTypeError):
        return JSONResponse(
            content=ErrorResponse(message=IncorrectRuleTypeError().message).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND,
        )
