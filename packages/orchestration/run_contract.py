"""
Run Contract v0 — deterministic execution-boundary definition for a Remedy job.

A RunContract describes what a run is allowed and not allowed to do.
It is an execution boundary, not a capability promise.

Provider-neutral: no model names, no network calls, no shell execution,
no external processes.  Pure data contract only.

Public API::

    build_default_run_contract(job) -> RunContract
    export_run_contract_json(contract) -> dict[str, Any]
    summarize_run_contract(contract) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunContract:
    """Immutable execution-boundary definition for a single job run.

    Fields are deterministic and JSON-serializable.  No external calls.
    """

    version: int
    job_id: str
    scope: str
    autonomy_level: int
    allowed_actions: tuple[str, ...]
    denied_actions: tuple[str, ...]
    max_loops: int
    max_tokens: int
    max_cost_cents: int
    model_policy: str
    command_policy: str
    stop_conditions: tuple[str, ...]
    requires_approval_for: tuple[str, ...]
    source: str
    notes: str


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DEFAULT_ALLOWED_ACTIONS: tuple[str, ...] = (
    "plan",
    "build_artifact",
    "create_patch_intent",
    "apply_approved_markdown_patch",
    "run_tests_local",
    "discover_commands",
)

_DEFAULT_DENIED_ACTIONS: tuple[str, ...] = (
    "arbitrary_shell",
    "apply_patch_without_approval",
    "modify_permissions_autonomously",
    "network_fetch",
    "install_packages",
)

_DEFAULT_STOP_CONDITIONS: tuple[str, ...] = (
    "max_loops_exceeded",
    "max_tokens_exceeded",
    "max_cost_exceeded",
    "all_tasks_completed",
    "permission_denied_unresolvable",
)

_DEFAULT_REQUIRES_APPROVAL: tuple[str, ...] = (
    "patch_apply",
    "high_risk_command_execution",
)


def build_default_run_contract(job: Job) -> RunContract:
    """Build a sensible default RunContract for a job.

    Deterministic — derives contract from job metadata only.
    No LLM calls, no network, no filesystem access.
    """
    return RunContract(
        version=1,
        job_id=str(job.id),
        scope="job",
        autonomy_level=1,
        allowed_actions=_DEFAULT_ALLOWED_ACTIONS,
        denied_actions=_DEFAULT_DENIED_ACTIONS,
        max_loops=10,
        max_tokens=200_000,
        max_cost_cents=500,
        model_policy="local_first",
        command_policy="allowlist_only",
        stop_conditions=_DEFAULT_STOP_CONDITIONS,
        requires_approval_for=_DEFAULT_REQUIRES_APPROVAL,
        source="default_v1",
        notes="Auto-generated execution boundary. Not yet user-configurable.",
    )


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_run_contract_json(contract: RunContract) -> dict[str, Any]:
    """Export a RunContract as a JSON-serializable dict."""
    return {
        "version":               contract.version,
        "job_id":                contract.job_id,
        "scope":                 contract.scope,
        "autonomy_level":        contract.autonomy_level,
        "allowed_actions":       list(contract.allowed_actions),
        "denied_actions":        list(contract.denied_actions),
        "max_loops":             contract.max_loops,
        "max_tokens":            contract.max_tokens,
        "max_cost_cents":        contract.max_cost_cents,
        "model_policy":          contract.model_policy,
        "command_policy":        contract.command_policy,
        "stop_conditions":       list(contract.stop_conditions),
        "requires_approval_for": list(contract.requires_approval_for),
        "source":                contract.source,
        "notes":                 contract.notes,
    }


def summarize_run_contract(contract: RunContract) -> str:
    """Return a human-readable summary of the RunContract."""
    lines: list[str] = []
    lines.append("Run Contract")
    lines.append(f"  Version:         {contract.version}")
    lines.append(f"  Job:             {contract.job_id[:8]}")
    lines.append(f"  Scope:           {contract.scope}")
    lines.append(f"  Autonomy:        {contract.autonomy_level}")
    lines.append(f"  Model policy:    {contract.model_policy}")
    lines.append(f"  Command policy:  {contract.command_policy}")
    lines.append(f"  Max loops:       {contract.max_loops}")
    lines.append(f"  Max tokens:      {contract.max_tokens:,}")
    lines.append(f"  Max cost:        {contract.max_cost_cents} cents")
    lines.append(f"  Source:          {contract.source}")

    lines.append("  Allowed actions:")
    for a in contract.allowed_actions:
        lines.append(f"    + {a}")

    lines.append("  Denied actions:")
    for d in contract.denied_actions:
        lines.append(f"    - {d}")

    lines.append("  Stop conditions:")
    for s in contract.stop_conditions:
        lines.append(f"    * {s}")

    lines.append("  Requires approval for:")
    for r in contract.requires_approval_for:
        lines.append(f"    ! {r}")

    if contract.notes:
        lines.append(f"  Notes: {contract.notes}")

    return "\n".join(lines)
