from sqlalchemy import MetaData

from src.config import app_config
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

async_engine = create_async_engine(url=app_config.db_url, echo=app_config.is_debug)
async_session_factory = async_sessionmaker(
    bind=async_engine, autocommit=False, autoflush=False
)
meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


Base = declarative_base(metadata=meta)
