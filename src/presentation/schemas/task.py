from typing import TypedDict

from pydantic import BaseModel, Field

from src.business_logic.task.dto.task import TaskDTO
from src.business_logic.task.dto.task_application import (
    TaskApplicationDetail,
    TaskApplicationDTO,
)
from src.presentation.schemas.common import BasePaginate


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


TaskPaginatedResponseSchema = BasePaginate[TaskDTO]
TaskPaginatedResponseSchema.__name__ = "Paginate[List[TaskDTO]]"

TaskApplPaginatedResponseSchema = BasePaginate[TaskApplicationDTO]
TaskApplPaginatedResponseSchema.__name__ = "Paginate[List[TaskApplicationDTO]]"

TaskApplDetailPaginatedResponseSchema = BasePaginate[TaskApplicationDetail]
TaskApplDetailPaginatedResponseSchema.__name__ = "Paginate[List[TaskApplicationDetail]]"
