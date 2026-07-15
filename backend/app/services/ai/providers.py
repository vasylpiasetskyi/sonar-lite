from typing import Protocol


class AIProvider(Protocol):
    async def complete(self, prompt: str) -> str: ...


class MockAIProvider:
    DEFAULT_RESPONSE = (
        '{"summary": "Mock summary.", '
        '"positive_observations": ["Mock positive observation."], '
        '"risks": ["Mock risk."], '
        '"recommendations": ["Mock recommendation."], '
        '"next_week_focus": "Mock focus."}'
    )

    def __init__(self, responses: list[str] | None = None) -> None:
        self._responses = responses if responses is not None else [self.DEFAULT_RESPONSE]
        self._call_count = 0

    async def complete(self, prompt: str) -> str:
        index = min(self._call_count, len(self._responses) - 1)
        response = self._responses[index]
        self._call_count += 1
        return response
