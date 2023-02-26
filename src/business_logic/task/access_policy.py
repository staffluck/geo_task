from typing import Protocol

from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.task_application import TaskApplication


class User(Protocol):
    id: int


class TaskAccessPolicy:
    def __init__(self, user: User) -> None:
        self.user = user

    def _is_owner(self, task: Task) -> bool:
        return task.owner_id == self.user.id

    modify_task = _is_owner
    retrieve_applications = _is_owner


class TaskApplicationAccessPolicy:
    def __init__(self, user: User) -> None:
        self.user = user

    def _is_owner(self, task_appl: TaskApplication) -> bool:
        return task_appl.user_id == self.user.id

    modify_task = _is_owner
