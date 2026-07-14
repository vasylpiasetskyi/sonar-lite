import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


async def test_metrics_table_has_expected_columns_and_indexes() -> None:
    engine = create_async_engine(settings.database_url)

    async with engine.connect() as conn:

        def inspect(sync_conn: sa.Connection) -> tuple[set[str], set[str]]:
            inspector = sa.inspect(sync_conn)
            columns = {c["name"] for c in inspector.get_columns("metrics")}
            indexes = {i["name"] for i in inspector.get_indexes("metrics")}
            return columns, indexes

        columns, indexes = await conn.run_sync(inspect)

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
