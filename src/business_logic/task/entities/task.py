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
    owner_id: int
    geo: Any = None

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        reward: float,
        long: float,
        lat: float,
        owner_id: int,
    ) -> Task:
        return cls(
            id=None,  # type: ignore
            title=title,
            description=description,
            reward=reward,
            long=long,
            lat=lat,
            owner_id=owner_id,
        )
