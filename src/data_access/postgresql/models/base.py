import sqlalchemy as sa

from src.data_access.postgresql.base import Base


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer(), primary_key=True)
