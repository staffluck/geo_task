from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DatabaseSettings, database_settings, server_settings


def make_connection_string(
    db_settings: DatabaseSettings, async_fallback: bool = False  # noqa FBT001
) -> str:
    result = db_settings.db_url
    if async_fallback:
        result += "?async_fallback=True"
    return result


engine = create_async_engine(make_connection_string(database_settings), echo=server_settings.DEBUG)
Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
    autoflush=False,
)
