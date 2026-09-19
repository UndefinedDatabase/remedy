"""
Token Economy v0 — deterministic routing policy for a Remedy job.

A TokenPolicy describes how tokens should be allocated across steps:
which steps are zero-token (pure local Python), which use local-first
models, and which justify expensive frontier models.

Provider-neutral: no model names, no network calls, no shell execution,
no external processes.  Pure data contract only.

Public API::

    build_default_token_policy(job) -> TokenPolicy
    derive_token_mode(job) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan

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


def build_default_token_policy(job: JobPlan) -> TokenPolicy:
    """Build a sensible default TokenPolicy for a job.

    Deterministic — derives policy from job metadata only.
    No LLM calls, no network, no filesystem access.
    """
    job_id_str = str(job.job_id)
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


def derive_token_mode(job: JobPlan) -> str:
    """The token mode a job's shape asks for: caveman, compact or standard.

    Deterministic — reads the task count and the run state and nothing else.
    DECISION F274 D7 moved this here out of `worker_recommend`, which dies
    with the prototype cluster: a token mode is token policy.
    """
    task_count = len(job.tasks) if job.tasks else 0
    if task_count == 0 or job.state == RunState.COMPLETED:
        return "caveman"
    if task_count <= 2:
        return "compact"
    return "standard"
