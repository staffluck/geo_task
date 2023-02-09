from typing import Protocol

from src.business_logic.task.dto.task import TaskDetail, TaskFilterByGeo
from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.task_application import TaskApplication


class ITaskReader(Protocol):
    async def get_task_detail(self, task_id: int) -> TaskDetail:
        ...


class ITaskRepository(Protocol):
    async def create_task(self, task: Task) -> Task:
        ...

    async def is_exists(self, **kwargs: str | int) -> bool:
        ...

    async def get_task_by_id(self, task_id: int) -> Task:
        ...

    async def get_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        ...

    async def get_tasks_in_radius(
        self, filter: TaskFilterByGeo, radius: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        ...

    async def add_aplication(
        self, task_application: TaskApplication
    ) -> TaskApplication:
        ...
