from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from src.business_logic.common.dto.base import DTO


class LimitOffsetQuerySchema(BaseModel):
    limit: int = 100
    offset: int = 0


Model = TypeVar("Model", bound=DTO)


class BasePaginate(GenericModel, Generic[Model]):
    total: int
    limit: int
    offset: int
    data: list[Model]
