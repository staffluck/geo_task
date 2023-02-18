import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.business_logic.task.entities.task_application import TaskApplication
from src.business_logic.task.entities.user import User
from src.infrastructure.data_access.postgresql.base import mapper_registry

task_table = sa.Table(
    "task_application",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("text", sa.String(length=256), nullable=False),
    sa.Column("user_id", sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    sa.Column("task_id", sa.ForeignKey("task.id", ondelete="CASCADE"), nullable=False),
)


def map_task_application() -> None:
    mapper_registry.map_imperatively(
        TaskApplication,
        task_table,
        properties={
            "user": relationship(User, uselist=False, lazy="joined", viewonly=True)
        },
    )
