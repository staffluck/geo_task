from fastapi import Request
from fastapi.responses import JSONResponse

from src.business_logic.common.exceptions import (
    ApplicationError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)
from src.presentation.schemas.exceptions import HandledExceptionSchema


def application_error_handler(_: Request, exc: ApplicationError) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=500)


def object_not_found_error_handler(
    _: Request, exc: ObjectNotFoundError
) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=400)


def object_already_exists_error_handler(
    _: Request, exc: ObjectAlreadyExistsError
) -> JSONResponse:
    schema = HandledExceptionSchema(message=exc.message, context=exc.context)
    return JSONResponse(content=schema.dict(), status_code=400)
