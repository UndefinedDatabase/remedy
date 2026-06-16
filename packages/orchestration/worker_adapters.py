"""
Worker Adapter Foundation v0 — provider-neutral worker specifications.

Defines WorkerProviderSpec as a data-only description of external worker
providers (LLM services, local processes, future harnesses).  No network
calls, no secrets, no shell execution, no actual provider connections.

Provider-neutral: specs describe capabilities and roles without binding
to any specific provider SDK, API key, or endpoint.

Public API::

    list_worker_specs() -> tuple[WorkerProviderSpec, ...]
    export_worker_specs_json(specs) -> dict[str, Any]
    summarize_worker_specs(specs) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkerProviderSpec:
    """Immutable, provider-neutral specification for a worker provider.

    This is metadata only — no connection, no secrets, no execution.
    """

    provider_id: str
    display_name: str
    supported_roles: tuple[str, ...]
    execution_mode: str
    status: str
    notes: str


# ---------------------------------------------------------------------------
# Built-in future specs (data only, no connections)
# ---------------------------------------------------------------------------

_SPECS: tuple[WorkerProviderSpec, ...] = (
    WorkerProviderSpec(
        provider_id="ollama",
        display_name="Ollama (local)",
        supported_roles=("planner", "builder", "reviewer"),
        execution_mode="local_process",
        status="available",
        notes="Local LLM inference via Ollama. Currently used for planning.",
    ),
    WorkerProviderSpec(
        provider_id="claude_code",
        display_name="Claude Code (external harness)",
        supported_roles=("builder", "reviewer", "refactorer"),
        execution_mode="external_harness",
        status="future",
        notes="Anthropic Claude Code CLI as external build worker. Not yet integrated.",
    ),
    WorkerProviderSpec(
        provider_id="pi_dev",
        display_name="Pi Dev (local agent)",
        supported_roles=("builder", "reviewer"),
        execution_mode="local_process",
        status="future",
        notes="Local development agent. Not yet integrated.",
    ),
    WorkerProviderSpec(
        provider_id="copilot",
        display_name="GitHub Copilot (API)",
        supported_roles=("builder", "completer"),
        execution_mode="api",
        status="future",
        notes="GitHub Copilot API integration. Not yet integrated.",
    ),
    WorkerProviderSpec(
        provider_id="openai_api",
        display_name="OpenAI API",
        supported_roles=("planner", "builder", "reviewer"),
        execution_mode="api",
        status="future",
        notes="OpenAI API integration. Not yet integrated.",
    ),
)


def list_worker_specs() -> tuple[WorkerProviderSpec, ...]:
    """Return all known worker provider specifications.

    Deterministic, no network, no filesystem.
    """
    return _SPECS


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_worker_specs_json(specs: tuple[WorkerProviderSpec, ...] | None = None) -> dict[str, Any]:
    """Export worker specs as JSON-serializable dict with version envelope."""
    if specs is None:
        specs = _SPECS
    return {
        "version": 1,
        "providers": [
            {
                "provider_id":     s.provider_id,
                "display_name":    s.display_name,
                "supported_roles": list(s.supported_roles),
                "execution_mode":  s.execution_mode,
                "status":          s.status,
                "notes":           s.notes,
            }
            for s in specs
        ],
    }


def summarize_worker_specs(specs: tuple[WorkerProviderSpec, ...] | None = None) -> str:
    """Return a human-readable summary of worker provider specs."""
    if specs is None:
        specs = _SPECS

    lines: list[str] = []
    lines.append("Worker Adapters")
    lines.append(f"  Providers: {len(specs)}")

    for s in specs:
        status_icon = "+" if s.status == "available" else "~" if s.status == "future" else "?"
        lines.append(f"  {status_icon} {s.display_name} ({s.provider_id})")
        lines.append(f"      Roles: {', '.join(s.supported_roles)}")
        lines.append(f"      Mode:  {s.execution_mode}")
        lines.append(f"      Status: {s.status}")
        if s.notes:
            lines.append(f"      Notes: {s.notes}")

    return "\n".join(lines)
