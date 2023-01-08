import sqlalchemy as sa

from src.data_access.postgresql.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = sa.Column(sa.String(length=256), nullable=False)
    password = sa.Column(sa.String(length=256), nullable=False)
    first_name = sa.Column(sa.String(length=256))
    last_name = sa.Column(sa.String(length=256))
