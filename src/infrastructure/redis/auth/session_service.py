import json
from json.decoder import JSONDecodeError

from redis.asyncio import Redis

from src.domain.auth.constants import TIME_TO_LIVE_AUTH_SESSION
from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserBySessionNotFoundError
from src.domain.auth.value_objects import Email, PartOfName, UserRole
from src.domain.base_value_objects import UUID
from src.services.auth.session_service import SessionService


class RedisSessionService(SessionService):

    """Redis implementation of session service."""

    def __init__(self, session: Redis) -> None:
        self.session = session

    @staticmethod
    def from_domain_to_json_string(user: UserEntity) -> str:
        user_dict = {
            "id": user.id.value,
            "firstname": user.firstname.value,
            "lastname": user.lastname.value,
            "role": user.role.value,
            "email": user.email.value,
            "hashed_password": user.hashed_password,
        }
        return json.dumps(user_dict)

    async def get(self, auth_token: str) -> UserEntity:
        try:
            user_data_string = await self.session.get(auth_token)
            user_dict = json.loads(user_data_string)
            return UserEntity(
                id=UUID(user_dict["id"]),
                firstname=PartOfName(user_dict["firstname"]),
                lastname=PartOfName(user_dict["lastname"]),
                role=UserRole(user_dict["role"]),
                email=Email(user_dict["email"]),
                hashed_password=user_dict["hashed_password"],
            )
        except (TypeError, JSONDecodeError) as ex:  # no such key in Redis
            raise UserBySessionNotFoundError from ex

    async def update(self, auth_token: str, user: UserEntity) -> None:
        user_data_string = self.from_domain_to_json_string(user)
        remaining_ttl = await self.session.ttl(auth_token)
        await self.session.set(auth_token, user_data_string, keepttl=remaining_ttl)

    async def set(self, auth_token: str, user: UserEntity) -> None:
        user_data_string = self.from_domain_to_json_string(user)
        await self.session.setex(auth_token, TIME_TO_LIVE_AUTH_SESSION, user_data_string)

    async def delete(self, auth_token: str) -> None:
        await self.session.delete(auth_token)
