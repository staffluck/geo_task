import uvicorn
from fastapi import FastAPI

from src.config import ServerSettings
from src.presentation.api.v1.routers import router


def setup_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(router)
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
