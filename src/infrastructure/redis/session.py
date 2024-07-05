from redis import asyncio as aioredis
from redis.asyncio import Redis

from src.config import app_config

pool = aioredis.ConnectionPool.from_url(app_config.cache_url, max_connections=10)


async def get_redis_session() -> Redis:
    """Get Redis sesion.

    :return:
    """
    async with aioredis.Redis(connection_pool=pool) as session:
        yield session
