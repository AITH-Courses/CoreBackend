from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):

    """Variants of application mode."""

    DEV = "dev"
    PRODUCTION = "production"
    TEST = "test"


class Config(BaseSettings):

    """Class for loading the necessary env variables."""

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    REDIS_PORT: str
    REDIS_HOST: str

    MODE: ApplicationMode = Field(default=ApplicationMode.PRODUCTION)

    @property
    def is_debug(self) -> bool:
        """Gets true if application in dev mode else false."""
        return self.MODE == ApplicationMode.DEV

    @staticmethod
    def __generate_asyncpg_db_url(
            user: str, password: str, host: str, port: str, database_name: str,
    ) -> str:
        """Get asynpg database url.

        :param user:
        :param password:
        :param host:
        :param port:
        :param database_name:
        :return: dns
        """
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}"

    @property
    def db_url(self) -> str:
        """Get DSN for database."""
        return self.__generate_asyncpg_db_url(
            self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST,
            self.POSTGRES_PORT, self.POSTGRES_DB,
        )

    @staticmethod
    def __get_redis_cache_url(user: str, password: str, host: str, port: str) -> str:
        """Get redis cache url.

        :param user:
        :param password:
        :param host:
        :param port:
        :return: dns
        """
        return f"redis://{user}:{password}@{host}:{port}/0"

    @property
    def cache_url(self) -> str:
        """Get DSN to cache."""
        return self.__get_redis_cache_url(
            self.REDIS_USER, self.REDIS_USER_PASSWORD, self.REDIS_HOST, self.REDIS_PORT,
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_config = Config()
