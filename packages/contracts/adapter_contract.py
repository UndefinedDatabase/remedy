"""The worker adapter contract (F151 T002, DECISION F151 D2).

The ping-pong loop and its seams own transport, timeout computation, every
retry (transport, failover, and the reviewer's one parse retry), rate pacing
and per-call evidence; none of that is rebuilt here. A ``WorkerAdapter`` only
builds an invocation and maps a provider's raw output back onto typed shapes:
it takes no timeout, never sleeps or loops on a failure, and never opens a
process or a socket itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.stream_evidence import (
    EVENT_API_RETRY,
    EVENT_CAP_REACHED,
    EVENT_DEGRADED,
    EVENT_MALFORMED,
    EVENT_PROVIDER_ERROR,
    EVENT_RESULT,
    EVENT_TOKEN_USAGE,
    EVENT_TOOL_RESULT,
    EVENT_TOOL_USE,
)
from packages.orchestration.token_actuals import UsageActuals

#: The two roles the loop ever calls an adapter for; any other value is a bug, not a config choice.
ADAPTER_ROLES = ("builder", "reviewer")

#: Every event type a mapped stream may emit — named once in stream_evidence.py, read here by name.
STREAM_EVENT_TYPES = frozenset({
    EVENT_TOOL_USE,
    EVENT_TOOL_RESULT,
    EVENT_API_RETRY,
    EVENT_TOKEN_USAGE,
    EVENT_RESULT,
    EVENT_PROVIDER_ERROR,
    EVENT_MALFORMED,
    EVENT_CAP_REACHED,
    EVENT_DEGRADED,
})

#: The final-failure classes an adapter's classify_error may return; the rest of FailureClass
#: (worktree, config, resource, ...) belongs to layers an adapter never touches.
ADAPTER_ERROR_CLASSES = frozenset({
    FailureClass.PROVIDER_UNAVAILABLE,
    FailureClass.PROVIDER_TIMEOUT,
    FailureClass.PROVIDER_NONZERO_EXIT,
    FailureClass.PARSE,
    FailureClass.UNKNOWN,
})


@dataclass(frozen=True)
class AdapterCapabilities:
    """What one model/provider pair honestly supports, declared rather than assumed."""

    vision: bool
    json_schema: bool
    session_resume: bool
    streaming: bool
    tool_use: bool
    max_context_tokens: int


@dataclass(frozen=True)
class InvocationOptions:
    """Per-call options an adapter may read. Carries no timeout by construction (D2 (3))."""

    model: str
    output_schema: dict | None = None
    resume_ref: str | None = None
    max_output_chars: int = 50000


@dataclass(frozen=True)
class CliInvocation:
    """A subprocess invocation: the argv to run, and optional piped stdin."""

    argv: tuple[str, ...]
    stdin_text: str = ""


@dataclass(frozen=True)
class HttpInvocation:
    """An HTTP invocation: method, url, a JSON-serializable body, and optional headers.

    ``body`` has no default and so is declared before ``headers``, which does — the field
    order the dataclass machinery requires differs from D2 (3)'s prose order for this reason.
    """

    method: str
    url: str
    body: dict
    headers: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class AdapterUsage:
    """A mapped usage answer: the typed actuals plus the provider's own raw counters."""

    actuals: UsageActuals
    raw_counters: dict


#: The sum type build_invocation returns: a process to spawn, or a request to send.
AdapterInvocation = CliInvocation | HttpInvocation


@runtime_checkable
class WorkerAdapter(Protocol):
    """What every provider adapter promises the ping-pong loop (D2 (3))."""

    @property
    def adapter_id(self) -> str:
        """This adapter's stable name: lower-case letters, digits and hyphens."""
        ...

    def capabilities(self, model: str) -> AdapterCapabilities:
        """Declare what this model honestly supports."""
        ...

    def build_invocation(
        self, role: str, prompt_parts: tuple[str, ...], options: InvocationOptions,
    ) -> AdapterInvocation:
        """Build a CLI or HTTP invocation for one role; raise ValueError outside ADAPTER_ROLES."""
        ...

    def map_stream(self, raw_lines: tuple[str, ...]) -> tuple[dict, ...]:
        """Map raw provider stream lines onto STREAM_EVENT_TYPES events; empty when not streaming."""
        ...

    def map_usage(self, raw: str) -> AdapterUsage | None:
        """Map raw provider usage output onto AdapterUsage, or None when none is present."""
        ...

    def classify_error(self, error_text: str, exit_code: int | None) -> FailureClass:
        """Classify a failed call into one of ADAPTER_ERROR_CLASSES."""
        ...

    def isolation(self) -> None:
        """Reserved for F152; returns None until F152 shapes an isolation declaration."""
        ...
