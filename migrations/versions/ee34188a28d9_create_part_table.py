"""create part table

Revision ID: ee34188a28d9
Revises: 
Create Date: 2025-05-01 22:50:04.434768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ee34188a28d9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    table = op.create_table(
        "parts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("sku", sa.String(30), nullable=False),
        sa.Column("description", sa.String(1024), nullable=True),
        sa.Column("weight_ounces", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
    )

    op.bulk_insert(table, [
        {
            "name": "Heavy coil",
            "sku": "SDJDDH8223DHJ",
            "description": "Tightly wound nickel-gravy alloy spring",
            "weight_ounces": 22,
            "is_active": True
        },
        {
            "name": "Reverse lever",
            "sku": "DCMM39823DSJD",
            "description": "Attached to provide inverse leverage",
            "weight_ounces": 9,
            "is_active": False
        },
        {
            "name": "Macrochip",
            "sku": "OWDD823011DJSD",
            "description": "Used for heavy-load computing",
            "weight_ounces": 2,
            "is_active": True
        }
    ])
def downgrade() -> None:
    op.drop_table("parts")
