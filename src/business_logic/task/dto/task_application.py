from src.business_logic.common.dto.base import DTO
from src.business_logic.task.dto.user import UserDTO


class TaskApplicationDTO(DTO):
    text: str
    user: UserDTO


class TaskApplicationCreate(DTO):
    text: str
    user: UserDTO
    task_id: int
