from httpx import ASGITransport, AsyncClient

from app.api.ai import get_ai_service
from app.core.db import get_db
from app.main import app
from app.services.ai.ai_service import AIService
from app.services.ai.providers import MockAIProvider

VALID_RESPONSE = (
    '{"summary": "Test summary.", "positive_observations": ["Good sleep."], '
    '"risks": ["Low water."], "recommendations": ["Drink more water."], '
    '"next_week_focus": "Hydration."}'
)


async def _client(db_session) -> AsyncClient:
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


async def test_ai_summary_returns_recommendations_and_summary_on_success(db_session) -> None:
    app.dependency_overrides[get_ai_service] = lambda: AIService(
        MockAIProvider(responses=[VALID_RESPONSE])
    )

    async with await _client(db_session) as client:
        response = await client.post("/ai/summary")

    assert response.status_code == 200
    body = response.json()
    assert "rule_based_recommendations" in body
    assert body["ai_summary"]["summary"] == "Test summary."
    assert (
        body["ai_summary"]["disclaimer"]
        == "Recommendations are informational only, not medical advice."
    )
    assert body["ai_summary_error"] is None

    app.dependency_overrides.clear()


async def test_ai_summary_degrades_gracefully_when_ai_fails(db_session) -> None:
    app.dependency_overrides[get_ai_service] = lambda: AIService(
        MockAIProvider(responses=["not valid json"])
    )

    async with await _client(db_session) as client:
        response = await client.post("/ai/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["ai_summary"] is None
    assert body["ai_summary_error"] is not None
    assert "rule_based_recommendations" in body

    app.dependency_overrides.clear()
