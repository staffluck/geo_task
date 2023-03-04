import geoalchemy2
import sqlalchemy as sa

from src.infrastructure.data_access.postgresql.base import mapper_registry

city_table = sa.Table(
    "city",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("name", sa.String(length=256), nullable=False, index=True),
    sa.Column("geo", geoalchemy2.Geometry(geometry_type="POLYGON")),
    sa.Column("guid", sa.String(length=256), nullable=False),
)
