import json
from json.decoder import JSONDecodeError
from redis.asyncio import Redis

from src.domain.auth.constants import TIME_TO_LIVE_AUTH_SESSION
from src.domain.auth.entities import UserEntity
from src.domain.auth.exceptions import UserBySessionNotFoundError
from src.domain.auth.value_objects import PartOfName, UserRole, Email
from src.services.auth.session_service import SessionService


class RedisSessionService(SessionService):
    def __init__(self, session: Redis):
        self.session = session

    @staticmethod
    def from_domain_to_json_string(user: UserEntity) -> str:
        user_dict = dict(
            id=user.id,
            firstname=user.firstname.value,
            lastname=user.lastname.value,
            role=user.role.value,
            email=user.email.value,
            hashed_password=user.hashed_password,
        )
        user_data_string = json.dumps(user_dict)
        return user_data_string

    async def get(self, auth_token: str) -> UserEntity:
        try:
            user_data_string = await self.session.get(auth_token)
            user_dict = json.loads(user_data_string)
            return UserEntity(
                id=user_dict["id"],
                firstname=PartOfName(user_dict["firstname"]),
                lastname=PartOfName(user_dict["lastname"]),
                role=UserRole(user_dict["role"]),
                email=Email(user_dict["email"]),
                hashed_password=user_dict["hashed_password"],
            )
        except (TypeError, JSONDecodeError):  # no such key in Redis
            raise UserBySessionNotFoundError

    async def update(self, auth_token: str, user: UserEntity) -> None:
        user_data_string = self.from_domain_to_json_string(user)
        remaining_ttl = await self.session.ttl(auth_token)
        await self.session.set(auth_token, user_data_string, keepttl=remaining_ttl)

    async def set(self, auth_token: str, user: UserEntity) -> None:
        user_data_string = self.from_domain_to_json_string(user)
        await self.session.set(auth_token, user_data_string, keepttl=TIME_TO_LIVE_AUTH_SESSION)

    async def delete(self, auth_token: str) -> None:
        await self.session.delete(auth_token)
