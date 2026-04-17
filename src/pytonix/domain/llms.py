from datetime import datetime
from typing import Literal, Any
import msgspec


class LlmMessage(msgspec.Struct, frozen=True):
    "A single message in a chat history."

    role: Literal["system", "user", "assistant"]
    content: str  # tool use-related structured messages could be added via union


class LlmChatTranscript(msgspec.Struct):
    "A transcript of a chat with an LLM model."

    model: str
    provider: str
    messages: list[LlmMessage]
    system_prompt: str | None = None
    extra_sampling_params: dict[str, Any] = msgspec.field(default_factory=dict)


class AttemptLlmTrace(msgspec.Struct, frozen=True):
    """A record of all LLM interactions in a single attempt.

    We might want to add total tokens and cost information etc.
    """

    chats: list[LlmChatTranscript]
