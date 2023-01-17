from typing import AsyncGenerator

from fastapi import Depends

from src.config import (
    DatabaseSettings,
    SecuritySettings,
    database_settings,
    security_settings,
)
from src.infrastructure.data_access.postgresql.db import Session
from src.infrastructure.managers.jwt_manager import JWTManager


async def get_session() -> AsyncGenerator:
    session = Session()
    try:
        yield session
    finally:
        await session.rollback()


def get_db_settings() -> DatabaseSettings:
    return database_settings


def get_security_settings() -> SecuritySettings:
    return security_settings


def get_jwt_manager(
    security_settings: SecuritySettings = Depends(get_security_settings),
) -> JWTManager:
    return JWTManager(security_settings)
