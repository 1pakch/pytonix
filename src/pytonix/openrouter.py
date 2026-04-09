"""OpenRouter API client."""

import os
import httpx
from typing import Optional


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
        with httpx.Client() as client:
            response = client.send(request, timeout=timeout_seconds)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise OpenRouterError(f"HTTP error: {e}") from e
    except Exception as e:
        raise OpenRouterError(f"Request failed: {e}") from e


def complete_chat(
    user_prompt: str,
    model: str = "anthropic/claude-3.5-sonnet",
    system_prompt: str | None = None,
    timeout_seconds: float = 60.0
) -> str:
    """Send a one-shot chat completion request and return the response.

    Raises:
        OpenRouterError: If the API request fails.
    """
    api_key = get_api_key()

    # Compose the messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    payload = {
        "model": model,
        "messages": messages,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    request = httpx.Request(
        "POST",
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    try:
        data = _send_request(request, timeout_seconds)
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise OpenRouterError(f"Unexpected response format: {e}") from e


def list_models(timeout_seconds: float = 30.0) -> list[dict]:
    """Fetch available models from OpenRouter.

    Raises:
        OpenRouterError: If the API request fails.
    """
    api_key = get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    request = httpx.Request(
        "GET",
        "https://openrouter.ai/api/v1/models",
        headers=headers,
    )

    data = _send_request(request, timeout_seconds)
    return data.get("data", [])
