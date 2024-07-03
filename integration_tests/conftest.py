import asyncio
from typing import AsyncGenerator
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from src.app import create_application


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    app = create_application()
    return app


@pytest.fixture(scope="session")
async def async_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://localhost"
    ) as ac:
        yield ac
