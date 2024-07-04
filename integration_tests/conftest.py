import asyncio
from typing import AsyncGenerator
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession

from src.app import create_application
from src.infrastructure.sqlalchemy.session import async_engine, Base


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


@pytest.fixture(scope='function')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def test_async_session(async_db_engine: AsyncEngine):
    async_session_factory = async_sessionmaker(
        bind=async_db_engine,
        autocommit=False,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    )
    async with async_session_factory() as session:
        yield session


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
