from typing import List

from pydantic import parse_obj_as

from src.business_logic.task.dto.task import TaskDTO
from src.business_logic.task.protocols.uow import ITaskUoW


class TaskService:
    def __init__(
        self,
        task_uow: ITaskUoW,
    ) -> None:
        self.task_uow = task_uow

    async def get_tasks(self, limit: int = 100, offset: int = 0) -> list[TaskDTO]:
        tasks = await self.task_uow.task.get_tasks(limit=limit, offset=offset)
        return parse_obj_as(List[TaskDTO], tasks)
