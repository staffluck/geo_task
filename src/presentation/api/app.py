from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.business_logic.common.exceptions import (
    AccessDeniedError,
    ApplicationError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)
from src.business_logic.task.services.task_service import TaskService
from src.business_logic.user.services.auth_service import AuthService
from src.infrastructure.data_access.postgresql.tables.mappers import map_tables
from src.presentation.api.exception_handler import (
    access_denied_error_handler,
    application_error_handler,
    object_already_exists_error_handler,
    object_not_found_error_handler,
    request_validation_error_handler,
)
from src.presentation.api.v1.depends import get_auth_service, get_task_service
from src.presentation.api.v1.routers import router
from src.presentation.schemas.exceptions import HandledValidationExceptionSchema


def setup_exception_handlers(app: FastAPI) -> None:
    del app.exception_handlers[RequestValidationError]
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(ObjectNotFoundError, object_not_found_error_handler)
    app.add_exception_handler(
        ObjectAlreadyExistsError, object_already_exists_error_handler
    )
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(AccessDeniedError, access_denied_error_handler)


def setup_dependency(app: FastAPI) -> None:
    app.dependency_overrides[TaskService] = get_task_service
    app.dependency_overrides[AuthService] = get_auth_service


def setup_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(
        router,
        responses={
            422: {
                "description": "Validation Error",
                "model": HandledValidationExceptionSchema,
            }
        },
    )

    setup_exception_handlers(app)
    setup_dependency(app)

    map_tables()

    return app


app = setup_app()
