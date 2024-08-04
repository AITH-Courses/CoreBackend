import uuid

import pytest

from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserBySessionNotFoundError
from src.domain.auth.value_objects import PartOfName, UserRole, Email
from src.domain.base_value_objects import UUID
from src.infrastructure.redis.auth.session_service import RedisSessionService


@pytest.fixture(scope='function')
def redis_session_service(test_cache_session):
    return RedisSessionService(test_cache_session)


async def test_set_get_user(redis_session_service):
    auth_token = "auth-token"
    user = UserEntity(
        id=UUID(str(uuid.uuid4())),
        firstname=PartOfName("Nick"),
        lastname=PartOfName("Cargo"),
        role=UserRole("admin"),
        email=Email("nick@cargo.com"),
        hashed_password="32rserfs4t4ts4t4"
    )
    await redis_session_service.set(auth_token, user)
    user_in_cache = await redis_session_service.get(auth_token)
    assert user_in_cache.id == user.id
    assert user_in_cache.email == user.email
    assert user_in_cache.firstname == user.firstname
    assert user_in_cache.lastname == user.lastname
    assert user_in_cache.role == user.role
    assert user_in_cache.email == user.email
    assert user_in_cache.hashed_password == user.hashed_password


async def test_no_user(redis_session_service):
    auth_token = "auth-token"
    with pytest.raises(UserBySessionNotFoundError):
        await redis_session_service.get(auth_token)


async def test_delete_user(redis_session_service):
    auth_token = "auth-token"
    user = UserEntity(
        id=UUID(str(uuid.uuid4())),
        firstname=PartOfName("Nick"),
        lastname=PartOfName("Cargo"),
        role=UserRole("admin"),
        email=Email("nick@cargo.com"),
        hashed_password="32rserfs4t4ts4t4"
    )
    await redis_session_service.set(auth_token, user)
    await redis_session_service.delete(auth_token)
    with pytest.raises(UserBySessionNotFoundError):
        await redis_session_service.get(auth_token)


async def test_update_user(redis_session_service):
    auth_token = "auth-token"
    user = UserEntity(
        id=UUID(str(uuid.uuid4())),
        firstname=PartOfName("Nick"),
        lastname=PartOfName("Cargo"),
        role=UserRole("admin"),
        email=Email("nick@cargo.com"),
        hashed_password="32rserfs4t4ts4t4"
    )
    await redis_session_service.set(auth_token, user)
    updated_user = UserEntity(
        id=UUID(str(uuid.uuid4())),
        firstname=PartOfName("Carl"),
        lastname=PartOfName("Cargo"),
        role=UserRole("admin"),
        email=Email("nick@cargo.com"),
        hashed_password="32rserfs4t4ts4t4"
    )
    await redis_session_service.update(auth_token, updated_user)
    user_in_cache = await redis_session_service.get(auth_token)
    assert user_in_cache.id == updated_user.id
    assert user_in_cache.email == updated_user.email
    assert user_in_cache.firstname == updated_user.firstname
    assert user_in_cache.lastname == updated_user.lastname
    assert user_in_cache.role == updated_user.role
    assert user_in_cache.email == updated_user.email
    assert user_in_cache.hashed_password == updated_user.hashed_password
