from src.business_logic.common.dto.base import DTO


class BaseTask(DTO):
    title: str
    description: str
    reward: float


class TaskDTO(BaseTask):
    ...
