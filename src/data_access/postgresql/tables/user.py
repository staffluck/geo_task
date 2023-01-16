import sqlalchemy as sa
from sqlalchemy import Table

from data_access.postgresql.base import mapper_registry
from src.business_logic.entities.user import User

user_table = Table(
    "users",
    mapper_registry.metadata,
    sa.Column("email", sa.String(length=256), nullable=False),
    sa.Column("password", sa.String(length=256), nullable=False),
    sa.Column("first_name", sa.Column(length=100)),
    sa.Column("last_name", sa.Column(length=100)),
    sa.UniqueConstraint("email"),
)


def map_user():
    mapper_registry.map_imperatively(User, user_table)
