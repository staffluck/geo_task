import geoalchemy2
import sqlalchemy as sa
from sqlalchemy import ForeignKey, Table

import src.infrastructure.data_access.postgresql.tables.monkey_patch_geo  # noqa
from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.user import User
from src.infrastructure.data_access.postgresql.base import mapper_registry
from src.infrastructure.data_access.postgresql.tables.user import user_table

task_table = Table(
    "task",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("title", sa.String(length=256), nullable=False),
    sa.Column("description", sa.String(length=256), nullable=False),
    sa.Column("reward", sa.BigInteger(), nullable=False),
    sa.Column("long", sa.Float),
    sa.Column("lat", sa.Float),
    sa.Column("geo", geoalchemy2.Geometry(geometry_type="POINT", srid=4326)),
    sa.Column("owner_id", ForeignKey("user.id"), nullable=False),
)


def map_task() -> None:
    mapper_registry.map_imperatively(Task, task_table)
    mapper_registry.map_imperatively(
        User,
        user_table,
    )
