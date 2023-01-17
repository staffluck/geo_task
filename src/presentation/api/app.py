import uvicorn
from fastapi import FastAPI

from src.config import ServerSettings


def setup_app() -> FastAPI:
    app = FastAPI(debug=True)
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
