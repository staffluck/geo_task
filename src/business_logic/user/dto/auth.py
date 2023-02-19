from pydantic import EmailStr, Field, validator

from src.business_logic.common.dto.base import DTO
from src.business_logic.user.validators.password import validate_password


class BaseUser(DTO):
    email: EmailStr
    first_name: str
    last_name: str | None


class UserCreate(BaseUser):
    password: str

    @validator("password", pre=True)
    def validate_raw_password(cls, password: str) -> str:  # noqa: N805
        validate_password(password)
        return password


class UserSignin(DTO):
    email: EmailStr
    password: str = Field(min_length=6)


class Token(DTO):
    access_token: str
    refresh_token: str


class AccessTokenData(DTO):
    user_id: int


class RefreshTokenData(DTO):
    user_id: int


class UserDTO(BaseUser):
    id: int
