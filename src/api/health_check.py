from pydantic import BaseModel, Field
from fastapi import APIRouter, status


router = APIRouter(tags=["monitoring"])


class Health(BaseModel):
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
    }
)
def health_check():
    return Health(status="ok")
