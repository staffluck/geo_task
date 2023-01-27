import uvicorn
from fastapi import FastAPI

from src.business_logic.common.exceptions import (
    ApplicationError,
    ObjectAlreadyExistsError,
    ObjectNotFoundError,
)
from src.config import ServerSettings
from src.infrastructure.data_access.postgresql.tables.user import map_user
from src.presentation.api.exception_handler import (
    application_error_handler,
    object_already_exists_error_handler,
    object_not_found_error_handler,
)
from src.presentation.api.v1.routers import router


def setup_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(router)

    map_user()

    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(ObjectNotFoundError, object_not_found_error_handler)
    app.add_exception_handler(
        ObjectAlreadyExistsError, object_already_exists_error_handler
    )
    return app


app = setup_app()


if __name__ == "__main__":
    server_settings = ServerSettings()
    uvicorn.run(
        app="src.presentation.api.app:app",
        host=server_settings.SERVER_HOST,
        port=server_settings.SERVER_PORT,
        reload=server_settings.DEBUG,
    )
