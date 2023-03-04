import argparse

import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--import-cities", "-ic", action="store_true")
    args = parser.parse_args()
    if args.import_cities:
        import_cities()
    else:
        uvicorn.run("src.presentation.api.app:app")
