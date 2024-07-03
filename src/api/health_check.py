from fastapi import APIRouter, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["monitoring"])


class Health(BaseModel):

    """Health response."""

    status: str = Field(examples=["ok"])


@router.get(
    "/health_check",
    status_code=status.HTTP_200_OK,
    description="Check health of service",
    summary="Health check",
    responses={
        status.HTTP_200_OK: {
            "model": Health,
            "description": "Service is alive",
        },
    },
)
def health_check() -> Health:
    """Check health of service.

    :return: Health
    """
    return Health(status="ok")
