from pydantic import BaseModel


class LimitOffsetQuerySchema(BaseModel):
    limit: int = 100
    offset: int = 0
