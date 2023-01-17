from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.business_logic.common.protocols import IUoW
from src.business_logic.user.protocols.repository import IUserRepoistory
from src.business_logic.user.protocols.uow import IUserUoW


class SQLAlchemyBaseUoW(IUoW):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class SQLAlchemyUoW(SQLAlchemyBaseUoW, IUserUoW):
    def __init__(self, session: AsyncSession, user_repo: Type[IUserRepoistory]) -> None:
        self.session = session
        self.user = user_repo(session)
