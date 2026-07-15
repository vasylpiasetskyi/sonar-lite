import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


async def test_metrics_table_has_expected_columns_and_indexes() -> None:
    engine = create_async_engine(settings.database_url)

    async with engine.connect() as conn:

        def inspect(
            sync_conn: sa.Connection,
        ) -> tuple[set[str], set[str], dict[str, sa.types.TypeEngine]]:
            inspector = sa.inspect(sync_conn)
            columns = {c["name"] for c in inspector.get_columns("metrics")}
            indexes = {i["name"] for i in inspector.get_indexes("metrics")}
            column_types = {c["name"]: c["type"] for c in inspector.get_columns("metrics")}
            return columns, indexes, column_types

        columns, indexes, column_types = await conn.run_sync(inspect)

    await engine.dispose()

    assert columns == {
        "id",
        "user_id",
        "metric_type",
        "value",
        "recorded_at",
        "created_at",
        "updated_at",
    }
    assert "ix_metrics_user_recorded" in indexes
    assert "ix_metrics_user_type_recorded" in indexes

    assert isinstance(column_types["value"], sa.Float)
    assert column_types["recorded_at"].timezone is True
    assert column_types["created_at"].timezone is True
    assert column_types["updated_at"].timezone is True
    assert set(column_types["metric_type"].enums) == {
        "weight",
        "sleep",
        "heart_rate",
        "steps",
        "water",
    }
