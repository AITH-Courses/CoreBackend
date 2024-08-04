import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserNotFoundError
from src.domain.auth.value_objects import PartOfName, UserRole, Email
from src.domain.base_value_objects import UUID
from src.infrastructure.sqlalchemy.users.repository import SQLAlchemyUserRepository


async def create_user(async_session: AsyncSession) -> tuple[UUID, SQLAlchemyUserRepository]:
    repo = SQLAlchemyUserRepository(async_session)
    user_id = UUID(str(uuid.uuid4()))
    await repo.create(UserEntity(
        id=user_id,
        firstname=PartOfName("Nick"),
        lastname=PartOfName("Cargo"),
        role=UserRole("admin"),
        email=Email("nick@cargo.com"),
        hashed_password="32rserfs4t4ts4t4"
    ))
    await async_session.commit()
    return user_id, repo


async def test_create_user(test_async_session: AsyncSession):
    user_id, repo = await create_user(test_async_session)
    user = await repo.get_by_id(user_id)
    assert user.role == UserRole("admin")
    assert user.firstname == PartOfName("Nick")
    assert user.lastname == PartOfName("Cargo")
    assert user.email == Email("nick@cargo.com")


async def test_update_user(test_async_session: AsyncSession):
    user_id, repo = await create_user(test_async_session)
    user = await repo.get_by_id(user_id)
    user.firstname = PartOfName("Andrew")
    user.email = Email("andrew@mail.com")
    await repo.update(user)
    await test_async_session.commit()
    assert user.firstname == PartOfName("Andrew")
    assert user.email == Email("andrew@mail.com")


async def test_delete_user(test_async_session: AsyncSession):
    user_id, repo = await create_user(test_async_session)
    await repo.delete(user_id)
    await test_async_session.commit()
    with pytest.raises(UserNotFoundError):
        await repo.get_by_id(user_id)


async def test_get_another_email(test_async_session: AsyncSession):
    user_id, repo = await create_user(test_async_session)
    with pytest.raises(UserNotFoundError):
        await repo.get_by_email(Email("another@mail.ru"))
