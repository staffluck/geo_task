"""city_table

Revision ID: 76c1e690382a
Revises: 4f086789b675
Create Date: 2023-03-04 19:20:12.149584

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "76c1e690382a"
down_revision = "4f086789b675"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "city",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column(
            "geo",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON", from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=True,
        ),
        sa.Column("guid", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_city")),
    )
    op.create_index(op.f("ix_city_name"), "city", ["name"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_city_name"), table_name="city")
    op.drop_table("city")
    # ### end Alembic commands ###