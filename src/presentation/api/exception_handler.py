from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.business_logic.common.exceptions import (
    ApplicationError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)
from src.presentation.schemas.exceptions import (
    HandledExceptionSchema,
    HandledValidationExceptionSchema,
)


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


def request_validation_error_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    exception_schema = HandledValidationExceptionSchema(
        message="Невозможно обработать тело/параметры запроса",
        context=jsonable_encoder(exc.errors()),
    )
    return JSONResponse(status_code=422, content=exception_schema.dict())
