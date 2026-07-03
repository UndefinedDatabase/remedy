"""Token-cost policy evidence v1.

A job run consumes tokens across roles (builder, reviewer, repair). Reviewers
need one artifact that states, per role, *what the cost policy was* (model,
context budget, prompt-size cap, round/repair budgets) and *what the run
actually cost* (estimated / actual token usage, provider call counts) — then
flags where the policy was violated or the accounting is dishonest.

This module builds ``token_cost_policy.json`` deterministically from evidence
already collected: the role configuration, the honest token-truth report (see
``token_truth``), and the prompt-trace summary. No provider calls, no
target-repo mutation, no job state mutation — the same inputs always yield the
same artifact.

Cost-risk findings are raised for:
    * full repo context used unnecessarily (a role sent the whole repo),
    * prompt traces exceeding the configured per-role char budget,
    * actual token usage reported as available but no measured number exists,
    * estimated token usage missing for a role that made provider calls.

Public API:
    SCHEMA_VERSION
    build_token_cost_policy(job_id, step_range, role_configs, token_truth,
                            prompt_trace_summary, max_rounds, repair_budget) -> dict
"""
from __future__ import annotations

from typing import Any

SCHEMA_VERSION = "1.0.0"

# Canonical roles and their column in the prompt-trace / token-truth summaries.
_ROLE_PROMPT_KEYS = {
    "builder": "total_builder_prompts",
    "reviewer": "total_reviewer_prompts",
    "repair": "total_repair_prompts",
}
_ROLE_ESTIMATED_KEYS = {
    "builder": "builder_estimated_total",
    "reviewer": "reviewer_estimated_total",
    "repair": "repair_estimated_total",
}


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_int(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    return int(value)


def _is_truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "full", "full_repo", "on"}
    return bool(value)


def _finding(code: str, severity: str, role: str | None, message: str) -> dict[str, Any]:
    """Build one structured cost-risk finding."""
    return {"code": code, "severity": severity, "role": role, "message": message}


def _uses_full_repo(cfg: dict[str, Any]) -> bool:
    """True if a role config indicates the full repo was sent as context."""
    if _is_truthy(cfg.get("full_repo_context")):
        return True
    mode = str(cfg.get("context_mode", "")).strip().lower()
    return mode in {"full_repo", "full", "whole_repo"}


def _prompt_chars_for(role: str, trace: dict[str, Any]) -> int | None:
    """Per-role prompt char count from the trace summary, if recorded."""
    for key in (f"{role}_prompt_chars", f"total_{role}_prompt_chars"):
        if key in trace:
            return _as_int(trace[key])
    return None


def _actual_available_by_role(roles: list[str], token_truth: dict[str, Any]) -> dict[str, bool]:
    """Aggregate per-task actual availability from token-truth into per-role flags.

    A role is ``actual_available`` if any of its per-task entries reported measured
    provider usage. Falls back to the global flag when no per-task rows exist.
    """
    global_flag = bool(token_truth.get("actual_available"))
    per_task = _as_dict(token_truth.get("per_task"))

    seen: dict[str, bool] = {}
    for entry in per_task.values():
        entry = _as_dict(entry)
        role = str(entry.get("role", "")).strip().lower()
        if not role:
            continue
        seen[role] = seen.get(role, False) or bool(entry.get("actual_available"))

    return {role: seen.get(role, global_flag) for role in roles}


