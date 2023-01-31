import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy import Table

from src.business_logic.task.entities.task import Task
from src.infrastructure.data_access.postgresql.base import mapper_registry

task_table = Table(
    "task",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("title", sa.String(length=256), nullable=False),
    sa.Column("description", sa.String(length=256), nullable=False),
    sa.Column("reward", sa.BigInteger(), nullable=False),
    sa.Column("long", sa.Float),
    sa.Column("lat", sa.Float),
    sa.Column("geo", Geometry(geometry_type="POINT", srid=4326)),
)


def map_task() -> None:
    mapper_registry.map_imperatively(Task, task_table)