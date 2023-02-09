from dataclasses import dataclass

from src.business_logic.task.entities.user import TaskUser


@dataclass
class TaskApplication:
    id: int
    task_id: int
    text: str
    user: TaskUser
