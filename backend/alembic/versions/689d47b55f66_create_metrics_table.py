"""create metrics table

Revision ID: 689d47b55f66
Revises: 
Create Date: 2026-07-14 19:32:36.049630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '689d47b55f66'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    metric_type_enum = sa.Enum(
        "weight", "sleep", "heart_rate", "steps", "water", name="metric_type"
    )
    op.create_table(
        "metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("metric_type", metric_type_enum, nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_metrics_user_recorded", "metrics", ["user_id", "recorded_at"])
    op.create_index(
        "ix_metrics_user_type_recorded", "metrics", ["user_id", "metric_type", "recorded_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_metrics_user_type_recorded", table_name="metrics")
    op.drop_index("ix_metrics_user_recorded", table_name="metrics")
    op.drop_table("metrics")
    sa.Enum(name="metric_type").drop(op.get_bind(), checkfirst=True)
