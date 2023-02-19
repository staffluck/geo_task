from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.business_logic.common.constants import Empty


class GeoCoord(Protocol):
    lat: float
    long: float


@dataclass
class Task:
    id: int
    title: str
    description: str
    reward: float
    owner_id: int
    geo: GeoCoord | str | None = None

    @property
    def long(self) -> float:
        if self.geo and not isinstance(self.geo, str):
            return self.geo.long
        raise AttributeError()

    @property
    def lat(self) -> float:
        if self.geo and not isinstance(self.geo, str):
            return self.geo.lat
        raise AttributeError()

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

    def update(
        self, title: str | Empty = Empty.UNSET, description: str | Empty = Empty.UNSET
    ) -> Task:
        if title is not Empty.UNSET:
            self.title = title
        if description is not Empty.UNSET:
            self.description = description
        return self
