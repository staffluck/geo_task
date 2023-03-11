import argparse
import asyncio

import uvicorn

from src.commands.import_cities import import_cities

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--import-cities", "-ic", action="store_true")
    args = parser.parse_args()
    if args.import_cities:
        asyncio.run(import_cities())
    else:
        uvicorn.run("src.presentation.api.app:app", reload=True, port=8000, host="0.0.0.0")
