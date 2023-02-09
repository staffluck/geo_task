from __future__ import annotations

from dataclasses import dataclass

from src.business_logic.task.entities.user import User


@dataclass
class TaskApplication:
    id: int
    task_id: int
    text: str
    user_id: int
    user: User

    @classmethod
    def create(cls, text: str, task_id: int, user_id: int) -> TaskApplication:
        return cls(
            id=None,  # type: ignore
            user=None,  # type: ignore
            text=text,
            task_id=task_id,
            user_id=user_id,
        )
