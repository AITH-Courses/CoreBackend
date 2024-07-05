from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserWithEmailExistsError, UserNotFoundError
from src.domain.auth.user_repository import UserRepository
from src.domain.auth.value_objects import Email, UserRole, PartOfName
from src.infrastructure.sqlalchemy.users.models import User


class SQLAlchemyUserRepository(UserRepository):
    """SqlAlchemy implementation of Repository for User."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserEntity) -> None:
        user_ = User(
            id=str(user.id),
            firstname=user.firstname.value,
            lastname=user.lastname.value,
            role=user.role.value,
            email=user.email.value,
            hashed_password=user.hashed_password,
        )
        self.session.add(user_)

    async def update(self, user: UserEntity) -> None:
        result = await self.session.execute(select(User).filter_by(id=user.id))
        user_ = result.scalars().one()
        user_.firstname = user.firstname.value
        user_.lastname = user.lastname.value
        user_.email = user.email.value
        user_.hashed_password = user.hashed_password

    async def delete(self, user_id: str) -> None:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        user_ = result.scalars().one()
        await self.session.delete(user_)

    async def get_by_id(self, user_id: str) -> UserEntity:
        return await self.get_by_field(id=user_id)

    async def get_by_email(self, email: Email) -> UserEntity:
        return await self.get_by_field(email=email.value)

    async def get_by_field(self, **kwargs):
        try:
            result = await self.session.execute(select(User).filter_by(**kwargs))
            user_ = result.scalars().one()
            return UserEntity(
                id=str(user_.id),
                firstname=PartOfName(user_.firstname),
                lastname=PartOfName(user_.lastname),
                role=UserRole(user_.role),
                email=Email(user_.email),
                hashed_password=user_.hashed_password,
            )
        except NoResultFound:
            raise UserNotFoundError
