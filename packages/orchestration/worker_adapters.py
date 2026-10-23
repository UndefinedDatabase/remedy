"""
The worker adapter contract v2's list of workers — provider-neutral worker specifications.

Defines WorkerProviderSpec as a data-only description of worker providers (LLM services, local
processes, external harnesses). No network calls, no secrets, no shell execution, no actual
provider connections. `docs/system/worker-adapter-contract-v2.md` is the page of the same name.

Provider-neutral: specs describe capabilities and roles without binding
to any specific provider SDK, API key, or endpoint.

Public API::

    list_worker_specs() -> tuple[WorkerProviderSpec, ...]
    export_worker_specs_json(specs) -> dict[str, Any]
    summarize_worker_specs(specs) -> str

A ``WorkerProviderSpec`` DESCRIBES a worker — its roles and status — and says
nothing about running one. Its ``adapter_ref`` names the adapter
(`packages/contracts/adapter_contract.py`'s ``WorkerAdapter``) that EXECUTES the
contract for it; a record without a reference is a worker still awaiting its
adapter (DECISION F151 D5 (1)), and its notes say so (amend1023 D4).
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
    #: The v2 adapter's stable name (DECISION F151 D5 (1)); "" when this worker has none yet.
    adapter_ref: str = ""


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
        notes=("Local LLM inference via Ollama, used today for planning and reviewing through "
               "Remedy's own call path. No worker adapter yet."),
    ),
    WorkerProviderSpec(
        provider_id="claude_code",
        display_name="Claude Code (external harness)",
        supported_roles=("builder", "reviewer", "refactorer"),
        execution_mode="external_harness",
        status="available",
        notes=("Anthropic Claude Code CLI as builder and reviewer; its reference adapter "
               "claude-cli builds the command line of every call the loop makes and maps the "
               "usage of every call that is not streamed."),
        adapter_ref="claude-cli",
    ),
    WorkerProviderSpec(
        provider_id="pi_dev",
        display_name="Pi Dev (local agent)",
        supported_roles=("builder", "reviewer"),
        execution_mode="local_process",
        status="available",
        notes=("The Pi harness inside Remedy's tool sandbox, today's default builder and "
               "reviewer, through Remedy's own call path. No worker adapter yet."),
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
                "adapter_ref":     s.adapter_ref,
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
        if s.adapter_ref:
            lines.append(f"      Adapter: {s.adapter_ref}")

    return "\n".join(lines)
