import argparse
import asyncio

import uvicorn

from src.commands.import_cities import import_cities
from src.config import DatabaseSettings, ServerSettings
from src.infrastructure.data_access.postgresql.db import create_sesionmaker

if __name__ == "__main__":
    server_settings = ServerSettings()
    database_settings = DatabaseSettings()  # type: ignore
    parser = argparse.ArgumentParser()
    parser.add_argument("--import-cities", "-ic", action="store_true")
    args = parser.parse_args()
    if args.import_cities:
        sessionmaker = create_sesionmaker(
            database_settings=database_settings, echo=server_settings.DEBUG
        )
        asyncio.run(import_cities(sessionmaker()))
    else:
        uvicorn.run(
            "src.presentation.api.app:app",
            reload=True,
            port=server_settings.SERVER_PORT,
            host=server_settings.SERVER_HOST,
        )
