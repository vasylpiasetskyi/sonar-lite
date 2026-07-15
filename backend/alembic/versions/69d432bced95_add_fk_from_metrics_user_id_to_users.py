"""add fk from metrics user_id to users

Revision ID: 69d432bced95
Revises: 6aedeab4cb5c
Create Date: 2026-07-15 17:52:45.297558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69d432bced95'
down_revision: Union[str, Sequence[str], None] = '6aedeab4cb5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        "fk_metrics_user_id_users",
        "metrics",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_metrics_user_id_users", "metrics", type_="foreignkey")
