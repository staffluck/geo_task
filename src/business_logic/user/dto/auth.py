from pydantic import EmailStr, Field

from src.business_logic.common.dto.base import DTO


class BaseUser(DTO):
    email: EmailStr
    first_name: str | None
    last_name: str | None


class UserCreate(BaseUser):
    password: str = Field(min_length=6)


class UserDTO(BaseUser):
    ...
