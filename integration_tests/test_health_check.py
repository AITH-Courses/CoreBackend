from fastapi import status
from httpx import AsyncClient


async def test_health_check(async_client: AsyncClient):
    response = await async_client.get(
        url="/health_check",
    )
    assert response.status_code == status.HTTP_200_OK
