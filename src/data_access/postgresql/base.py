from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import DatabaseSettings

Base = declarative_base()

engine = create_async_engine(
    DatabaseSettings().db_url,
    echo=True,
)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)
