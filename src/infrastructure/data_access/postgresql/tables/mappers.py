from src.infrastructure.data_access.postgresql.tables.task import map_task
from src.infrastructure.data_access.postgresql.tables.user import map_user


def map_tables() -> None:
    map_user()
    map_task()
