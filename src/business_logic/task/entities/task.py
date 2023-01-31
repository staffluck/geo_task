from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    id: int
    title: str
    description: str
    reward: float
    long: float
    lat: float
    geo: Any = None

    @classmethod
    def create(
        cls, title: str, description: str, reward: float, long: float, lat: float
    ) -> Task:
        return cls(
            id=None,  # type: ignore
            title=title,
            reward=reward,
            description=description,
            long=long,
            lat=lat,
        )
