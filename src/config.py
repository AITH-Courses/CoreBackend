from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):
    DEV = "dev"
    PRODUCTION = "production"
    TEST = "test"


class Config(BaseSettings):
    """
    Class for loading the necessary env variables
    """
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    MODE: ApplicationMode = Field(default=ApplicationMode.PRODUCTION)

    @property
    def is_debug(self) -> bool:
        """
        Gets true if application in dev mode else false
        """
        return self.MODE == ApplicationMode.DEV

    @staticmethod
    def __generate_asyncpg_db_url(
            user: str, password: str, host, port: str, database_name: str
    ) -> str:
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}"

    @property
    def db_url(self) -> str:
        """
        Gets DSN for database
        """
        return self.__generate_asyncpg_db_url(
            self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST,
            self.POSTGRES_PORT, self.POSTGRES_DB
        )

    model_config = SettingsConfigDict(env_file=".env")


app_config = Config()
