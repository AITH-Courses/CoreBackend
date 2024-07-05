from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    message: str = Field("Something error message")


class SuccessResponse(BaseModel):
    message: str = Field("All is well")


class AuthTokenResponse(BaseModel):
    auth_token: str = Field("423fsdf23ffs3a2sd3432sd2fa2fag")


class LoginRequest(BaseModel):
    email: str = Field("john@mail.com")
    password: str = Field("super-password")


class RegisterRequest(BaseModel):
    firstname: str = Field("Johny")
    lastname: str = Field("Stark")
    email: str = Field("john@mail.com")
    password: str = Field("super-password")


class UserDTO(BaseModel):
    id: str = Field("423fsdf23ffs3a2sd3432sd2fa2fag")
    firstname: str = Field("Johny")
    lastname: str = Field("Stark")
    email: str = Field("john@mail.com")
