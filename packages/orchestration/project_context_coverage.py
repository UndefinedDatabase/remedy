"""
Project Context Coverage v0 — project-scoped, deterministic context-health indicator.

Aggregates context signals across all jobs and repos linked to a RemyProject.
This is NOT model confidence and NOT a truth score.

Scope: project in v0.  No repo scanning, no network access, no artifact
content, no event log reading.

Redaction policy:
  No artifact content, diff previews, approval reasons, event messages,
  raw command output, or exception text appear in any signal, summary, or export.

Signals (weights sum to 100):
  project_metadata        — +10   project object exists and has a name
  linked_repos            — +15   project has ≥1 attached repo path
  linked_jobs             — +15   project has ≥1 loaded linked job
  planned_tasks           — +10   any linked job has tasks
  builder_artifacts       — +10   any linked job has a BUILDER_PROPOSAL artifact
  patch_intents           — +10   any linked job has derived patch intents
  verification_results    — +10   any linked job has VERIFICATION artifacts or completed tasks
  approval_decisions      — +5    any linked job has approved/rejected patch intents
  project_memory          — +10   local memory v0 (approved entries)
  mcp_tool_context        — +5    always absent in v0 (MCP Skill Registry)

v0 maximum score = 95 (only mcp_tool_context is always absent).

Public API::

    ProjectContextSignal
    ProjectContextCoverageSnapshot
    derive_project_context_coverage(project, jobs) -> ProjectContextCoverageSnapshot
    summarize_project_context_coverage(snapshot) -> str
    export_project_context_coverage_json(snapshot) -> dict[str, Any]
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from packages.core.models import ArtifactKind, RunState

if TYPE_CHECKING:
    from packages.orchestration.project_registry import RemyProject


# ---------------------------------------------------------------------------
# Signal definitions  (weights must sum to 100)
# ---------------------------------------------------------------------------

_SIGNALS: list[dict[str, Any]] = [
    {
        "key": "project_metadata",
        "label": "Project metadata",
        "weight": 10,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "linked_repos",
        "label": "Linked repos",
        "weight": 15,
        "v0_always_false": False,
        "v0_detail_absent": "",
    },
    {
        "key": "linked_jobs",
        "label": "Linked jobs",
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
        "v0_always_false": True,
        "v0_detail_absent": "MCP Skill Registry not connected yet",
    },
]

_TOTAL_WEIGHT: int = sum(s["weight"] for s in _SIGNALS)
assert _TOTAL_WEIGHT == 100, f"Signal weights must sum to 100, got {_TOTAL_WEIGHT}"

V0_MAX_SCORE: int = _TOTAL_WEIGHT - sum(
    s["weight"] for s in _SIGNALS if s["v0_always_false"]
)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProjectContextSignal:
    """A single project-level context-health signal."""

    key: str
    label: str
    present: bool
    weight: int
    detail: str


@dataclass(frozen=True)
class ProjectContextCoverageSnapshot:
    """Immutable project context-coverage snapshot."""

    project_id: str
    project_name: str
    scope: str              # always "project"
    score: int              # 0..85 in v0
    present_signal_count: int
    missing_signal_count: int
    repo_count: int
    job_count: int
    signals: tuple[ProjectContextSignal, ...]
    missing_keys: tuple[str, ...]


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def derive_project_context_coverage(
    project: "RemyProject",
    jobs: list[Any],  # list[Job] — Any to avoid cross-package circular imports
) -> ProjectContextCoverageSnapshot:
    """Build a read-only ProjectContextCoverageSnapshot from a project and its loaded jobs.

    Deterministic — no LLM calls, no external processes, no repo scanning.
    Redaction: no artifact content, approval reasons, event messages, diff
    previews, or raw command output are read or surfaced.

    ``jobs`` must be the Job objects already loaded for this project — the
    caller is responsible for filtering to the jobs linked in project.job_ids.
    """
    from packages.orchestration.approval_queue import (
        APPROVAL_PENDING,
        list_patch_intents,
    )

    repo_count = len(project.repo_paths)
    job_count = len(jobs)

    total_tasks = sum(len(j.tasks) for j in jobs)

    has_builder_artifacts = any(
        a.kind == ArtifactKind.BUILDER_PROPOSAL
        for j in jobs
        for a in j.artifacts
    )

    all_intents: list[dict[str, Any]] = []
    for j in jobs:
        all_intents.extend(list_patch_intents(j))
    has_patch_intents = bool(all_intents)

    has_approvals = any(
        intent["state"] != APPROVAL_PENDING for intent in all_intents
    )

    # Verification: explicit VERIFICATION artifacts OR any completed task (v0 heuristic)
    has_verification = any(
        a.kind == ArtifactKind.VERIFICATION
        for j in jobs
        for a in j.artifacts
    ) or any(
        t.status == RunState.COMPLETED
        for j in jobs
        for t in j.tasks
    )

    def _eval(key: str) -> tuple[bool, str]:
        if key == "project_metadata":
            return True, f"name={project.name!r}"

        if key == "linked_repos":
            present = repo_count > 0
            return present, (
                f"{repo_count} repo(s)" if present else "no repos attached"
            )

        if key == "linked_jobs":
            present = job_count > 0
            return present, (
                f"{job_count} job(s)" if present else "no jobs linked"
            )

        if key == "planned_tasks":
            present = total_tasks > 0
            return present, (
                f"{total_tasks} task(s) across {job_count} job(s)"
                if present else "no tasks planned"
            )

        if key == "builder_artifacts":
            return has_builder_artifacts, (
                "builder artifacts present" if has_builder_artifacts
                else "no builder artifacts yet"
            )

        if key == "patch_intents":
            count = len(all_intents)
            return has_patch_intents, (
                f"{count} patch intent(s)" if has_patch_intents
                else "no patch intents derived yet"
            )

        if key == "verification_results":
            return has_verification, (
                "verification results present" if has_verification
                else "no verification results yet"
            )

        if key == "approval_decisions":
            return has_approvals, (
                "approval decisions recorded" if has_approvals
                else "no approval decisions yet"
            )

        if key == "project_memory":
            try:
                from packages.memory.local_gateway import has_approved_memory
                present = has_approved_memory(
                    project_id=str(project.id),
                )
                if not present:
                    # Check any linked job
                    for j in jobs:
                        if has_approved_memory(job_id=str(j.id)):
                            present = True
                            break
            except Exception:
                present = False
            return present, (
                "approved memory entries present" if present
                else "no approved memory entries"
            )

        return False, "unknown signal"

    built: list[ProjectContextSignal] = []
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

        built.append(ProjectContextSignal(
            key=key,
            label=spec["label"],
            present=present,
            weight=weight,
            detail=detail,
        ))

    score = max(0, min(100, round(present_weight / _TOTAL_WEIGHT * 100)))
    missing_keys = tuple(s.key for s in built if not s.present)

    return ProjectContextCoverageSnapshot(
        project_id=str(project.id),
        project_name=project.name,
        scope="project",
        score=score,
        present_signal_count=sum(1 for s in built if s.present),
        missing_signal_count=sum(1 for s in built if not s.present),
        repo_count=repo_count,
        job_count=job_count,
        signals=tuple(built),
        missing_keys=missing_keys,
    )


def summarize_project_context_coverage(
    snapshot: ProjectContextCoverageSnapshot,
) -> str:
    """Return a human-readable Project Context Coverage report.

    Read-only: never mutates snapshot or any filesystem resource.
    Redaction: no artifact content, approval reasons, event messages,
    diff previews, or command output are included.
    """
    score = snapshot.score
    short_id = snapshot.project_id[:8]

    bar_len = 20
    filled = round(bar_len * score / 100)
    bar = "█" * filled + "░" * (bar_len - filled)

    parts: list[str] = []
    parts.append("Remedy Project Context Coverage")
    parts.append(f"Project: {short_id} — {snapshot.project_name}")
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
            detail_str = f"  {s.detail}" if s.detail else ""
            parts.append(f"  ✓ {label_padded} +{s.weight}{detail_str}")
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
        "  Project Context Coverage is a deterministic signal of structured context"
    )
    parts.append("  available across this project.")
    parts.append(
        "  It is not model confidence and not a guarantee of correctness."
    )
    parts.append(
        f"  In v0, the maximum score is {V0_MAX_SCORE}% —"
        " MCP/tool context (+5) is not yet implemented."
    )

    return "\n".join(parts)


def export_project_context_coverage_json(
    snapshot: ProjectContextCoverageSnapshot,
) -> dict[str, Any]:
    """Export a ProjectContextCoverageSnapshot as a JSON-serialisable dict.

    Schema::

        {
            "version": 1,
            "project_id": "...",
            "project_name": "...",
            "scope": "project",
            "score": 0..85 in v0,
            "present_signal_count": int,
            "missing_signal_count": int,
            "repo_count": int,
            "job_count": int,
            "v0_max_score": 95,
            "signals": [{"key", "label", "weight", "present", "detail"}, ...],
            "missing_keys": [...],
        }

    Redaction: no artifact content, diff previews, approval reasons, event
    messages, or command output are included.
    """
    return {
        "version": 1,
        "project_id": snapshot.project_id,
        "project_name": snapshot.project_name,
        "scope": snapshot.scope,
        "score": snapshot.score,
        "present_signal_count": snapshot.present_signal_count,
        "missing_signal_count": snapshot.missing_signal_count,
        "repo_count": snapshot.repo_count,
        "job_count": snapshot.job_count,
        "v0_max_score": V0_MAX_SCORE,
        "signals": [
            {
                "key": s.key,
                "label": s.label,
                "weight": s.weight,
                "present": s.present,
                "detail": s.detail,
            }
            for s in snapshot.signals
        ],
        "missing_keys": list(snapshot.missing_keys),
    }
