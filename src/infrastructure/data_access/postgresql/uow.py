from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.business_logic.common.protocols import IUoW
from src.business_logic.task.protocols.uow import ITaskUoW
from src.business_logic.user.protocols.uow import IUserUoW
from src.infrastructure.data_access.postgresql.repositories.task import (
    TaskReader,
    TaskRepository,
)
from src.infrastructure.data_access.postgresql.repositories.task_application import (
    TaskApplicationReader,
    TaskApplicationRepository,
)
from src.infrastructure.data_access.postgresql.repositories.user import UserRepository


class SQLAlchemyBaseUoW(IUoW):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class SQLAlchemyUoW(SQLAlchemyBaseUoW, IUserUoW, ITaskUoW):
    def __init__(
        self,
        session: AsyncSession,
        user_repo: Type[UserRepository],
        task_repo: Type[TaskRepository],
        task_reader: Type[TaskReader],
        task_appl: Type[TaskApplicationRepository],
        task_appl_reader: Type[TaskApplicationReader],
    ) -> None:
        self.user = user_repo(session)
        self.task = task_repo(session)
        self.task_reader = task_reader(session)
        self.task_appl = task_appl(session)
        self.task_appl_reader = task_appl_reader(session)
        super().__init__(session)
