from pydantic import Field

from src.business_logic.common.dto.base import DTO


class BaseTask(DTO):
    title: str
    description: str
    reward: float = Field(gt=0)
    long: float
    lat: float


class TaskDTO(BaseTask):
    ...


class TaskCreate(BaseTask):
    owner_id: int


class GeoLocation(DTO):
    long: float
    lat: float


class TaskFilter(DTO):
    current_geo: GeoLocation | None = None


class TaskFilterByGeo(DTO):
    current_geo: GeoLocation
