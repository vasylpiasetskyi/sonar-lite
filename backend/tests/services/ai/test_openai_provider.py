from unittest.mock import AsyncMock, MagicMock, patch

from app.services.ai.providers import OpenAIProvider


async def test_openai_provider_sends_correct_request_and_extracts_content() -> None:
    mock_message = MagicMock()
    mock_message.content = '{"summary": "ok"}'
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch("app.services.ai.providers.AsyncOpenAI") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        provider = OpenAIProvider(api_key="test-key", model="gpt-4o-mini")
        result = await provider.complete("test prompt")

        assert result == '{"summary": "ok"}'
        mock_client_cls.assert_called_once_with(api_key="test-key")
        mock_client.chat.completions.create.assert_awaited_once_with(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test prompt"}],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
