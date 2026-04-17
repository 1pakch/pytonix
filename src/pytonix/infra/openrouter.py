"""OpenRouter API client."""

import os
import httpx
import msgspec
from typing import Optional

from ..domain.llms import LlmChatTranscript, LlmMessage

# API configuration
DEFAULT_MODEL = "qwen/qwen3-coder-next"
CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS_URL = "https://openrouter.ai/api/v1/models"

# Cache for models list
_MODELS_CACHE: list[dict] | None = None


class OpenRouterError(Exception):
    pass


def get_api_key() -> str:
    """Get OpenRouter API key from environment.

    Raises:
        OpenRouterError: If API key is not set.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise OpenRouterError("OPENROUTER_API_KEY environment variable not set")
    return api_key


def _send_request(request: httpx.Request, timeout_seconds: float) -> dict:
    """Send an HTTP request and return the JSON response.

    Raises:
        OpenRouterError: If the request fails.
    """
    try:
        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.send(request)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        # Try to extract error message from API response
        try:
            error_data = e.response.json()
            api_error = error_data.get("error", {}).get("message", str(e))
            error_msg = f"OpenRouter API error: {api_error}"
        except Exception:
            error_msg = f"HTTP error: {e}"
        raise OpenRouterError(error_msg) from e
    except httpx.HTTPError as e:
        raise OpenRouterError(f"HTTP error: {e}") from e
    except Exception as e:
        raise OpenRouterError(f"Request failed: {e}") from e


def _make_chat_request(
    model: str, messages: list[LlmMessage], timeout_seconds: float
) -> str:
    """Make a chat completion request and return the response content.

    Raises:
        OpenRouterError: If the request fails.
    """
    api_key = get_api_key()
    payload = {"model": model, "messages": messages}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # Use msgspec to encode the payload (handles LlmMessage structs)
    content = msgspec.json.encode(payload)
    request = httpx.Request(
        "POST", CHAT_COMPLETIONS_URL, headers=headers, content=content
    )

    try:
        data = _send_request(request, timeout_seconds)
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise OpenRouterError(f"Unexpected response format: {e}") from e


class LiveLlmChat:
    """A stateful chat session with an LLM."""

    def __init__(
        self,
        model: str,
        provider: str = "openrouter",
        system_prompt: str | None = None,
    ):
        self.model = model
        self.provider = provider
        self.messages: list[LlmMessage] = []

        # Store system prompt as the first message if provided
        if system_prompt:
            self.messages.append(LlmMessage(role="system", content=system_prompt))

    def send_message(self, content: str, timeout_seconds: float = 60.0) -> str:
        """Send a user message and get the assistant's response.

        The user message is added to history before the API call.
        If the API call fails, the user message remains in history.

        Raises:
            OpenRouterError: If the API request fails.
        """
        # Add user message to history
        self.messages.append(LlmMessage(role="user", content=content))

        # Make request with all messages (including system prompt if present)
        response_content = _make_chat_request(
            self.model, self.messages, timeout_seconds
        )

        # Add assistant response to history
        self.messages.append(LlmMessage(role="assistant", content=response_content))

        return response_content

    def transcript(self) -> LlmChatTranscript:
        """Export the current chat as an immutable transcript.

        Extracts system prompt from messages if present.
        """
        # Extract system prompt if first message is a system message
        system_prompt = None
        messages = self.messages
        if messages and messages[0].role == "system":
            system_prompt = messages[0].content
            messages = messages[1:]  # Exclude system message from transcript messages

        return LlmChatTranscript(
            model=self.model,
            provider=self.provider,
            messages=list(messages),  # Create a copy
            system_prompt=system_prompt,
        )


def complete_chat(
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str | None = None,
    timeout_seconds: float = 60.0,
) -> str:
    """Send a one-shot chat completion request and return the response.

    Raises:
        OpenRouterError: If the API request fails.
    """
    chat = LiveLlmChat(model=model, system_prompt=system_prompt)
    return chat.send_message(user_prompt, timeout_seconds=timeout_seconds)


def list_models(timeout_seconds: float = 30.0) -> list[dict]:
    """Fetch available models from OpenRouter.

    Uses cached results after the first successful call.

    Raises:
        OpenRouterError: If the API request fails.
    """
    global _MODELS_CACHE

    if _MODELS_CACHE is not None:
        return _MODELS_CACHE

    api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    request = httpx.Request(
        "GET",
        MODELS_URL,
        headers=headers,
    )

    data = _send_request(request, timeout_seconds)
    _MODELS_CACHE = data.get("data", [])
    return _MODELS_CACHE
