from httpx import ASGITransport, AsyncClient

from app.core.db import get_db
from app.main import app


async def _client(db_session) -> AsyncClient:
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


async def test_register_returns_201_with_token(db_session) -> None:
    async with await _client(db_session) as client:
        response = await client.post(
            "/auth/register", json={"email": "person@example.com", "password": "longenough"}
        )

    assert response.status_code == 201
    body = response.json()
    assert body["user"]["email"] == "person@example.com"
    assert body["access_token"]
    assert body["token_type"] == "bearer"

    app.dependency_overrides.clear()


async def test_register_rejects_duplicate_email(db_session) -> None:
    async with await _client(db_session) as client:
        await client.post(
            "/auth/register", json={"email": "person@example.com", "password": "longenough"}
        )
        response = await client.post(
            "/auth/register", json={"email": "person@example.com", "password": "different"}
        )

    assert response.status_code == 409
    app.dependency_overrides.clear()


async def test_login_succeeds_with_correct_credentials(db_session) -> None:
    async with await _client(db_session) as client:
        await client.post(
            "/auth/register", json={"email": "person@example.com", "password": "longenough"}
        )
        response = await client.post(
            "/auth/login", json={"email": "person@example.com", "password": "longenough"}
        )

    assert response.status_code == 200
    assert response.json()["access_token"]
    app.dependency_overrides.clear()


async def test_login_rejects_wrong_password(db_session) -> None:
    async with await _client(db_session) as client:
        await client.post(
            "/auth/register", json={"email": "person@example.com", "password": "longenough"}
        )
        response = await client.post(
            "/auth/login", json={"email": "person@example.com", "password": "wrong-password"}
        )

    assert response.status_code == 401
    app.dependency_overrides.clear()
