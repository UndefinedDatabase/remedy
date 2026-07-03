"""Sticky per-task actor binding v1.

Each task is executed by a *builder* actor and reviewed by a *reviewer* actor.
Across repair rounds and re-reviews, it matters whether the *same* actors stayed
bound to the task ("sticky"): a builder that fixes its own findings and a reviewer
that re-reviews its own prior review produce more coherent, accountable evidence
than a fresh actor per round.

This module records a ``task_actor_binding`` artifact per task, capturing builder
and reviewer identity (provider + model), round/repair counts, findings per round,
and whether stickiness held across rounds.

Public API:
    build_task_actor_binding(task_id, builder_provider, builder_model,
                             reviewer_provider, reviewer_model, rounds,
                             repair_rounds, findings_by_round, repaired_by_round,
                             unresolved, same_builder_repairs,
                             same_reviewer_re_review) -> dict
"""
from __future__ import annotations

from typing import Any


def _identity(provider: Any, model: Any) -> str | None:
    """Compose a ``provider:model`` identity string, or None if both are absent."""
    provider_str = "" if provider is None else str(provider)
    model_str = "" if model is None else str(model)
    if not provider_str and not model_str:
        return None
    return f"{provider_str}:{model_str}"


def build_task_actor_binding(
    task_id: str,
    builder_provider: Any = None,
    builder_model: Any = None,
    reviewer_provider: Any = None,
    reviewer_model: Any = None,
    rounds: int = 0,
    repair_rounds: int = 0,
    findings_by_round: Any = None,
    repaired_by_round: Any = None,
    unresolved: int = 0,
    same_builder_repairs: bool = False,
    same_reviewer_re_review: bool = False,
) -> dict[str, Any]:
    """Build a structured, self-describing ``task_actor_binding`` evidence dict.

    ``sticky_across_rounds`` is True only when both ``same_builder_repairs`` and
    ``same_reviewer_re_review`` are True — i.e. the same builder fixed its own
    findings and the same reviewer re-reviewed across every round.

    ``findings_by_round`` and ``repaired_by_round`` are normalized to lists of
    non-negative ints. ``rounds``, ``repair_rounds`` and ``unresolved`` are
    clamped to non-negative ints.
    """
    findings = [max(0, int(n or 0)) for n in (findings_by_round or [])]
    repaired = [max(0, int(n or 0)) for n in (repaired_by_round or [])]

    same_builder = bool(same_builder_repairs)
    same_reviewer = bool(same_reviewer_re_review)

    return {
        "task_id": str(task_id),
        "builder_role": "builder",
        "builder_provider": builder_provider,
        "builder_model_configured": builder_model,
        "builder_identity": _identity(builder_provider, builder_model),
        "reviewer_role": "reviewer",
        "reviewer_provider": reviewer_provider,
        "reviewer_model_configured": reviewer_model,
        "reviewer_identity": _identity(reviewer_provider, reviewer_model),
        "sticky_across_rounds": same_builder and same_reviewer,
        "rounds": max(0, int(rounds or 0)),
        "repair_rounds": max(0, int(repair_rounds or 0)),
        "reviewer_findings_by_round": findings,
        "repaired_findings_by_round": repaired,
        "unresolved_findings": max(0, int(unresolved or 0)),
        "same_builder_used_for_repairs": same_builder,
        "same_reviewer_used_for_re_review": same_reviewer,
    }
