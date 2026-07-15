from typing import Protocol

from openai import AsyncOpenAI


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


class OpenAIProvider:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def complete(self, prompt: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        return content or ""
