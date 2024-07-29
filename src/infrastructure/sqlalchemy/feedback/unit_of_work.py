from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlalchemy.feedback.repository import SQLAlchemyFeedbackRepository
from src.services.feedback.unit_of_work import FeedbackUnitOfWork


class SQLAlchemyFeedbackUnitOfWork(FeedbackUnitOfWork):

    """SQLA implementation for unit of work."""

    def __init__(self, sqla_session: AsyncSession) -> None:
        self.session = sqla_session
        self.feedback_repo = SQLAlchemyFeedbackRepository(sqla_session)

    async def begin(self) -> None:
        await self.session.begin()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
