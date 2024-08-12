from sqlalchemy.ext.asyncio import AsyncSession

from src.services.base_unit_of_work import ServiceUnitOfWork


class SQLAlchemyUnitOfWork(ServiceUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        self.session = sqla_session

    async def begin(self) -> None:
        await self.session.begin()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
