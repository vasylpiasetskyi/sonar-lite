import uuid

from app.repositories.user_repository import UserRepository


async def test_create_persists_user(db_session) -> None:
    repo = UserRepository(db_session)

    user = await repo.create("person@example.com", "hashed-value")

    assert user.id is not None
    assert user.email == "person@example.com"


async def test_get_by_email_returns_none_when_missing(db_session) -> None:
    repo = UserRepository(db_session)

    result = await repo.get_by_email("missing@example.com")

    assert result is None


async def test_get_by_email_finds_created_user(db_session) -> None:
    repo = UserRepository(db_session)
    created = await repo.create("person@example.com", "hashed-value")

    found = await repo.get_by_email("person@example.com")

    assert found is not None
    assert found.id == created.id


async def test_get_by_id_returns_none_when_missing(db_session) -> None:
    repo = UserRepository(db_session)

    result = await repo.get_by_id(uuid.uuid4())

    assert result is None
