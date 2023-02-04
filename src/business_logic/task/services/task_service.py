from typing import List

from pydantic import parse_obj_as

from src.business_logic.task.dto.task import (
    TaskCreate,
    TaskDetail,
    TaskDTO,
    TaskFilterByGeo,
)
from src.business_logic.task.entities.task import Task
from src.business_logic.task.protocols.uow import ITaskUoW


class TaskService:
    def __init__(
        self,
        task_uow: ITaskUoW,
    ) -> None:
        self.task_uow = task_uow

    async def get_tasks(self, *, limit: int = 100, offset: int = 0) -> list[TaskDTO]:
        tasks = await self.task_uow.task.get_tasks(limit=limit, offset=offset)
        return parse_obj_as(List[TaskDTO], tasks)

    async def get_near_tasks(
        self, filter: TaskFilterByGeo, *, limit: int = 100, offset: int = 0
    ) -> list[TaskDTO]:
        tasks = await self.task_uow.task.get_tasks_in_radius(
            filter,
            radius=10 * 1000,
            limit=limit,
            offset=offset,
        )
        return parse_obj_as(List[TaskDTO], tasks)

    async def get_task_detail(self, task_id: int) -> TaskDetail:
        task = await self.task_uow.task_reader.get_task_detail(task_id)
        return task

    async def create_task(self, task_data: TaskCreate) -> TaskDTO:
        task = Task.create(
            title=task_data.title,
            description=task_data.description,
            reward=task_data.reward,
            long=task_data.long,
            lat=task_data.lat,
            owner_id=task_data.owner.id,
        )
        task_in_db = await self.task_uow.task.create_task(task)
        await self.task_uow.commit()
        return TaskDTO.from_orm(task_in_db)
