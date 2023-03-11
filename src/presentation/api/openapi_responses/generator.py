from typing import Any

from src.business_logic.common.exceptions import ApplicationError, FieldBasedError
from src.presentation.schemas.exceptions import HandledExceptionSchema


def _generate_schema(message: str, context: dict[str, Any]) -> HandledExceptionSchema:
    return HandledExceptionSchema(message=message, context=context)


def generate_example_schema(
    exception: ApplicationError | FieldBasedError,
) -> HandledExceptionSchema:
    return _generate_schema(
        message=exception.message,
        context=exception.context
        if isinstance(exception, FieldBasedError)
        else {"detail": exception._context},  # noqa SLF001
    )
