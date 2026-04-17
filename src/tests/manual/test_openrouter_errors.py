"""Manual test for OpenRouter error handling.

Requires OPENROUTER_API_KEY environment variable.
Run: pytest tests/manual/test_openrouter_errors.py -v
"""

import pytest
from pytonix.infra.openrouter import LiveLlmChat, OpenRouterError

GEMMA3_4B_FREE = "google/gemma-3-4b-it:free"


def test_gemma_with_system_prompt_fails():
    """Gemma doesn't support system prompts - should get clear error."""
    with pytest.raises(OpenRouterError) as exc_info:
        chat = LiveLlmChat(GEMMA3_4B_FREE, system_prompt="Reply in French")
        chat.send_message("Hello there")

    error = exc_info.value
    assert error.provider_name == "Google AI Studio"
    assert "Developer instruction" in error.provider_error
    print(f"\nError message: {error}")


def test_gemma_without_system_prompt_succeeds():
    """Gemma without system prompt - should work."""
    chat = LiveLlmChat(GEMMA3_4B_FREE)
    response = chat.send_message("Say hello in one word")
    assert response
    assert len(response) > 0
    print(f"\nResponse: {response}")
