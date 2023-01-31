from typing import List

from pydantic import parse_obj_as

from src.business_logic.task.dto.task import TaskDTO, TaskFilter, TaskFilterByGeo
from src.business_logic.task.protocols.uow import ITaskUoW


class TaskService:
    def __init__(
        self,
        task_uow: ITaskUoW,
    ) -> None:
        self.task_uow = task_uow

    async def get_tasks(
        self, filter: TaskFilter | None = None, limit: int = 100, offset: int = 0
    ) -> list[TaskDTO]:
        if not filter or not filter.current_geo:
            tasks = await self.task_uow.task.get_tasks(limit=limit, offset=offset)
        else:
            if filter.current_geo:
                tasks = await self.task_uow.task.get_tasks_in_radius(
                    TaskFilterByGeo(current_geo=filter.current_geo),
                    radius=10 * 1000,
                    limit=limit,
                    offset=offset,
                )
        return parse_obj_as(List[TaskDTO], tasks)
