from pydantic import validator

from src.business_logic.common.dto.base import DTO
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.validators.task_application import validate_text


class TaskApplicationDTO(DTO):
    text: str
    user: UserDTO


class TaskApplicationCreate(DTO):
    text: str
    user: UserDTO
    task_id: int

    @validator("text", pre=True)
    def validate_raw_text(cls, text: str) -> str:  # noqa: N805
        validate_text(text)
        return text
