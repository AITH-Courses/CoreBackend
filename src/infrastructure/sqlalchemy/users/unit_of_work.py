from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.users.repository import SQLAlchemyUserRepository
from src.services.auth.unit_of_work import AuthUnitOfWork


class SQLAlchemyAuthUnitOfWork(AuthUnitOfWork):
    def __init__(self, sqla_session: AsyncSession):
        self.session = sqla_session
        self.user_repo = SQLAlchemyUserRepository(sqla_session)

    async def begin(self):
        await self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
