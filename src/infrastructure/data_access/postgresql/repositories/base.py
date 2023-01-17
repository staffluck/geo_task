from abc import ABC, abstractmethod

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    async def is_exists(self, **kwargs: str | int) -> bool:
        ...

    async def validate_uniques(self, obj: Table) -> list[str]:
        exc_context = []
        for column in obj.columns:
            if column.unique and not column.name == "id":
                to_search = {column.name: getattr(obj, column.name)}
                if await self.is_exists(**to_search):
                    exc_context.append(column.name)

        return exc_context
