from fastapi import Request
from fastapi.responses import JSONResponse

from src.business_logic.common.exceptions import ApplicationError
from src.presentation.schemas.exceptions import HandledExceptionSchema


def application_error_handler(_: Request, exc: ApplicationError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict())
