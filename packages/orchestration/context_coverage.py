"""
Context Coverage v0 — deterministic, redaction-safe context-health indicator.

This is NOT a model confidence score and NOT a truth score.
It is a context-health signal based on available, observable structured signals
(job model, run-log events, and project constitution).

Scope: job-scoped in v0.  Future steps will add Repo Brain and Project Brain
aggregation once those layers are implemented.

Redaction policy:
  No artifact content, diff previews, approval reasons, event messages, or
  raw command output appear in any signal detail, summary, or JSON export.

Public API::

    derive_context_coverage(job, events, *, constitution=None) -> ContextCoverageSnapshot
    summarize_context_coverage(snapshot) -> str
    export_context_coverage_json(snapshot) -> dict[str, Any]
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import ArtifactKind, Job

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_int(value: object, default: int = 0) -> int:
    """Return int(value) or default on any parse error."""
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Signal definitions  (weights must sum to 100)
# ---------------------------------------------------------------------------

_SIGNALS: list[dict[str, Any]] = [
    {
        "key": "attached_repo",
        "label": "Attached repo",
        "weight": 15,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "project_constitution",
        "label": "Project Constitution",
        "weight": 15,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "planned_tasks",
        "label": "Planned tasks",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "builder_artifacts",
        "label": "Builder artifacts",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "patch_intents",
        "label": "Patch intents",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "verification_results",
        "label": "Verification results",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "run_logs",
        "label": "Run logs",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "approval_decisions",
        "label": "Approval decisions",
        "weight": 5,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "project_memory",
        "label": "Project memory",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "mcp_tool_context",
        "label": "MCP/tool context",
        "weight": 5,
        "v0_detail_absent": "MCP Quarantine / Skill Registry not connected yet",
        "v0_always_false": True,
    },
]

_TOTAL_WEIGHT: int = sum(s["weight"] for s in _SIGNALS)
assert _TOTAL_WEIGHT == 100, f"Signal weights must sum to 100, got {_TOTAL_WEIGHT}"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContextCoverageSignal:
    """A single context-health signal."""

    key: str
    label: str
    present: bool
    weight: int
    detail: str


@dataclass(frozen=True)
class ContextCoverageSnapshot:
    """Immutable context-coverage snapshot for a job."""

    job_id: str
    scope: str           # "job" in v0
    score: int           # 0..100
    present_weight: int
    total_weight: int
    signals: tuple[ContextCoverageSignal, ...]
    missing_keys: tuple[str, ...]


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def derive_context_coverage(
    job: Job,
    events: list[dict[str, Any]],
    *,
    constitution: object | None = None,
) -> ContextCoverageSnapshot:
    """Build a read-only ContextCoverageSnapshot from job model and run-log events.

    Deterministic — no LLM calls, no external processes, no repo access.
    Redaction: no artifact content, approval reasons, event messages, diff
    previews, or raw command output are read or surfaced.
    """
    event_types: frozenset[str] = frozenset(
        e.get("event", "") for e in events if isinstance(e, dict)
    )

    def _eval(key: str) -> tuple[bool, str]:
        if key == "attached_repo":
            present = bool(job.metadata.get("target_repo"))
            return present, ("attached" if present else "no repo attached")

        if key == "project_constitution":
            present = (
                constitution is not None
                and bool(getattr(constitution, "source_files", None))
            )
            return present, (
                "loaded" if present
                else "no constitution loaded" if constitution is None
                else "constitution present but empty"
            )

        if key == "planned_tasks":
            present = bool(job.tasks)
            return present, (
                f"{len(job.tasks)} task(s)" if present else "no tasks planned"
            )

        if key == "builder_artifacts":
            builder = [
                a for a in job.artifacts
                if a.kind == ArtifactKind.BUILDER_PROPOSAL
            ]
            present = bool(builder)
            return present, (
                f"{len(builder)} artifact(s)" if present
                else "no builder artifacts yet"
            )

        if key == "patch_intents":
            has_pi = any(
                _safe_int(a.metadata.get("patch_intent_count")) > 0
                for a in job.artifacts
            )
            if not has_pi:
                has_pi = "patch_intent_created" in event_types
            return has_pi, (
                "patch intents present" if has_pi
                else "no patch intents derived yet"
            )

        if key == "verification_results":
            present = bool(
                {"verification_passed", "verification_failed"} & event_types
            )
            return present, (
                "verification results logged" if present
                else "no verification results yet"
            )

        if key == "run_logs":
            present = bool(events)
            return present, (
                f"{len(events)} event(s)" if present else "no run-log events"
            )

        if key == "approval_decisions":
            present = bool(
                {"patch_intent_approved", "patch_intent_rejected"} & event_types
            )
            return present, (
                "approval decisions recorded" if present
                else "no approval decisions yet"
            )

        if key == "project_memory":
            try:
                from packages.memory.local_gateway import has_approved_memory
                project_id = job.metadata.get("project_id")
                present = has_approved_memory(
                    project_id=project_id,
                    job_id=str(job.id) if not project_id else None,
                )
                # Also check job-scoped when project_id is set
                if not present and project_id:
                    present = has_approved_memory(job_id=str(job.id))
            except (ImportError, ValueError, OSError):
                present = False
            return present, (
                "approved memory entries present" if present
                else "no approved memory entries"
            )

        # Should never reach here for defined signals
        return False, "unknown signal"

    built: list[ContextCoverageSignal] = []
    present_weight = 0

    for spec in _SIGNALS:
        key = spec["key"]
        weight = spec["weight"]
        always_false: bool = spec["v0_always_false"]
        absent_detail: str = spec["v0_detail_absent"]

        if always_false:
            present = False
            detail = absent_detail
        else:
            present, detail = _eval(key)

        if present:
            present_weight += weight

        built.append(ContextCoverageSignal(
            key=key,
            label=spec["label"],
            present=present,
            weight=weight,
            detail=detail,
        ))

    total = _TOTAL_WEIGHT
    score = max(0, min(100, round(present_weight / total * 100)))
    missing_keys = tuple(s.key for s in built if not s.present)

    return ContextCoverageSnapshot(
        job_id=str(job.id),
        scope="job",
        score=score,
        present_weight=present_weight,
        total_weight=total,
        signals=tuple(built),
        missing_keys=missing_keys,
    )


def summarize_context_coverage(snapshot: ContextCoverageSnapshot) -> str:
    """Return a human-readable Context Coverage report.

    Read-only: never mutates snapshot or any filesystem resource.
    Redaction: no artifact content, approval reasons, event messages,
    diff previews, or command output are included.
    """
    job_short = snapshot.job_id[:8]
    score = snapshot.score

    bar_len = 20
    filled = round(bar_len * score / 100)
    bar = "█" * filled + "░" * (bar_len - filled)

    parts: list[str] = []
    parts.append("Remedy Context Coverage")
    parts.append(f"Job: {job_short}")
    parts.append(f"Scope: {snapshot.scope}")
    parts.append(f"Coverage: {score}%")
    parts.append("")

    parts.append("── Coverage bar " + "─" * 37)
    parts.append(f"  [{bar}] {score}%")
    parts.append("")

    present = [s for s in snapshot.signals if s.present]
    missing = [s for s in snapshot.signals if not s.present]

    if present:
        parts.append("── Available context " + "─" * 32)
        for s in present:
            label_padded = f"{s.label:<28}"
            parts.append(f"  ✓ {label_padded} +{s.weight}")
        parts.append("")

    if missing:
        parts.append("── Missing context " + "─" * 34)
        for s in missing:
            label_padded = f"{s.label:<28}"
            detail_str = f"  {s.detail}" if s.detail else ""
            parts.append(f"  ○ {label_padded} +{s.weight}{detail_str}")
        parts.append("")

    parts.append("── Meaning " + "─" * 42)
    parts.append(
        "  Context Coverage is a signal of available project/job context."
    )
    parts.append(
        "  It is not model confidence and not a guarantee of correctness."
    )
    parts.append(
        "  In v0, the maximum score is 95% — only MCP/tool context (+5)"
        " is not yet implemented. Local memory v0 is active."
    )
    parts.append("")

    parts.append("── Next useful action " + "─" * 31)
    parts.append(f"  → remedy brain graph {snapshot.job_id[:8]}")
    parts.append(f"  → remedy brain trust {snapshot.job_id[:8]}")

    return "\n".join(parts)


def export_context_coverage_json(snapshot: ContextCoverageSnapshot) -> dict[str, Any]:
    """Export a ContextCoverageSnapshot as a JSON-serialisable dict.

    Schema::

        {
            "version": 1,
            "job_id": "<uuid>",
            "scope": "job",
            "score": <int>,
            "present_weight": <int>,
            "total_weight": <int>,
            "signals": [{"key", "label", "present", "weight", "detail"}, ...],
            "missing_keys": ["<key>", ...],
        }

    Redaction: no artifact content, diff previews, approval reasons, event
    messages, or command output are included.
    """
    return {
        "version": 1,
        "job_id": snapshot.job_id,
        "scope": snapshot.scope,
        "score": snapshot.score,
        "present_weight": snapshot.present_weight,
        "total_weight": snapshot.total_weight,
        "signals": [
            {
                "key": s.key,
                "label": s.label,
                "present": s.present,
                "weight": s.weight,
                "detail": s.detail,
            }
            for s in snapshot.signals
        ],
        "missing_keys": list(snapshot.missing_keys),
    }
