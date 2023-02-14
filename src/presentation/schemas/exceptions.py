from pydantic import BaseModel


class HandledExceptionSchema(BaseModel):
    message: str
    context: dict


class HandledValidationExceptionSchema(BaseModel):
    message: str
    context: list
