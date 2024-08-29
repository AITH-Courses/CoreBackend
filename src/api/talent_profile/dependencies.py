from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Depends

from src.infrastructure.sqlalchemy.session import get_async_session
from src.infrastructure.sqlalchemy.talent_profile.unit_of_work import SQLAlchemyTalentProfileUnitOfWork
from src.services.talent_profile.command_service import TalentProfileCommandService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def get_talent_profile_service(
        db_session: AsyncSession = Depends(get_async_session),
) -> TalentProfileCommandService:
    """Get auth service on sessions.

    :param db_session:
    :return:
    """
    unit_of_work = SQLAlchemyTalentProfileUnitOfWork(db_session)
    return TalentProfileCommandService(unit_of_work)
