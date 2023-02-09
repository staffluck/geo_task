from dataclasses import dataclass

from src.business_logic.task.entities.user import User


@dataclass
class TaskApplication:
    id: int
    task_id: int
    text: str
    user: User
