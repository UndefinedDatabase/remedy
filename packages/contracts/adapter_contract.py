"""The worker adapter contract (F151 T002, DECISION F151 D2).

The ping-pong loop and its seams own transport, timeout computation, every
retry (transport, failover, and the reviewer's one parse retry), rate pacing
and per-call evidence; none of that is rebuilt here. A ``WorkerAdapter`` only
builds an invocation and maps a provider's raw output back onto typed shapes:
it takes no timeout, never sleeps or loops on a failure, and never opens a
process or a socket itself.

A v1 ``WorkerProviderSpec`` (`packages/orchestration/worker_adapters.py`) DESCRIBES a
worker — its roles and status — and says nothing about running one. Its ``adapter_ref``
names the v2 ``WorkerAdapter`` that EXECUTES the contract for it; a record without a
reference is a worker still awaiting its adapter (DECISION F151 D5 (1)).
"""
from __future__ import annotations

import re
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

#: The three ways a worker's call keeps the operator's own configuration and secrets out of it
#: (DECISION F152 D3 (1)); any other string is a bug, not a config choice.
ISOLATION_METHODS = ("tool_flag", "clean_env", "sandbox_reinforced")

#: `WorkerIsolation.adr_ref` must fully match this: `docs/adr/`, four digits, `-`, lower-case
#: words joined by `-`, `.md` — the one shape an isolation record's own research page may take.
_ADR_REF_PATTERN = re.compile(r"^docs/adr/\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


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


# WHY: one declared shape for how far a worker's call keeps the operator's own configuration and
# secrets out of it, so a route reads one typed answer instead of trusting an adapter's prose
# (DECISION F152 D3 (1)).
@dataclass(frozen=True)
class WorkerIsolation:
    """How one adapter isolates a worker's call: which of ISOLATION_METHODS, the record that
    backs the choice, and what the method actually does to the call line or the environment.
    `applies` lets a route turn isolation off for one call (e.g. the operator's own documented
    customization switch) without a second declaration."""

    method: str
    adr_ref: str
    tool_args: tuple[str, ...] = ()
    env_allowlist: tuple[str, ...] = ()
    throwaway_home: bool = False
    applies: bool = True

    def __post_init__(self) -> None:
        if self.method not in ISOLATION_METHODS:
            raise ValueError(f"unknown isolation method: {self.method!r}")
        if not _ADR_REF_PATTERN.fullmatch(self.adr_ref):
            raise ValueError(
                f"adr_ref must match docs/adr/NNNN-slug.md: {self.adr_ref!r}")
        for field_name in ("tool_args", "env_allowlist"):
            value = getattr(self, field_name)
            if not isinstance(value, tuple) or not all(
                isinstance(member, str) and member for member in value
            ):
                raise ValueError(
                    f"{field_name} must be a tuple of non-empty strings: {value!r}")
        if self.method == "tool_flag" and not self.tool_args:
            raise ValueError("tool_flag requires tool_args")
        if self.method in ("clean_env", "sandbox_reinforced") and not self.env_allowlist:
            raise ValueError(f"{self.method} requires env_allowlist")
        if self.throwaway_home and self.method == "tool_flag":
            raise ValueError("throwaway_home is not allowed with tool_flag")


# WHY: one declared shape for an adapter's own default sandbox profile and whether its process
# runs inside the tool sandbox, so a route and the conformance kit read one typed answer instead
# of trusting an adapter's prose (DECISION F162 D4 (1)).
@dataclass(frozen=True)
class WorkerSandboxDefault:
    """An adapter's default sandbox profile: TOML text `parse_sandbox_profile` parses with the
    adapter's own `adapter_id` as its name, and whether the adapter's process runs inside the
    tool sandbox. `reason` is required whenever `tool_sandbox` is False, naming why the process
    cannot run inside the sandbox's boundary."""

    profile_toml: str
    tool_sandbox: bool
    reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.profile_toml, str) or not self.profile_toml:
            raise ValueError(f"profile_toml must be a non-empty string: {self.profile_toml!r}")
        if not isinstance(self.tool_sandbox, bool):
            raise ValueError(f"tool_sandbox must be a bool: {self.tool_sandbox!r}")
        if not isinstance(self.reason, str):
            raise ValueError(f"reason must be a string: {self.reason!r}")
        if not self.tool_sandbox and not self.reason:
            raise ValueError("tool_sandbox False requires a non-empty reason")


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

    def isolation(self) -> WorkerIsolation:
        """Declare how this adapter keeps the operator's own configuration and secrets out of a
        worker's call (DECISION F152 D3 (1))."""
        ...

    def sandbox_default(self) -> WorkerSandboxDefault:
        """Declare this adapter's default sandbox profile as TOML text, and whether its process
        runs inside the tool sandbox (DECISION F162 D4 (1))."""
        ...
