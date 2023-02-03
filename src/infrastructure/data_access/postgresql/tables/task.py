import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship

from src.business_logic.task.entities.task import Task, TaskOwner
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
    sa.Column("owner_id", ForeignKey("user.id"), nullable=False),
)


def map_task() -> None:
    mapper_registry.map_imperatively(
        Task,
        task_table,
        properties={"owner": relationship(TaskOwner, lazy="noload")},
    )
