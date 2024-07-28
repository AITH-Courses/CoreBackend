from abc import ABC, abstractmethod

from src.domain.feedback.feedback_repository import IFeedbackRepository


class FeedbackUnitOfWork(ABC):

    """Base class implemented pattern Unit of Work."""

    feedback_repo: IFeedbackRepository

    @abstractmethod
    async def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
