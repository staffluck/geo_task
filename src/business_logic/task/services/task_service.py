from dataclasses import dataclass
from typing import List

from pydantic import parse_obj_as

from src.business_logic.common.exceptions import AccessDeniedError
from src.business_logic.task.access_policy import TaskAccessPolicy
from src.business_logic.task.dto.task import (
    TaskCreate,
    TaskDetail,
    TaskDTO,
    TaskFilterByGeo,
    TaskUpdate,
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


@dataclass
class GeoObject:
    long: float
    lat: float


class TaskService:
    def __init__(self, task_uow: ITaskUoW, access_policy: TaskAccessPolicy) -> None:
        self.task_uow = task_uow
        self.access_policy = access_policy

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
            geo=GeoObject(task_data.long, lat=task_data.lat),
            owner_id=task_data.owner.id,
        )
        task_in_db = await self.task_uow.task.create_task(task)
        await self.task_uow.commit()
        return TaskDTO.from_orm(task_in_db)

    async def delete_task(self, task_id: int) -> None:
        task = await self.task_uow.task.get_task_by_id(task_id)
        if not self.access_policy.modify_task(task):
            raise AccessDeniedError()
        await self.task_uow.task.delete_task(task_id)
        await self.task_uow.commit()

    async def update_task(self, task_data: TaskUpdate) -> TaskDTO:
        task = await self.task_uow.task.get_task_by_id(task_data.task_id)
        if not self.access_policy.modify_task(task):
            raise AccessDeniedError()
        task.update(title=task_data.title, description=task_data.description)
        await self.task_uow.task.update_task(task)
        await self.task_uow.commit()
        return TaskDTO.from_orm(task)

    async def add_application(
        self, task_application_data: TaskApplicationCreate
    ) -> TaskApplicationDTO:
        if await self.task_uow.task_appl.user_has_application(
            task_application_data.user.id, task_application_data.task_id
        ):
            raise TaskApplicationAlreadyExistsError(["user"])
        task = TaskApplication.create(
            task_id=task_application_data.task_id,
            user_id=task_application_data.user.id,
            text=task_application_data.text,
        )
        task_in_db = await self.task_uow.task_appl.create_application(task)
        await self.task_uow.commit()
        return TaskApplicationDTO.from_orm(task_in_db)
