from pydantic import BaseModel


class HandledExceptionSchema(BaseModel):
    message: str
    context: dict
