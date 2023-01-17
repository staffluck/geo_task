import sqlalchemy as sa
from sqlalchemy import Table

from src.business_logic.user.entities.user import User
from src.infrastructure.data_access.postgresql.base import mapper_registry

user_table = Table(
    "users",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("email", sa.String(length=256), nullable=False),
    sa.Column("password", sa.String(length=256), nullable=False),
    sa.Column("first_name", sa.String(length=100)),
    sa.Column("last_name", sa.String(length=100)),
    sa.UniqueConstraint("email"),
)


def map_user() -> None:
    mapper_registry.map_imperatively(User, user_table)
