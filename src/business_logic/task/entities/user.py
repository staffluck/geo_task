from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TaskUser:
    id: int
    email: str
    first_name: str | None
    last_name: str | None
