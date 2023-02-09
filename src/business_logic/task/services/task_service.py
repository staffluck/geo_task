from typing import List

from pydantic import parse_obj_as

from src.business_logic.task.dto.task import (
    TaskCreate,
    TaskDetail,
    TaskDTO,
    TaskFilterByGeo,
)
from src.business_logic.task.dto.task_application import (
    TaskApplicationCreate,
    TaskApplicationDTO,
)
from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.task_application import TaskApplication
from src.business_logic.task.exceptions.task_application import (
    TaskApplicationAlreadyExistsError,
)
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

    async def add_application(
        self, task_application_data: TaskApplicationCreate
    ) -> TaskApplicationDTO:
        if await self.task_uow.task.user_has_application(
            task_application_data.user.id, task_application_data.task_id
        ):
            raise TaskApplicationAlreadyExistsError(["user"])
        task = TaskApplication.create(
            task_id=task_application_data.task_id,
            user_id=task_application_data.user.id,
            text=task_application_data.text,
        )
        task_in_db = await self.task_uow.task.add_aplication(task)
        await self.task_uow.commit()
        return TaskApplicationDTO.from_orm(task_in_db)
