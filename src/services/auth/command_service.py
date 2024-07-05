import uuid

from sqlalchemy.exc import IntegrityError

from src.domain.auth.constants import TALENT_ROLE
from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserWithEmailExistsError
from src.domain.auth.value_objects import Email, PartOfName, UserRole
from src.infrastructure.security.password_service import PasswordService
from src.services.auth.session_service import SessionService
from src.services.auth.unit_of_work import AuthUnitOfWork


class AuthCommandService:

    """Class implemented CQRS pattern, command class."""

    def __init__(self, uow: AuthUnitOfWork, session_service: SessionService) -> None:
        self.uow = uow
        self.session_service = session_service

    async def register_talent(self, firstname_: str, lastname_: str, email_: str, password_: str) -> str:
        user_id = str(uuid.uuid4())
        firstname = PartOfName(firstname_)
        lastname = PartOfName(lastname_)
        role = UserRole(TALENT_ROLE)
        email = Email(email_)
        PasswordService.validate_password(password_)
        hashed_password = PasswordService.create_hashed_password(password_)
        user = UserEntity(user_id, firstname, lastname, role, email, hashed_password)
        auth_token = str(uuid.uuid4())
        try:
            await self.uow.user_repo.create(user)
            await self.uow.commit()
        except IntegrityError:
            await self.uow.rollback()
            raise UserWithEmailExistsError from IntegrityError
        await self.session_service.set(auth_token, user)
        return auth_token

    async def login(self, email_: str, password_: str) -> str:
        email = Email(email_)
        auth_token = str(uuid.uuid4())
        user = await self.uow.user_repo.get_by_email(email)
        PasswordService.verify_password(password_, user.hashed_password)
        await self.session_service.set(auth_token, user)
        return auth_token

    async def logout(self, auth_token: str) -> None:
        await self.session_service.delete(auth_token)

    async def me(self, auth_token: str) -> UserEntity:
        return await self.session_service.get(auth_token)
