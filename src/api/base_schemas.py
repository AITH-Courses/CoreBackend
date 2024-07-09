from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):

    """Schema of error operation."""

    message: str = Field("Something error message")


class SuccessResponse(BaseModel):

    """Schema of success operation."""

    message: str = Field("All is well")
