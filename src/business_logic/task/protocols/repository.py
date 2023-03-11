from typing import Protocol

from src.business_logic.task.dto.task import TaskDetail, TaskFilterByGeo
from src.business_logic.task.dto.task_application import TaskApplicationDetail, TaskApplicationDTO
from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.task_application import TaskApplication


class ITaskReader(Protocol):
    async def get_task_detail(self, task_id: int) -> TaskDetail:
        ...

    async def get_task_applications_by_task_id(
        self, task_id: int, limit: int = 100, offset: int = 0
    ) -> list[TaskApplicationDTO]:
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
        self, filters: TaskFilterByGeo, radius: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        ...

    async def delete_task(self, task_id: int) -> None:
        ...

    async def update_task(self, task: Task) -> Task:
        ...

    async def get_nearest_city_name(self, lat: float, long: float) -> str:
        ...


class ITaskApplicationReader(Protocol):
    async def get_user_task_applications(
        self, user_id: int, limit: int = 100, offset: int = 0
    ) -> list[TaskApplicationDetail]:
        ...


class ITaskApplicationRepository(Protocol):
    async def user_has_application(self, user_id: int, task_id: int) -> bool:
        ...

    async def create_application(self, task_application: TaskApplication) -> TaskApplication:
        ...