def build_token_cost_policy(
    job_id: str,
    step_range: str,
    role_configs: Any,
    token_truth: Any,
    prompt_trace_summary: Any,
    max_rounds: int,
    repair_budget: int,
) -> dict[str, Any]:
    """Build a deterministic token-cost policy evidence artifact.

    ``role_configs`` maps role name -> config dict. Recognized config keys:
    ``model``, ``context_budget`` (token budget for context), ``max_prompt_chars``
    (per-prompt char cap), and ``full_repo_context`` / ``context_mode`` (whether
    the whole repo was sent).

    ``token_truth`` is a token-truth report (see :mod:`token_truth`); its
    ``*_estimated_total`` and ``per_task`` fields feed estimated usage and actual
    availability. ``prompt_trace_summary`` supplies per-role provider call counts
    and prompt char sizes.
    """
    configs = _as_dict(role_configs)
    truth = _as_dict(token_truth)
    trace = _as_dict(prompt_trace_summary)

    roles = sorted(str(r) for r in configs)

    per_role_model_policy: dict[str, Any] = {}
    context_budget_policy: dict[str, Any] = {}
    max_prompt_chars_per_role: dict[str, Any] = {}
    estimated_tokens_by_role: dict[str, int] = {}
    provider_call_count_by_role: dict[str, int] = {}

    for role in roles:
        cfg = _as_dict(configs[role])
        per_role_model_policy[role] = cfg.get("model")
        context_budget_policy[role] = cfg.get("context_budget")
        max_prompt_chars_per_role[role] = cfg.get("max_prompt_chars")

        est_key = _ROLE_ESTIMATED_KEYS.get(role)
        estimated_tokens_by_role[role] = (
            _as_int(truth.get(est_key)) if est_key and est_key in truth else 0
        )

        prompt_key = _ROLE_PROMPT_KEYS.get(role)
        if prompt_key and prompt_key in trace:
            calls = _as_int(trace[prompt_key])
        elif f"{role}_prompts" in trace:
            calls = _as_int(trace[f"{role}_prompts"])
        else:
            calls = 0
        provider_call_count_by_role[role] = calls

    actual_available_by_role = _actual_available_by_role(roles, truth)
    global_actual_available = bool(truth.get("actual_available"))

    findings: list[dict[str, Any]] = []

    for role in roles:
        cfg = _as_dict(configs[role])

        # 1. Full repo context used unnecessarily.
        if _uses_full_repo(cfg):
            findings.append(
                _finding(
                    "FULL_REPO_CONTEXT",
                    "warning",
                    role,
                    f"Role '{role}' sent the full repository as context; use a "
                    "scoped context pack instead.",
                )
            )

        # 2. Prompt traces exceed the configured char budget.
        cap = cfg.get("max_prompt_chars")
        chars = _prompt_chars_for(role, trace)
        if isinstance(cap, (int, float)) and not isinstance(cap, bool) and cap > 0 and chars is not None and chars > cap:
            findings.append(
                _finding(
                    "PROMPT_TRACE_OVER_BUDGET",
                    "warning",
                    role,
                    f"Role '{role}' prompt traces used {chars} chars, over the "
                    f"{int(cap)}-char budget.",
                )
            )

        # 3. Actual usage reported as available but no measured number exists.
        if actual_available_by_role.get(role):
            has_actual_number = (
                _as_int(truth.get("actual_total_tokens")) > 0
                or _as_int(truth.get("actual_prompt_tokens")) > 0
                or _as_int(truth.get("actual_completion_tokens")) > 0
            )
            if not has_actual_number:
                findings.append(
                    _finding(
                        "ACTUAL_REPORTED_UNAVAILABLE",
                        "critical",
                        role,
                        f"Role '{role}' reports actual token usage as available, "
                        "but no measured token count is present.",
                    )
                )

        # 4. Estimated usage missing for a role that made provider calls.
        if provider_call_count_by_role.get(role, 0) > 0 and estimated_tokens_by_role.get(role, 0) <= 0:
            findings.append(
                _finding(
                    "ESTIMATE_MISSING",
                    "warning",
                    role,
                    f"Role '{role}' made {provider_call_count_by_role[role]} "
                    "provider call(s) but recorded no estimated token usage.",
                )
            )

    recommendations = _build_recommendations(findings, global_actual_available)

    return {
        "schema_version": SCHEMA_VERSION,
        "job_id": str(job_id),
        "step_range": str(step_range),
        "per_role_model_policy": per_role_model_policy,
        "context_budget_policy": context_budget_policy,
        "max_prompt_chars_per_role": max_prompt_chars_per_role,
        "max_rounds": max(0, _as_int(max_rounds)),
        "repair_budget": max(0, _as_int(repair_budget)),
        "actual_available_by_role": actual_available_by_role,
        "estimated_tokens_by_role": estimated_tokens_by_role,
        "provider_call_count_by_role": provider_call_count_by_role,
        "cost_risk_findings": findings,
        "recommendations": recommendations,
    }


def _build_recommendations(findings: list[dict[str, Any]], global_actual_available: bool) -> list[str]:
    """Derive de-duplicated, ordered recommendations from cost-risk findings."""
    codes = {f["code"] for f in findings}
    recs: list[str] = []

    if "FULL_REPO_CONTEXT" in codes:
        recs.append(
            "Replace full-repo context with scoped context packs to cut prompt token cost."
        )
    if "PROMPT_TRACE_OVER_BUDGET" in codes:
        recs.append(
            "Reduce prompt size or raise the per-role char budget to stay within policy."
        )
    if "ACTUAL_REPORTED_UNAVAILABLE" in codes:
        recs.append(
            "Do not report actual token usage as available unless a measured count exists; "
            "fall back to clearly-labeled estimates."
        )
    if "ESTIMATE_MISSING" in codes:
        recs.append(
            "Record estimated token usage for every role that issues provider calls."
        )

    if not global_actual_available:
        recs.append(
            "Actual token usage is unavailable for this run; treat all token figures as "
            "low-confidence estimates."
        )

    if not recs:
        recs.append("No token-cost risks detected; usage is within the configured policy.")

    return recs
