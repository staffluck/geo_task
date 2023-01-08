from dotenv import load_dotenv
from pydantic import BaseSettings as pydantic_BaseSettings
from pydantic import PostgresDsn

load_dotenv()


class BaseSettings(pydantic_BaseSettings):
    pass


class DatabaseSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str | None

    @property
    def db_url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            path=f"/{self.DB_NAME}",
            port=self.DB_PORT,
        )


class ServerConfig(BaseSettings):
    DEBUG: bool = True

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000


import os

print(os.getenv("DB_NAME"))

database_settings = DatabaseSettings()
