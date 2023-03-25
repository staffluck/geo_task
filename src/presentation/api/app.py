from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.business_logic.common.exceptions import (
    AccessDeniedError,
    ApplicationError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)
from src.business_logic.common.validators import ValidationError
from src.business_logic.task.access_policy import TaskAccessPolicy, TaskApplicationAccessPolicy
from src.business_logic.task.services.task_application import TaskApplicationService
from src.business_logic.task.services.task_service import TaskService
from src.business_logic.user.services.auth_service import AuthService
from src.config import DatabaseSettings, LoggingSettings, SecuritySettings
from src.infrastructure.data_access.postgresql.db import create_sesionmaker
from src.infrastructure.data_access.postgresql.tables.mappers import map_tables
from src.infrastructure.data_access.postgresql.uow import SQLAlchemyUoW
from src.infrastructure.logger.main import setup_logging
from src.infrastructure.managers.hash_manager import HashManager
from src.infrastructure.managers.jwt_manager import JWTManager
from src.presentation.api.exception_handler import (
    access_denied_error_handler,
    application_error_handler,
    custom_validation_error_handler,
    object_already_exists_error_handler,
    object_not_found_error_handler,
    request_validation_error_handler,
)
from src.presentation.api.v1.depends import (
    get_auth_service,
    get_hash_manager,
    get_jwt_manager,
    get_session,
    get_task_access_policy,
    get_task_appl_access_policy,
    get_task_appl_service,
    get_task_service,
    get_uow,
)
from src.presentation.api.v1.routers import router
from src.presentation.schemas.exceptions import HandledValidationExceptionSchema


def setup_exception_handlers(app: FastAPI) -> None:
    del app.exception_handlers[RequestValidationError]
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(ObjectNotFoundError, object_not_found_error_handler)
    app.add_exception_handler(ObjectAlreadyExistsError, object_already_exists_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(AccessDeniedError, access_denied_error_handler)
    app.add_exception_handler(ValidationError, custom_validation_error_handler)


def setup_service_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[SQLAlchemyUoW] = get_uow
    app.dependency_overrides[TaskService] = get_task_service
    app.dependency_overrides[TaskApplicationService] = get_task_appl_service
    app.dependency_overrides[AuthService] = get_auth_service
    app.dependency_overrides[TaskApplicationAccessPolicy] = get_task_appl_access_policy
    app.dependency_overrides[TaskAccessPolicy] = get_task_access_policy


def setup_managers_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[JWTManager] = get_jwt_manager
    app.dependency_overrides[HashManager] = get_hash_manager


def setup_settings_dependencies(
    app: FastAPI, database_settings: DatabaseSettings, security_settings: SecuritySettings
) -> None:
    app.dependency_overrides[SecuritySettings] = lambda: security_settings
    app.dependency_overrides[DatabaseSettings] = lambda: database_settings


def setup_db_settings(app: FastAPI, database_settings: DatabaseSettings) -> None:
    async_sessionmaker = create_sesionmaker(database_settings)
    app.dependency_overrides[sessionmaker] = lambda: async_sessionmaker
    app.dependency_overrides[AsyncSession] = get_session


def setup_dependencies(app: FastAPI) -> None:
    security_settings = SecuritySettings()  # type: ignore
    database_settings = DatabaseSettings()  # type: ignore
    setup_service_dependencies(app)
    setup_settings_dependencies(
        app, database_settings=database_settings, security_settings=security_settings
    )
    setup_db_settings(app, database_settings=database_settings)


def setup_app() -> FastAPI:
    logging_settings = LoggingSettings()  # type: ignore
    setup_logging(logging_settings)
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
    setup_dependencies(app)

    map_tables()

    return app


app = setup_app()
