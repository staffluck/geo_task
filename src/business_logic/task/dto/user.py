from pydantic import EmailStr

from src.business_logic.common.dto.base import DTO


class TaskOwnerDTO(DTO):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None