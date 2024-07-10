from pydantic import BaseModel, Field


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
