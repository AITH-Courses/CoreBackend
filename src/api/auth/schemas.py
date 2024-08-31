from pydantic import BaseModel, Field

from src.domain.auth.entities import UserEntity


class AuthTokenResponse(BaseModel):

    """Schema of auth token."""

    auth_token: str = Field("423fsdf23ffs3a2sd3432sd2fa2fag")


class LoginRequest(BaseModel):

    """Schema of login."""

    email: str = Field("john@mail.com")
    password: str = Field("super-password")


class RegisterRequest(BaseModel):

    """Schema of registration."""

    firstname: str = Field("Johny")
    lastname: str = Field("Stark")
    email: str = Field("john@mail.com")
    password: str = Field("super-password")


class UserDTO(BaseModel):

    """Schema of user."""

    id: str = Field("423fsdf23ffs3a2sd3432sd2fa2fag")
    firstname: str = Field("Johny")
    lastname: str = Field("Stark")
    email: str = Field("john@mail.com")
    role: str = Field("talent")

    @staticmethod
    def from_entity(user: UserEntity) -> "UserDTO":
        return UserDTO(
            id=user.id.value,
            firstname=user.firstname.value,
            lastname=user.lastname.value,
            email=user.email.value,
            role=user.role.value,
        )
