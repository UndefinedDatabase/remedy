"""
Token Economy v0 — deterministic routing policy for a Remedy job.

A TokenPolicy describes how tokens should be allocated across steps:
which steps are zero-token (pure local Python), which use local-first
models, and which justify expensive frontier models.

Provider-neutral: no model names, no network calls, no shell execution,
no external processes.  Pure data contract only.

Public API::

    build_default_token_policy(job) -> TokenPolicy
    export_token_policy_json(policy) -> dict[str, Any]
    summarize_token_policy(policy) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from packages.core.models import Job


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TokenPolicy:
    """Immutable token-routing policy for a single job run.

    Fields are deterministic and JSON-serializable.  No external calls.
    """

    version: int
    job_id: str
    scope: str
    zero_token_steps: tuple[str, ...]
    local_first_steps: tuple[str, ...]
    expensive_model_steps: tuple[str, ...]
    forbidden_context: tuple[str, ...]
    compaction_rules: tuple[str, ...]
    budget: MappingProxyType[str, int]
    future_layers: tuple[str, ...]


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DEFAULT_ZERO_TOKEN: tuple[str, ...] = (
    "command_discovery",
    "risk_assessment",
    "permission_check",
    "patch_intent_creation",
    "context_coverage_derivation",
    "brain_graph_construction",
    "run_contract_inspection",
    "token_policy_inspection",
)

_DEFAULT_LOCAL_FIRST: tuple[str, ...] = (
    "planning",
    "verification",
    "constitution_check",
    "agent_loop_inspection",
)

_DEFAULT_EXPENSIVE: tuple[str, ...] = (
    "artifact_generation",
    "complex_refactoring",
    "multi_file_patch",
)

_DEFAULT_FORBIDDEN_CONTEXT: tuple[str, ...] = (
    "raw_credentials",
    "api_keys",
    "environment_secrets",
    "user_personal_data",
    "raw_command_output",
    "raw_stdout",
    "raw_stderr",
    "artifact_content",
)

_DEFAULT_COMPACTION: tuple[str, ...] = (
    "truncate_large_artifacts_before_context",
    "summarize_long_run_logs",
    "drop_redundant_verification_details",
)

_DEFAULT_FUTURE_LAYERS: tuple[str, ...] = (
    "adaptive_budget_rebalancing",
    "per_task_cost_tracking",
    "model_quality_feedback_loop",
)


def build_default_token_policy(job: Job) -> TokenPolicy:
    """Build a sensible default TokenPolicy for a job.

    Deterministic — derives policy from job metadata only.
    No LLM calls, no network, no filesystem access.
    """
    job_id_str = str(job.id)
    task_count = len(job.tasks) if job.tasks else 0
    scope = "job"

    budget_local = 50_000
    budget_expensive = 100_000
    if task_count > 3:
        budget_expensive = 150_000

    return TokenPolicy(
        version=1,
        job_id=job_id_str,
        scope=scope,
        zero_token_steps=_DEFAULT_ZERO_TOKEN,
        local_first_steps=_DEFAULT_LOCAL_FIRST,
        expensive_model_steps=_DEFAULT_EXPENSIVE,
        forbidden_context=_DEFAULT_FORBIDDEN_CONTEXT,
        compaction_rules=_DEFAULT_COMPACTION,
        budget=MappingProxyType({"local_tokens": budget_local, "expensive_tokens": budget_expensive}),
        future_layers=_DEFAULT_FUTURE_LAYERS,
    )


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_token_policy_json(policy: TokenPolicy) -> dict[str, Any]:
    """Export a TokenPolicy as a JSON-serializable dict."""
    return {
        "version":              policy.version,
        "job_id":               policy.job_id,
        "scope":                policy.scope,
        "zero_token_steps":     list(policy.zero_token_steps),
        "local_first_steps":    list(policy.local_first_steps),
        "expensive_model_steps": list(policy.expensive_model_steps),
        "forbidden_context":    list(policy.forbidden_context),
        "compaction_rules":     list(policy.compaction_rules),
        "budget":               dict(policy.budget),
        "future_layers":        list(policy.future_layers),
    }


def summarize_token_policy(policy: TokenPolicy) -> str:
    """Return a human-readable summary of the TokenPolicy."""
    lines: list[str] = []
    lines.append("Token Policy")
    lines.append(f"  Version:  {policy.version}")
    lines.append(f"  Job:      {policy.job_id[:8]}")
    lines.append(f"  Scope:    {policy.scope}")

    lines.append("  Zero-token steps (no LLM):")
    for s in policy.zero_token_steps:
        lines.append(f"    0 {s}")

    lines.append("  Local-first steps (cheap model):")
    for s in policy.local_first_steps:
        lines.append(f"    L {s}")

    lines.append("  Expensive-model steps (frontier):")
    for s in policy.expensive_model_steps:
        lines.append(f"    $ {s}")

    lines.append("  Forbidden context (never sent to LLM):")
    for f in policy.forbidden_context:
        lines.append(f"    X {f}")

    lines.append("  Compaction rules:")
    for c in policy.compaction_rules:
        lines.append(f"    ~ {c}")

    lines.append(f"  Budget: local={policy.budget.get('local_tokens', 0):,}  expensive={policy.budget.get('expensive_tokens', 0):,}")

    lines.append("  Future layers:")
    for fl in policy.future_layers:
        lines.append(f"    > {fl}")

    return "\n".join(lines)
