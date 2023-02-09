from pydantic import Field

from src.business_logic.common.dto.base import DTO
from src.business_logic.task.dto.user import UserDTO


class BaseTask(DTO):
    title: str
    description: str
    reward: float = Field(gt=0)
    long: float
    lat: float


class TaskDTO(BaseTask):
    id: int


class TaskDetail(TaskDTO):
    owner: UserDTO


class TaskCreate(BaseTask):
    owner: UserDTO


class GeoLocation(DTO):
    long: float
    lat: float


class TaskFilter(DTO):
    current_geo: GeoLocation | None = None


class TaskFilterByGeo(DTO):
    current_geo: GeoLocation
