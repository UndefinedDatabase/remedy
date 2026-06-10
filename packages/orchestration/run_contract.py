"""
Run Contract v1 — deterministic execution-boundary definition for a Remedy job.

A RunContract describes what a run is allowed and not allowed to do.
It is an execution boundary, not a capability promise.

Provider-neutral: no model names, no network calls, no shell execution,
no external processes.  Pure data contract only.

Public API::

    build_default_run_contract(job) -> RunContract
    evaluate_run_action(contract, action, ...) -> RunActionDecision
    export_run_contract_json(contract) -> dict[str, Any]
    summarize_run_contract(contract) -> str
    save_contract(job, contract) -> None
    load_contract(job) -> RunContract | None
    ensure_contract(job) -> RunContract
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from packages.core.models import Job


# ---------------------------------------------------------------------------
# Data model (Step 1048)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunContract:
    """Immutable execution-boundary definition for a single job run.

    Fields are deterministic and JSON-serializable.  No external calls.
    """

    version: int = 1
    contract_id: str = ""
    job_id: str = ""
    scope: str = "job"
    autonomy_level: int = 1
    allowed_actions: tuple[str, ...] = ()
    denied_actions: tuple[str, ...] = ()
    max_loops: int = 10
    max_test_runs: int = 0
    max_runtime_seconds: int = 600
    max_tokens: int = 200_000
    max_cost_cents: int = 500
    allowed_paths: tuple[str, ...] = ()
    denied_paths: tuple[str, ...] = ()
    stop_before_apply: bool = True
    stop_on_unknown_risk: bool = True
    stop_on_medium_risk: bool = False
    prefer_local: bool = True
    no_cloud: bool = True
    model_policy: str = "local_first"
    command_policy: str = "allowlist_only"
    stop_conditions: tuple[str, ...] = ()
    requires_approval_for: tuple[str, ...] = ()
    source: str = ""
    created_at: str = ""
    notes: str = ""


# ---------------------------------------------------------------------------
# Action decision result (Step 1049)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunActionDecision:
    """Result of evaluating an action against the contract."""

    allowed: bool
    status: str  # allowed, blocked, exhausted, unknown
    reason: str
    next_safe_action: str = ""


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DEFAULT_ALLOWED_ACTIONS: tuple[str, ...] = (
    "plan",
    "context",
    "build_artifact",
    "create_patch_intent",
    "discover_commands",
    "write_metadata",
)

_DEFAULT_DENIED_ACTIONS: tuple[str, ...] = (
    "apply",
    "source_apply",
    "arbitrary_shell",
    "apply_patch_without_approval",
    "modify_permissions_autonomously",
    "network_fetch",
    "install_packages",
    "cloud_provider",
)

_DEFAULT_DENIED_PATHS: tuple[str, ...] = (
    ".env",
    ".env.secret",
    ".env.local",
    "credentials.json",
    "secrets.yaml",
    "node_modules/",
    ".git/",
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

_APPLY_ACTIONS = frozenset({"apply", "source_apply", "patch_apply"})
_CLOUD_ACTIONS = frozenset({"cloud_provider", "network_fetch", "install_packages"})


def build_default_run_contract(job: Job) -> RunContract:
    """Build a sensible default RunContract for a job.

    Deterministic — derives contract from job metadata only.
    No LLM calls, no network, no filesystem access.
    """
    return RunContract(
        version=1,
        contract_id=f"rc-{str(job.id)[:8]}",
        job_id=str(job.id),
        scope="job",
        autonomy_level=1,
        allowed_actions=_DEFAULT_ALLOWED_ACTIONS,
        denied_actions=_DEFAULT_DENIED_ACTIONS,
        max_loops=10,
        max_test_runs=0,
        max_runtime_seconds=600,
        max_tokens=200_000,
        max_cost_cents=500,
        allowed_paths=(),
        denied_paths=_DEFAULT_DENIED_PATHS,
        stop_before_apply=True,
        stop_on_unknown_risk=True,
        stop_on_medium_risk=False,
        prefer_local=True,
        no_cloud=True,
        model_policy="local_first",
        command_policy="allowlist_only",
        stop_conditions=_DEFAULT_STOP_CONDITIONS,
        requires_approval_for=_DEFAULT_REQUIRES_APPROVAL,
        source="default_v1",
        created_at=datetime.now(timezone.utc).isoformat(),
        notes="Auto-generated execution boundary. Not yet user-configurable.",
    )


# ---------------------------------------------------------------------------
# Contract persistence (Step 1066)
# ---------------------------------------------------------------------------

_CONTRACT_META_KEY = "run_contract"


def _contract_from_dict(data: dict[str, Any]) -> RunContract:
    """Reconstruct a RunContract from a metadata dict."""
    # Convert list fields back to tuples
    tuple_fields = (
        "allowed_actions", "denied_actions", "allowed_paths", "denied_paths",
        "stop_conditions", "requires_approval_for",
    )
    cleaned = dict(data)
    for field in tuple_fields:
        if field in cleaned and isinstance(cleaned[field], list):
            cleaned[field] = tuple(cleaned[field])
    return RunContract(**cleaned)


def save_contract(job: Job, contract: RunContract) -> None:
    """Store a RunContract in job.metadata. Caller must persist the job."""
    job.metadata[_CONTRACT_META_KEY] = export_run_contract_json(contract)


def load_contract(job: Job) -> RunContract | None:
    """Load the persisted RunContract from job.metadata, or None if absent."""
    data = job.metadata.get(_CONTRACT_META_KEY)
    if not isinstance(data, dict):
        return None
    return _contract_from_dict(data)


def ensure_contract(job: Job) -> RunContract:
    """Return the persisted contract, creating and saving one if absent.

    Guarantees stable contract_id and created_at across reloads.
    Caller must persist the job if this function creates a new contract.
    """
    existing = load_contract(job)
    if existing is not None:
        return existing
    contract = build_default_run_contract(job)
    save_contract(job, contract)
    return contract


def needs_contract_migration(job: Job) -> bool:
    """Check if a job needs contract migration (no persisted contract)."""
    return not isinstance(job.metadata.get(_CONTRACT_META_KEY), dict)


def migrate_contract(job: Job) -> RunContract:
    """Migrate an old job to have a persisted contract.

    Idempotent — returns existing contract if already present.
    Caller must persist the job after calling this.
    """
    return ensure_contract(job)


# ---------------------------------------------------------------------------
# Contract decision helper (Step 1049)
# ---------------------------------------------------------------------------


def evaluate_run_action(
    contract: RunContract,
    action: str,
    *,
    path: str | None = None,
    risk: str | None = None,
    loop_index: int | None = None,
    test_run_count: int | None = None,
) -> RunActionDecision:
    """Evaluate whether an action is allowed under the contract.

    Returns a RunActionDecision with allowed, status, reason, next_safe_action.
    """
    # 1. Denied actions
    if action in contract.denied_actions:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Action '{action}' is in denied_actions",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # 2. Not in allowed actions
    if contract.allowed_actions and action not in contract.allowed_actions:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Action '{action}' not in allowed_actions",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # 3. stop_before_apply blocks apply-type actions
    if contract.stop_before_apply and action in _APPLY_ACTIONS:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason="stop_before_apply blocks apply actions",
            next_safe_action="remedy patch approve <job_id> <intent_id>",
        )

    # 4. no_cloud blocks cloud actions
    if contract.no_cloud and action in _CLOUD_ACTIONS:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason="no_cloud blocks cloud/provider actions",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # 5. Loop budget
    if loop_index is not None and loop_index >= contract.max_loops:
        return RunActionDecision(
            allowed=False,
            status="exhausted",
            reason=f"Loop index {loop_index} >= max_loops {contract.max_loops}",
            next_safe_action="remedy job show <job_id> --json",
        )

    # 6. Test run budget
    if test_run_count is not None and test_run_count >= contract.max_test_runs:
        return RunActionDecision(
            allowed=False,
            status="exhausted",
            reason=f"Test runs {test_run_count} >= max_test_runs {contract.max_test_runs}",
            next_safe_action="remedy job show <job_id> --json",
        )

    # 7. Path policy
    if path is not None:
        path_decision = _check_path_policy(contract, path)
        if path_decision is not None:
            return path_decision

    # 8. Risk policy
    if risk is not None:
        risk_lower = risk.lower()
        if risk_lower == "unknown" and contract.stop_on_unknown_risk:
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason="stop_on_unknown_risk blocks unknown-risk actions",
                next_safe_action="remedy contract inspect <job_id> --json",
            )
        if risk_lower in ("medium", "high") and contract.stop_on_medium_risk:
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason=f"stop_on_medium_risk blocks {risk_lower}-risk actions",
                next_safe_action="remedy contract inspect <job_id> --json",
            )

    return RunActionDecision(
        allowed=True,
        status="allowed",
        reason=f"Action '{action}' permitted by contract",
    )


def _check_path_policy(contract: RunContract, path: str) -> RunActionDecision | None:
    """Check path against allowed/denied path policies. Returns decision if blocked."""
    normalized = os.path.normpath(path)

    # Block absolute paths
    if os.path.isabs(normalized):
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Absolute path '{normalized}' blocked by policy",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # Block traversal
    if ".." in normalized.split(os.sep):
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Path traversal in '{normalized}' blocked by policy",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # Denied paths win over allowed paths
    for denied in contract.denied_paths:
        if normalized == denied or normalized.startswith(denied.rstrip("/") + "/") or normalized.startswith(denied):
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason=f"Path '{normalized}' matches denied path '{denied}'",
                next_safe_action="remedy contract inspect <job_id> --json",
            )

    # If allowed_paths specified, path must match
    if contract.allowed_paths:
        matched = False
        for allowed in contract.allowed_paths:
            if normalized == allowed or normalized.startswith(allowed.rstrip("/") + "/"):
                matched = True
                break
        if not matched:
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason=f"Path '{normalized}' not in allowed_paths",
                next_safe_action="remedy contract inspect <job_id> --json",
            )

    return None


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_run_contract_json(contract: RunContract) -> dict[str, Any]:
    """Export a RunContract as a JSON-serializable dict."""
    return {
        "version":               contract.version,
        "contract_id":           contract.contract_id,
        "job_id":                contract.job_id,
        "scope":                 contract.scope,
        "autonomy_level":        contract.autonomy_level,
        "allowed_actions":       list(contract.allowed_actions),
        "denied_actions":        list(contract.denied_actions),
        "max_loops":             contract.max_loops,
        "max_test_runs":         contract.max_test_runs,
        "max_runtime_seconds":   contract.max_runtime_seconds,
        "max_tokens":            contract.max_tokens,
        "max_cost_cents":        contract.max_cost_cents,
        "allowed_paths":         list(contract.allowed_paths),
        "denied_paths":          list(contract.denied_paths),
        "stop_before_apply":     contract.stop_before_apply,
        "stop_on_unknown_risk":  contract.stop_on_unknown_risk,
        "stop_on_medium_risk":   contract.stop_on_medium_risk,
        "prefer_local":          contract.prefer_local,
        "no_cloud":              contract.no_cloud,
        "model_policy":          contract.model_policy,
        "command_policy":        contract.command_policy,
        "stop_conditions":       list(contract.stop_conditions),
        "requires_approval_for": list(contract.requires_approval_for),
        "source":                contract.source,
        "created_at":            contract.created_at,
        "notes":                 contract.notes,
    }


def export_run_action_decision_json(decision: RunActionDecision) -> dict[str, Any]:
    """Export action decision as JSON dict."""
    return {
        "allowed": decision.allowed,
        "status": decision.status,
        "reason": decision.reason,
        "next_safe_action": decision.next_safe_action,
    }


def summarize_run_contract(contract: RunContract) -> str:
    """Return a human-readable summary of the RunContract."""
    lines: list[str] = []
    lines.append("Run Contract")
    lines.append(f"  Version:         {contract.version}")
    lines.append(f"  Contract ID:     {contract.contract_id}")
    lines.append(f"  Job:             {contract.job_id[:8]}")
    lines.append(f"  Scope:           {contract.scope}")
    lines.append(f"  Autonomy:        {contract.autonomy_level}")
    lines.append(f"  Model policy:    {contract.model_policy}")
    lines.append(f"  Command policy:  {contract.command_policy}")
    lines.append(f"  Max loops:       {contract.max_loops}")
    lines.append(f"  Max test runs:   {contract.max_test_runs}")
    lines.append(f"  Max runtime:     {contract.max_runtime_seconds}s")
    lines.append(f"  Max tokens:      {contract.max_tokens:,}")
    lines.append(f"  Max cost:        {contract.max_cost_cents} cents")
    lines.append(f"  Stop before apply: {contract.stop_before_apply}")
    lines.append(f"  Stop on unknown risk: {contract.stop_on_unknown_risk}")
    lines.append(f"  Stop on medium risk:  {contract.stop_on_medium_risk}")
    lines.append(f"  Prefer local:    {contract.prefer_local}")
    lines.append(f"  No cloud:        {contract.no_cloud}")
    lines.append(f"  Source:          {contract.source}")

    lines.append("  Allowed actions:")
    for a in contract.allowed_actions:
        lines.append(f"    + {a}")

    lines.append("  Denied actions:")
    for d in contract.denied_actions:
        lines.append(f"    - {d}")

    if contract.allowed_paths:
        lines.append("  Allowed paths:")
        for p in contract.allowed_paths:
            lines.append(f"    + {p}")

    if contract.denied_paths:
        lines.append("  Denied paths:")
        for p in contract.denied_paths:
            lines.append(f"    - {p}")

    lines.append("  Stop conditions:")
    for s in contract.stop_conditions:
        lines.append(f"    * {s}")

    lines.append("  Requires approval for:")
    for r in contract.requires_approval_for:
        lines.append(f"    ! {r}")

    if contract.notes:
        lines.append(f"  Notes: {contract.notes}")

    return "\n".join(lines)
