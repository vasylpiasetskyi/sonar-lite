from datetime import datetime, timezone

from httpx import ASGITransport, AsyncClient

from app.core.db import get_db
from app.main import app


async def _client(db_session) -> AsyncClient:
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


async def test_get_dashboard_returns_full_contract_shape(db_session) -> None:
    async with await _client(db_session) as client:
        response = await client.get("/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert "latest" in body
    assert "metrics" in body
    assert "health_score" in body
    assert body["ai_summary"] is None
    assert set(body["latest"].keys()) == {"weight", "sleep", "heart_rate", "steps", "water"}

    app.dependency_overrides.clear()


async def test_get_dashboard_reflects_created_metric(db_session) -> None:
    async with await _client(db_session) as client:
        await client.post(
            "/metrics",
            json={
                "metric_type": "steps",
                "value": 9000,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        response = await client.get("/dashboard")

    body = response.json()
    assert body["latest"]["steps"]["value"] == 9000.0
    assert body["metrics"]["steps"]["avg_7d"] == 9000.0

    app.dependency_overrides.clear()
