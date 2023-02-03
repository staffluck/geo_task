from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.business_logic.task.entities.user import TaskOwner


@dataclass
class Task:
    id: int
    title: str
    description: str
    reward: float
    long: float
    lat: float
    owner_id: int
    owner: TaskOwner
    geo: Any = None
