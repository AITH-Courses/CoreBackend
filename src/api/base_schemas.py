from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):

    """Schema of error operation."""

    message: str = Field(examples=["Произошла ошибка"])


class SuccessResponse(BaseModel):

    """Schema of success operation."""

    message: str = Field(examples=["Операция успешно выполнена"])
