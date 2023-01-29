from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    id: int
    title: str
    description: str
    long: float
    lat: float
    geo: Any = None

    @classmethod
    def create(cls, title: str, description: str, long: float, lat: float) -> Task:
        return cls(
            id=None,  # type: ignore
            title=title,
            description=description,
            long=long,
            lat=lat,
        )
