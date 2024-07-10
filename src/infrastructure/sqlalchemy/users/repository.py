from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserNotFoundError
from src.domain.auth.user_repository import IUserRepository
from src.domain.auth.value_objects import Email
from src.infrastructure.sqlalchemy.users.models import User


class SQLAlchemyUserRepository(IUserRepository):

    """SqlAlchemy implementation of Repository for User."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: UserEntity) -> None:
        user_ = User.from_domain(user)
        self.session.add(user_)

    async def update(self, user: UserEntity) -> None:
        user_ = await self.__get_by_field(id=user.id)
        user_.firstname = user.firstname.value
        user_.lastname = user.lastname.value
        user_.email = user.email.value
        user_.hashed_password = user.hashed_password

    async def delete(self, user_id: str) -> None:
        user_ = await self.__get_by_field(id=user_id)
        await self.session.delete(user_)

    async def get_by_id(self, user_id: str) -> UserEntity:
        user = await self.__get_by_field(id=user_id)
        return user.to_domain()

    async def get_by_email(self, email: Email) -> UserEntity:
        user = await self.__get_by_field(email=email.value)
        return user.to_domain()

    async def __get_by_field(self, **kwargs) -> User:
        try:
            result = await self.session.execute(select(User).filter_by(**kwargs))
            return result.scalars().one()
        except NoResultFound:
            raise UserNotFoundError from NoResultFound
