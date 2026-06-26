"""create products

Revision ID: 202606250001
Revises:
Create Date: 2026-06-25 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202606250001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=240), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.execute(
        "CREATE INDEX ix_products_updated_at_id_desc "
        "ON products (updated_at DESC, id DESC)"
    )
    op.execute(
        "CREATE INDEX ix_products_category_updated_at_id_desc "
        "ON products (category, updated_at DESC, id DESC)"
    )


def downgrade() -> None:
    op.drop_index("ix_products_category_updated_at_id_desc", table_name="products")
    op.drop_index("ix_products_updated_at_id_desc", table_name="products")
    op.drop_table("products")