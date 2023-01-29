from sqlalchemy import select

from src.business_logic.task.entities.task import Task
from src.business_logic.task.exceptions.task import TaskNotFoundError
from src.business_logic.task.protocols.repository import ITaskRepository
from src.infrastructure.data_access.postgresql.repositories.base import BaseRepository


class TaskRepository(BaseRepository, ITaskRepository):
    async def is_exists(self, **kwargs: str | int) -> bool:
        query = select(select(Task.id).filter_by(**kwargs).exists())
        expr = await self.session.execute(query)
        return bool(expr.scalar())

    async def create_task(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_task_by_id(self, task_id: int) -> Task:
        query = select(Task).filter(Task.id == task_id)
        expr = await self.session.execute(query)
        task = expr.scalar()
        if not task:
            raise TaskNotFoundError(["id"])
        return task

    async def get_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        query = select(Task).limit(limit).offset(offset)
        expr = await self.session.execute(query)
        return expr.scalars().all()
