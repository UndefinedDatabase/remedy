"""
Context Budget Optimizer v1 — deterministic context budget optimization.

No LLM calls, no network, no external execution. Local-first.

Public API::

    explain_context(job, events, *, mode, budget) -> dict
    optimize_context(job, events, *, budget) -> dict
"""

from __future__ import annotations

from typing import Any

from packages.core.models import Job
from packages.orchestration.context_pack import (
    ContextPack,
    PackSection,
    _build_apply_proof,
    _build_blockers,
    _build_command_candidates,
    _build_job_summary,
    _build_memory_keys,
    _build_readiness_summary,
    _build_run_events,
    _build_task_state,
    build_context_pack,
)


def _all_sections(job: Job, events: list[dict[str, Any]], mode: str) -> list[PackSection]:
    """Build all context pack sections for analysis."""
    return [
        _build_job_summary(job, mode),
        _build_task_state(job, mode),
        _build_blockers(job, mode),
        _build_apply_proof(events, mode),
        _build_readiness_summary(job, events, mode),
        _build_memory_keys(mode),
        _build_command_candidates(events, mode),
        _build_run_events(events, mode),
    ]


def _section_reason(name: str) -> str:
    """Why a section is included."""
    reasons = {
        "job_summary": "Core job identity and state — always included.",
        "task_state": "Current task statuses — critical for decision making.",
        "blockers_permissions": "Permission state — required for autonomy assessment.",
        "apply_test_proof": "Apply/test evidence — confirms what was done.",
        "readiness_summary": "Readiness level — guides next actions.",
        "memory_keys": "Project memory — context from prior runs.",
        "command_candidates": "Discovered commands — informs test execution.",
        "run_events": "Event counts — overall run health signal.",
    }
    return reasons.get(name, "Context section.")


def _is_zero_token(name: str) -> bool:
    """Whether section is derived without any external calls."""
    # All current sections are local-derived
    return True


def explain_context(
    job: Job,
    events: list[dict[str, Any]],
    *,
    mode: str = "compact",
    budget: int = 2000,
) -> dict[str, Any]:
    """Explain what a context pack contains and why."""
    if mode not in ("compact", "caveman", "standard"):
        mode = "compact"

    all_secs = _all_sections(job, events, mode)
    all_secs.sort(key=lambda s: s.priority)

    pack = build_context_pack(job, events, budget=budget, mode=mode)
    included_names = {s.name for s in pack.sections}

    sections = []
    excluded = []
    for s in all_secs:
        entry = {
            "id": s.name,
            "title": s.name.replace("_", " ").title(),
            "estimated_tokens": s.estimated_tokens,
            "reason": _section_reason(s.name),
            "source": "local",
            "zero_token": _is_zero_token(s.name),
            "included": s.name in included_names,
            "truncated": False,
        }
        if s.name in included_names:
            sections.append(entry)
        else:
            entry["included"] = False
            excluded.append(entry)

    recommendations: list[str] = []
    if pack.truncated:
        recommendations.append("Use 'caveman' mode for smaller context.")
        recommendations.append("Increase budget to include all sections.")
    if mode == "standard":
        recommendations.append("Switch to 'compact' mode to save ~30% tokens.")

    return {
        "version": 1,
        "job_id": str(job.id),
        "mode": mode,
        "budget": budget,
        "estimated_tokens": pack.estimated_tokens,
        "sections": sections,
        "excluded": excluded,
        "recommendations": recommendations,
    }


def optimize_context(
    job: Job,
    events: list[dict[str, Any]],
    *,
    budget: int = 2000,
) -> dict[str, Any]:
    """Recommend optimal context configuration for a budget."""
    from packages.orchestration.worker_recommend import recommend_worker

    # Try all modes
    modes = ["caveman", "compact", "standard"]
    best_mode = "compact"
    best_tokens = 0
    results: dict[str, ContextPack] = {}

    for m in modes:
        pack = build_context_pack(job, events, budget=budget, mode=m)
        results[m] = pack
        if not pack.truncated and pack.estimated_tokens > best_tokens:
            best_tokens = pack.estimated_tokens
            best_mode = m

    # If all modes truncate, pick caveman (smallest)
    if all(r.truncated for r in results.values()):
        best_mode = "caveman"
        best_tokens = results["caveman"].estimated_tokens

    chosen = results[best_mode]
    standard = results["standard"]
    savings = standard.estimated_tokens - chosen.estimated_tokens

    # Worker recommendation
    rec = recommend_worker(job, events)

    included = [s.name for s in chosen.sections]
    all_names = {s.name for m in modes for s in results[m].sections}
    excluded = sorted(all_names - set(included))

    recommendations: list[str] = []
    if best_mode == "caveman":
        recommendations.append("Budget is tight — using caveman mode.")
    if savings > 100:
        recommendations.append(f"Saving ~{savings} tokens vs standard mode.")
    if not rec.recommended_worker.startswith("ollama"):
        recommendations.append("Consider local-first worker to avoid remote token cost.")

    return {
        "version": 1,
        "job_id": str(job.id),
        "budget": budget,
        "recommended_mode": best_mode,
        "estimated_tokens": chosen.estimated_tokens,
        "token_savings": max(0, savings),
        "included_sections": included,
        "excluded_sections": excluded,
        "recommendations": recommendations,
        "recommended_worker": rec.recommended_worker,
    }
