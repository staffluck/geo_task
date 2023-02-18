from typing import TypedDict

from pydantic import BaseModel, Field


class TaskFilterByGeoQuerySchema(BaseModel):
    long: float
    lat: float


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    reward: int = Field(gt=0, example=100)
    long: float
    lat: float


class TaskUpdateSchema(TypedDict, total=False):
    title: str
    description: str


class TaskApplicationCreateSchema(BaseModel):
    text: str
    task_id: int
