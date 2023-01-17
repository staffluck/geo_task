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


class ServerSettings(BaseSettings):
    DEBUG: bool = True

    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000


class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: str


database_settings = DatabaseSettings()
security_settings = SecuritySettings()
