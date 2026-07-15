import uuid
from datetime import datetime, timedelta, timezone

import jwt
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.db import get_db
from app.main import app
from tests.auth_helpers import create_test_user_token


async def _client(db_session) -> AsyncClient:
    app.dependency_overrides[get_db] = lambda: db_session
    token = await create_test_user_token(db_session)
    transport = ASGITransport(app=app)
    return AsyncClient(
        transport=transport, base_url="http://test", headers={"Authorization": f"Bearer {token}"}
    )


async def test_create_metric_returns_201(db_session) -> None:
    async with await _client(db_session) as client:
        response = await client.post(
            "/metrics",
            json={
                "metric_type": "sleep",
                "value": 7.5,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert body["value"] == 7.5
    assert body["metric_type"] == "sleep"

    app.dependency_overrides.clear()


async def test_create_metric_rejects_non_positive_value(db_session) -> None:
    async with await _client(db_session) as client:
        response = await client.post(
            "/metrics",
            json={
                "metric_type": "sleep",
                "value": 0,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    assert response.status_code == 422
    app.dependency_overrides.clear()


async def test_update_metric_rejects_non_positive_value(db_session) -> None:
    async with await _client(db_session) as client:
        create_response = await client.post(
            "/metrics",
            json={
                "metric_type": "sleep",
                "value": 7.0,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        metric_id = create_response.json()["id"]

        response = await client.patch(f"/metrics/{metric_id}", json={"value": 0})

    assert response.status_code == 422
    app.dependency_overrides.clear()


async def test_get_metric_returns_404_for_missing_id(db_session) -> None:
    async with await _client(db_session) as client:
        response = await client.get("/metrics/00000000-0000-0000-0000-000000000099")

    assert response.status_code == 404
    app.dependency_overrides.clear()


async def test_list_then_get_then_update_then_delete_roundtrip(db_session) -> None:
    async with await _client(db_session) as client:
        create_response = await client.post(
            "/metrics",
            json={
                "metric_type": "weight",
                "value": 70,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        metric_id = create_response.json()["id"]

        list_response = await client.get("/metrics", params={"metric_type": "weight"})
        assert list_response.json()["total"] >= 1

        get_response = await client.get(f"/metrics/{metric_id}")
        assert get_response.status_code == 200

        patch_response = await client.patch(f"/metrics/{metric_id}", json={"value": 71})
        assert patch_response.json()["value"] == 71

        delete_response = await client.delete(f"/metrics/{metric_id}")
        assert delete_response.status_code == 204

        get_after_delete = await client.get(f"/metrics/{metric_id}")
        assert get_after_delete.status_code == 404

    app.dependency_overrides.clear()


async def test_create_metric_requires_authentication(db_session) -> None:
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/metrics",
            json={
                "metric_type": "sleep",
                "value": 7.0,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    assert response.status_code == 401
    app.dependency_overrides.clear()


async def test_get_metric_rejects_expired_token(db_session) -> None:
    app.dependency_overrides[get_db] = lambda: db_session
    expired_token = jwt.encode(
        {"sub": str(uuid.uuid4()), "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"Authorization": f"Bearer {expired_token}"},
    ) as client:
        response = await client.get("/metrics/00000000-0000-0000-0000-000000000099")

    assert response.status_code == 401
    app.dependency_overrides.clear()


async def test_metric_operations_return_404_for_another_users_metric(db_session) -> None:
    app.dependency_overrides[get_db] = lambda: db_session
    token_a = await create_test_user_token(db_session)
    token_b = await create_test_user_token(db_session)
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url="http://test", headers={"Authorization": f"Bearer {token_a}"}
    ) as client_a:
        create_response = await client_a.post(
            "/metrics",
            json={
                "metric_type": "sleep",
                "value": 7.0,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    metric_id = create_response.json()["id"]

    async with AsyncClient(
        transport=transport, base_url="http://test", headers={"Authorization": f"Bearer {token_b}"}
    ) as client_b:
        get_response = await client_b.get(f"/metrics/{metric_id}")
        patch_response = await client_b.patch(f"/metrics/{metric_id}", json={"value": 8.0})
        delete_response = await client_b.delete(f"/metrics/{metric_id}")

    assert get_response.status_code == 404
    assert patch_response.status_code == 404
    assert delete_response.status_code == 404

    app.dependency_overrides.clear()
