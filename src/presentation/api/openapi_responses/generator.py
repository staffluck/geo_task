from src.business_logic.common.exceptions import ApplicationError, FieldBasedError
from src.presentation.schemas.exceptions import HandledExceptionSchema


def _generate_schema(message: str, context: dict | None) -> HandledExceptionSchema:
    return HandledExceptionSchema(message=message, context=context)


def generate_example_schema(
    exception: ApplicationError | FieldBasedError,
) -> HandledExceptionSchema:
    return _generate_schema(
        message=exception.message,
        context=exception.context
        if isinstance(exception, FieldBasedError)
        else {"detail": exception._context},
    )
