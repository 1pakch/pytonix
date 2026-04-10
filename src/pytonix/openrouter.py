"""OpenRouter API client."""

import os
import httpx
from typing import Optional

# API configuration
DEFAULT_MODEL = "qwen/qwen3-coder-next"
CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS_URL = "https://openrouter.ai/api/v1/models"


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


def complete_chat(
    user_prompt: str,
    model: str = DEFAULT_MODEL,
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
        CHAT_COMPLETIONS_URL,
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
        MODELS_URL,
        headers=headers,
    )

    data = _send_request(request, timeout_seconds)
    return data.get("data", [])
