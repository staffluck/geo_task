from pydantic import BaseModel, Field


class HandledExceptionSchema(BaseModel):
    message: str
    context: dict


class HandledValidationExceptionSchema(BaseModel):
    message: str
    context: list = Field(
        example=[
            [
                {
                    "loc": ["loc(body/query/nested/)", "field"],
                    "msg": "field required",
                    "type": "type_error.missing",
                }
            ]
        ]
    )
