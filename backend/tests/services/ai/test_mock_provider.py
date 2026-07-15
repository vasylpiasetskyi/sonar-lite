from app.services.ai.providers import MockAIProvider


async def test_mock_provider_returns_default_valid_response() -> None:
    provider = MockAIProvider()

    result = await provider.complete("any prompt")

    assert "summary" in result


async def test_mock_provider_returns_responses_in_sequence() -> None:
    provider = MockAIProvider(responses=["first", "second"])

    first = await provider.complete("prompt")
    second = await provider.complete("prompt")

    assert first == "first"
    assert second == "second"


async def test_mock_provider_repeats_last_response_after_sequence_exhausted() -> None:
    provider = MockAIProvider(responses=["only"])

    first = await provider.complete("prompt")
    second = await provider.complete("prompt")

    assert first == "only"
    assert second == "only"
