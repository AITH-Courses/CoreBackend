from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.talent_profile.repository import SQLAlchemyTalentProfileRepository
from src.infrastructure.sqlalchemy.users.repository import SQLAlchemyUserRepository
from src.services.auth.unit_of_work import AuthUnitOfWork


class SQLAlchemyAuthUnitOfWork(AuthUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        self.session = sqla_session
        self.user_repo = SQLAlchemyUserRepository(sqla_session)
        self.profile_repo = SQLAlchemyTalentProfileRepository(sqla_session)

    async def begin(self) -> None:
        await self.session.begin()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
