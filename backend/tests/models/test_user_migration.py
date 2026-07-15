import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


async def test_users_table_has_expected_columns_and_unique_email_index() -> None:
    engine = create_async_engine(settings.database_url)

    async with engine.connect() as conn:

        def inspect(sync_conn: sa.Connection) -> tuple[set[str], list[dict]]:
            inspector = sa.inspect(sync_conn)
            columns = {c["name"] for c in inspector.get_columns("users")}
            indexes = inspector.get_indexes("users")
            return columns, indexes

        columns, indexes = await conn.run_sync(inspect)

    await engine.dispose()

    assert columns == {"id", "email", "hashed_password", "created_at", "updated_at"}
    email_index = next(i for i in indexes if i["name"] == "ix_users_email")
    assert email_index["unique"] is True
    assert email_index["column_names"] == ["email"]
