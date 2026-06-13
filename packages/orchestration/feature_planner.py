"""
Feature Planner v0 — deterministic next-work suggestions.

No LLM. Rules-based only. Suggestions must be explicitly accepted by user.

Public API::

    build_feature_plan(ledger, job=None) -> FeaturePlan
    export_feature_plan_json(plan) -> dict
    summarize_feature_plan(plan) -> str
    accept_feature_suggestion(plan, suggestion_id, job_id) -> dict
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from packages.orchestration.progress_ledger import (
    ProgressLedger,
    ProgressSource,
    ProgressStatus,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class FeaturePlanPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FeaturePlanSource(str, Enum):
    OPEN_FINDING = "open_finding"
    KNOWN_RISK = "known_risk"
    PROOF_GAP = "proof_gap"
    REPAIR_ARTIFACT = "repair_artifact"
    FAILED_TEST = "failed_test"
    STALE_HANDOFF = "stale_handoff"
    ROADMAP = "roadmap"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class FeatureSuggestion:
    """One deterministic suggestion."""

    suggestion_id: str = ""
    title: str = ""
    rationale: str = ""
    priority: FeaturePlanPriority = FeaturePlanPriority.MEDIUM
    source_type: FeaturePlanSource = FeaturePlanSource.ROADMAP
    source_refs: list[str] = field(default_factory=list)
    estimated_risk: str = "low"
    suggested_steps: list[str] = field(default_factory=list)
    acceptance_summary: str = ""
    default_selected: bool = False
    creates_proposed_task: bool = True
    next_action: str = ""


@dataclass
class FeaturePlan:
    """Full feature plan."""

    version: int = 0
    planner_version: str = "v0-deterministic"
    suggestions: list[FeatureSuggestion] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Deterministic suggestion ID
# ---------------------------------------------------------------------------


def _make_suggestion_id(source_type: str, title: str) -> str:
    """Stable, deterministic suggestion ID."""
    raw = f"{source_type}:{title}"
    return "sug-" + hashlib.sha256(raw.encode()).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Roadmap suggestions (when everything is clean)
# ---------------------------------------------------------------------------

_ROADMAP_SUGGESTIONS = [
    FeatureSuggestion(
        suggestion_id="sug-roadmap-provenance",
        title="File Provenance v1 expansion",
        rationale="Extend file provenance chain to cover full lifecycle.",
        priority=FeaturePlanPriority.MEDIUM,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Expand proof chain", "Add file-level trust scores", "CLI integration"],
        next_action="remedy feature accept <job_id> sug-roadmap-provenance",
    ),
    FeatureSuggestion(
        suggestion_id="sug-roadmap-contract",
        title="Run Contract Enforcement v1",
        rationale="Enforce execution contracts before applying changes.",
        priority=FeaturePlanPriority.MEDIUM,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Define run contracts", "Pre-apply validation", "CLI enforcement"],
        next_action="remedy feature accept <job_id> sug-roadmap-contract",
    ),
    FeatureSuggestion(
        suggestion_id="sug-roadmap-test-exec",
        title="Real Test Execution v1",
        rationale="Run actual project tests (not just fixture stubs).",
        priority=FeaturePlanPriority.MEDIUM,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Test discovery", "Sandboxed execution", "Result collection"],
        next_action="remedy feature accept <job_id> sug-roadmap-test-exec",
    ),
    FeatureSuggestion(
        suggestion_id="sug-roadmap-cockpit",
        title="Operator Cockpit read-only v0.2",
        rationale="Read-only dashboard for monitoring job progress.",
        priority=FeaturePlanPriority.LOW,
        source_type=FeaturePlanSource.ROADMAP,
        suggested_steps=["Status endpoint", "Progress view", "Finding summary"],
        next_action="remedy feature accept <job_id> sug-roadmap-cockpit",
    ),
]


# ---------------------------------------------------------------------------
# Step 1018: Deterministic suggestion rules
# ---------------------------------------------------------------------------


def build_feature_plan(ledger: ProgressLedger, job: Any = None) -> FeaturePlan:
    """Build deterministic feature plan from ledger state."""
    plan = FeaturePlan()
    seen_ids: set[str] = set()

    # Rule 0: Continuation outcomes (Step 1176) — tailored next actions, no
    # automatic action or policy relaxation. Claims the relevant ledger item so
    # the generic rules below do not also emit a duplicate suggestion.
    _CONT_RULES = {
        "cont-test-fail": (
            "Start repair for failed continuation test",
            "Continuation test failed — repair available (no auto-repair).",
            FeaturePlanSource.FAILED_TEST,
            "remedy repair start <job_id> <failure_artifact_id> --json",
        ),
        "cont-evidence-incomplete": (
            "Repair continuation evidence",
            "Apply may have succeeded but evidence degraded — manual review.",
            FeaturePlanSource.PROOF_GAP,
            "remedy change proof <job_id> --json",
        ),
        "cont-snapshot-failed": (
            "Investigate continuation snapshot failure",
            "Snapshot could not be created or verified — investigate before retry.",
            FeaturePlanSource.PROOF_GAP,
            "remedy snapshot inspect <job_id> --json",
        ),
        "test-budget-exhausted": (
            "Review run contract test budget",
            "Test budget blocked the continuation — review the contract (no auto-raise).",
            FeaturePlanSource.KNOWN_RISK,
            "remedy contract inspect <job_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _CONT_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, next_action = rule
        sug_id = _make_suggestion_id("continuation", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        # Suppress the generic finding/gap suggestions for this same item.
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id,
            title=title,
            rationale=rationale,
            priority=FeaturePlanPriority.HIGH,
            source_type=source,
            source_refs=[item.item_id],
            estimated_risk="medium",
            default_selected=True,
            next_action=next_action,
        ))

    # Rule 0b: Repair Loop v1 outcomes (Step 1207) — evidence-backed next actions,
    # no automatic approval or contract relaxation.
    _REPAIR_RULES = {
        "repair-needed": (
            "Propose a repair for the failing test",
            "A failing test has no completed repair proposal yet.",
            FeaturePlanSource.FAILED_TEST,
            "remedy repair propose <job_id> <failure_artifact_id> --json",
        ),
        "repair-approval": (
            "Approve or reject the repair patch intent",
            "A repair patch intent is pending approval — your decision is required.",
            FeaturePlanSource.OPEN_FINDING,
            "remedy patch approve <job_id> <repair_intent_id>",
        ),
        "repair-blocked": (
            "Review the repair blocker",
            "A repair attempt was blocked (e.g. contract or eligibility) — review it.",
            FeaturePlanSource.KNOWN_RISK,
            "remedy repair status <job_id> --json",
        ),
    }
    for item in ledger.items:
        rule = _REPAIR_RULES.get(item.item_id)
        if rule is None:
            continue
        title, rationale, source, next_action = rule
        sug_id = _make_suggestion_id("repair", item.item_id)
        if sug_id in seen_ids:
            continue
        seen_ids.add(sug_id)
        seen_ids.add(_make_suggestion_id("finding", item.title))
        seen_ids.add(_make_suggestion_id("gap", item.title))
        plan.suggestions.append(FeatureSuggestion(
            suggestion_id=sug_id,
            title=title,
            rationale=rationale,
            priority=FeaturePlanPriority.HIGH,
            source_type=source,
            source_refs=[item.item_id],
            estimated_risk="medium",
            default_selected=True,
            next_action=next_action,
        ))

    # Rule 1: Open blocker/high findings -> high priority suggestions
    for item in ledger.items:
        if item.status == ProgressStatus.BLOCKED:
            sug_id = _make_suggestion_id("finding", item.title)
            if sug_id in seen_ids:
                continue
            seen_ids.add(sug_id)
            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title=f"Resolve: {item.title}"[:200],
                rationale=f"Open {item.severity} finding blocks progress.",
                priority=FeaturePlanPriority.HIGH,
                source_type=FeaturePlanSource.OPEN_FINDING,
                source_refs=[item.item_id],
                estimated_risk="medium",
                default_selected=True,
                next_action=f"Fix {item.item_id}",
            ))

    # Rule 2: Known risks / pre-existing failures -> medium/high suggestions
    for item in ledger.items:
        if item.status == ProgressStatus.RISK:
            sug_id = _make_suggestion_id("risk", item.title)
            if sug_id in seen_ids:
                continue
            seen_ids.add(sug_id)

            is_test_failure = item.source_type in (
                ProgressSource.REPAIR_ARTIFACT, ProgressSource.KNOWN_RISK
            ) and "fail" in item.title.lower()

            priority = FeaturePlanPriority.HIGH if is_test_failure else FeaturePlanPriority.MEDIUM
            source = FeaturePlanSource.FAILED_TEST if is_test_failure else FeaturePlanSource.KNOWN_RISK

            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title=f"Address risk: {item.title}"[:200],
                rationale="Known risk should be tracked and resolved.",
                priority=priority,
                source_type=source,
                source_refs=[item.item_id],
                estimated_risk="medium",
                next_action=f"Investigate {item.item_id}",
            ))

    # Rule 3: Proof gaps — snapshot-unverified applies get HIGH priority (no revert capability)
    for item in ledger.items:
        if item.source_type == ProgressSource.PROOF_GAP:
            sug_id = _make_suggestion_id("gap", item.title)
            if sug_id in seen_ids:
                continue
            seen_ids.add(sug_id)
            is_snapshot_gap = "snapshot" in item.title.lower() or "snapshot" in item.safe_summary.lower()
            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title=f"Close proof gap: {item.title}"[:200],
                rationale=(
                    "Apply without verified snapshot — revert capability unavailable."
                    if is_snapshot_gap else
                    "Proof chain incomplete — close gap for verification."
                ),
                priority=FeaturePlanPriority.HIGH if is_snapshot_gap else FeaturePlanPriority.MEDIUM,
                source_type=FeaturePlanSource.PROOF_GAP,
                source_refs=[item.item_id],
                estimated_risk="high" if is_snapshot_gap else "low",
                next_action=(
                    "Re-apply with snapshot or run remedy snapshot inspect"
                    if is_snapshot_gap else
                    "File Provenance expansion"
                ),
            ))

    # Rule 4: Stale handoff (inconsistencies in ledger)
    if ledger.inconsistencies:
        sug_id = _make_suggestion_id("handoff", "stale-handoff")
        if sug_id not in seen_ids:
            seen_ids.add(sug_id)
            plan.suggestions.append(FeatureSuggestion(
                suggestion_id=sug_id,
                title="Fix stale handoff state",
                rationale=f"{len(ledger.inconsistencies)} inconsistency(ies) in progress ledger.",
                priority=FeaturePlanPriority.HIGH,
                source_type=FeaturePlanSource.STALE_HANDOFF,
                source_refs=[],
                estimated_risk="low",
                next_action="Update .agent/ files to resolve inconsistencies",
            ))

    # Rule 5: If no issues, suggest roadmap items
    if not plan.suggestions:
        for roadmap in _ROADMAP_SUGGESTIONS:
            if roadmap.suggestion_id not in seen_ids:
                seen_ids.add(roadmap.suggestion_id)
                plan.suggestions.append(roadmap)

    # Sort: high first, then medium, then low
    priority_order = {FeaturePlanPriority.HIGH: 0, FeaturePlanPriority.MEDIUM: 1, FeaturePlanPriority.LOW: 2}
    plan.suggestions.sort(key=lambda s: priority_order.get(s.priority, 1))

    return plan


# ---------------------------------------------------------------------------
# Accept suggestion -> ProposedTask
# ---------------------------------------------------------------------------


def accept_feature_suggestion(plan: FeaturePlan, suggestion_id: str, job_id: str) -> dict:
    """Accept a suggestion — returns ProposedTask metadata dict.

    Does NOT create a real task or execute anything.
    Returns metadata for creating a ProposedTask.
    """
    suggestion = None
    for s in plan.suggestions:
        if s.suggestion_id == suggestion_id:
            suggestion = s
            break

    if suggestion is None:
        return {"error": f"Suggestion {suggestion_id} not found", "accepted": False}

    return {
        "accepted": True,
        "suggestion_id": suggestion.suggestion_id,
        "title": suggestion.title,
        "rationale": suggestion.rationale,
        "priority": suggestion.priority.value,
        "source_type": suggestion.source_type.value,
        "source_refs": suggestion.source_refs,
        "planner_version": plan.planner_version,
        "job_id": job_id,
        "creates_proposed_task": True,
        "executed": False,
        "applied": False,
    }


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_feature_plan_json(plan: FeaturePlan) -> dict:
    """Export feature plan as safe JSON dict."""
    return {
        "version": plan.version,
        "planner_version": plan.planner_version,
        "suggestion_count": len(plan.suggestions),
        "suggestions": [
            {
                "suggestion_id": s.suggestion_id,
                "title": s.title,
                "rationale": s.rationale,
                "priority": s.priority.value,
                "source_type": s.source_type.value,
                "source_refs": s.source_refs,
                "estimated_risk": s.estimated_risk,
                "suggested_steps": s.suggested_steps,
                "default_selected": s.default_selected,
                "next_action": s.next_action,
            }
            for s in plan.suggestions
        ],
    }


def summarize_feature_plan(plan: FeaturePlan) -> str:
    """Human-readable feature plan summary."""
    lines = ["Feature Plan (v0 — deterministic)", "=" * 40]
    lines.append(f"Suggestions: {len(plan.suggestions)}")
    lines.append("")

    for s in plan.suggestions:
        selected = "*" if s.default_selected else " "
        lines.append(f"  [{selected}] {s.suggestion_id} — {s.title}")
        lines.append(f"      Priority: {s.priority.value}  Source: {s.source_type.value}")
        lines.append(f"      Rationale: {s.rationale}")
        if s.next_action:
            lines.append(f"      Next: {s.next_action}")
        lines.append("")

    lines.append("To accept: remedy feature accept <job_id> <suggestion_id>")
    return "\n".join(lines)
