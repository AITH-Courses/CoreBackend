from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.base_unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.sqlalchemy.talent_profile.repository import SQLAlchemyTalentProfileRepository
from src.infrastructure.sqlalchemy.users.repository import SQLAlchemyUserRepository
from src.services.talent_profile.unit_of_work import TalentProfileUnitOfWork


class SQLAlchemyTalentProfileUnitOfWork(SQLAlchemyUnitOfWork, TalentProfileUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        super().__init__(sqla_session)
        self.user_repo = SQLAlchemyUserRepository(sqla_session)
        self.profile_repo = SQLAlchemyTalentProfileRepository(sqla_session)
