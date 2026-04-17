import msgspec

from typing import Any
from .packaging import PythonPackagingTask, NixFlake
from .llms import AttemptLlmTrace


class HumanAuthored(msgspec.Struct, frozen=True, tag=True):
    "Metadata on human-produced packaging solutions/attempts."

    author_name: str
    notes: str | None = None


class AgentAuthored(msgspec.Struct, frozen=True, tag=True):
    "Metadata on agent-produced packaging solutions/attempts."

    agent_name: str
    llm_trace: AttemptLlmTrace
    agent_config: dict[str, Any] = msgspec.field(default_factory=dict)
    notes: str | None = None


class PackagingAttempt(msgspec.Struct, frozen=True, tag=True):
    "An attempt to solve a packaging task."

    task: PythonPackagingTask
    result: NixFlake | None  # None if agent failed to produce a valid flake
    provenance: HumanAuthored | AgentAuthored
