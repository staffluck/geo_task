from pydantic import Field, validator

from src.business_logic.common.constants import Empty
from src.business_logic.common.dto.base import DTO
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.validators.task import validate_title


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

    @validator("title", pre=True)
    def validate_raw_title(cls, title: str) -> str:  # noqa: N805
        validate_title(title)
        return title

    @validator("description", pre=True)
    def validate_raw_description(cls, description: str) -> str:  # noqa: N805
        validate_title(description)
        return description


class TaskUpdate(DTO):
    task_id: int
    title: str | Empty = Empty.UNSET
    description: str | Empty = Empty.UNSET


class GeoLocation(DTO):
    long: float
    lat: float


class TaskFilter(DTO):
    current_geo: GeoLocation | None = None


class TaskFilterByGeo(DTO):
    current_geo: GeoLocation
