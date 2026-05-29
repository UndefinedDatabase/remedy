"""
Autonomy Readiness v0 — deterministic readiness assessment for jobs and projects.

Reports which autonomy levels the current job/project can safely support,
based on factual signals (attached repo, permissions, apply proofs, test proofs,
memory, etc.).  This is NOT model confidence — it is infrastructure readiness.

Autonomy levels:
  0 observe         — read-only inspection
  1 propose         — can generate plans/artifacts
  2 approved_apply  — can apply approved markdown patches
  3 test_execution  — can run discovered test commands
  4 bounded_loop    — can run agent loop with max_cycles
  5 repair_loop     — rollback + retry (not implemented)
  6 external_tools  — MCP/external tool use (not implemented)
  7 provider_autonomy — provider-level autonomy (not implemented)

Public API::

    assess_job_readiness(job, events) -> ReadinessReport
    assess_project_readiness(project_id, jobs, all_events) -> ReadinessReport
    export_readiness_json(report) -> dict
    summarize_readiness(report) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.core.models import Job, RunState


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

LEVELS: list[dict[str, Any]] = [
    {"level": 0, "name": "observe"},
    {"level": 1, "name": "propose"},
    {"level": 2, "name": "approved_apply"},
    {"level": 3, "name": "test_execution"},
    {"level": 4, "name": "bounded_loop"},
    {"level": 5, "name": "repair_loop"},
    {"level": 6, "name": "external_tools"},
    {"level": 7, "name": "provider_autonomy"},
]


@dataclass(frozen=True)
class LevelAssessment:
    """Assessment of a single autonomy level."""

    level: int
    name: str
    eligible: bool
    present_signals: tuple[str, ...]
    missing_signals: tuple[str, ...]
    blockers: tuple[str, ...]
    next_actions: tuple[str, ...]


@dataclass(frozen=True)
class ReadinessReport:
    """Full readiness assessment."""

    version: int
    scope: str  # "job" or "project"
    job_id: str
    project_id: str
    highest_eligible_level: int
    levels: tuple[LevelAssessment, ...]
    next_actions: tuple[str, ...]


# ---------------------------------------------------------------------------
# Signal helpers
# ---------------------------------------------------------------------------

def _has_attached_repo(job: Job) -> bool:
    return bool(job.metadata.get("target_repo"))


def _has_constitution(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "project_constitution_loaded" for e in events)


def _has_tasks(job: Job) -> bool:
    return len(job.tasks) > 0


def _has_permission(job: Job, perm: str) -> bool:
    return job.metadata.get("permissions", {}).get(perm) == "allow"


def _has_apply_proof(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "patch_apply_proof_recorded" for e in events)


def _has_approved_patch(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "patch_intent_approved" for e in events)


def _has_test_proof(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "test_run_completed" for e in events)


def _has_command_discovery(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "command_discovery_completed" for e in events)


def _has_run_contract(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "run_contract_inspected" for e in events)


def _has_token_policy(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "token_policy_inspected" for e in events)


def _has_approved_memory() -> bool:
    try:
        from packages.memory.local_gateway import has_approved_memory
        return has_approved_memory()
    except Exception:
        return False


def _has_worker_adapters(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "worker_adapters_listed" for e in events)


def _has_agent_loop(events: list[dict[str, Any]]) -> bool:
    return any(
        e.get("event", "").startswith("agent_loop_") for e in events
    )


# ---------------------------------------------------------------------------
# Level assessment
# ---------------------------------------------------------------------------

def _assess_level(
    level_def: dict[str, Any],
    job: Job,
    events: list[dict[str, Any]],
) -> LevelAssessment:
    """Assess a single autonomy level for a job."""
    lvl = level_def["level"]
    name = level_def["name"]

    present: list[str] = []
    missing: list[str] = []
    blockers: list[str] = []
    actions: list[str] = []

    if lvl == 0:
        # observe: always eligible
        present.append("read_access")
        return LevelAssessment(
            level=lvl, name=name, eligible=True,
            present_signals=tuple(present), missing_signals=(),
            blockers=(), next_actions=(),
        )

    if lvl == 1:
        # propose: need repo + tasks
        if _has_attached_repo(job):
            present.append("attached_repo")
        else:
            missing.append("attached_repo")
            actions.append("remedy job attach-repo <job_id> <path>")
        if _has_tasks(job):
            present.append("tasks_defined")
        else:
            missing.append("tasks_defined")
            actions.append("remedy job create ... --task-type <type>")

    elif lvl == 2:
        # approved_apply: need repo + permission + approved patch
        if _has_attached_repo(job):
            present.append("attached_repo")
        else:
            missing.append("attached_repo")
        if _has_permission(job, "repo_generated_write"):
            present.append("repo_generated_write")
        else:
            missing.append("repo_generated_write")
            actions.append("remedy job permit <job_id> repo_generated_write allow")
        if _has_approved_patch(events):
            present.append("approved_patch")
        else:
            missing.append("approved_patch")
        if _has_apply_proof(events):
            present.append("apply_proof")
        else:
            missing.append("apply_proof")

    elif lvl == 3:
        # test_execution: need command discovery + permission
        if _has_command_discovery(events):
            present.append("command_discovery")
        else:
            missing.append("command_discovery")
            actions.append("remedy test discover <job_id>")
        if _has_permission(job, "repo_test_run"):
            present.append("repo_test_run")
        else:
            missing.append("repo_test_run")
            actions.append("remedy job permit <job_id> repo_test_run allow")
        if _has_test_proof(events):
            present.append("test_proof")
        else:
            missing.append("test_proof")

    elif lvl == 4:
        # bounded_loop: need agent loop + run contract + token policy
        if _has_agent_loop(events):
            present.append("agent_loop")
        else:
            missing.append("agent_loop")
            actions.append("remedy job run-loop <job_id>")
        if _has_run_contract(events):
            present.append("run_contract")
        else:
            missing.append("run_contract")
        if _has_token_policy(events):
            present.append("token_policy")
        else:
            missing.append("token_policy")

    elif lvl == 5:
        # repair_loop: rollback not implemented
        blockers.append("rollback_not_implemented")
        missing.append("rollback_capability")

    elif lvl == 6:
        # external_tools: MCP not implemented
        blockers.append("mcp_not_connected")
        missing.append("mcp_quarantine")

    elif lvl == 7:
        # provider_autonomy: not implemented
        blockers.append("provider_autonomy_not_implemented")
        missing.append("provider_integration")

    eligible = len(missing) == 0 and len(blockers) == 0

    return LevelAssessment(
        level=lvl, name=name, eligible=eligible,
        present_signals=tuple(present), missing_signals=tuple(missing),
        blockers=tuple(blockers), next_actions=tuple(actions),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def assess_job_readiness(
    job: Job,
    events: list[dict[str, Any]],
) -> ReadinessReport:
    """Assess autonomy readiness for a single job."""
    assessments = tuple(_assess_level(ld, job, events) for ld in LEVELS)
    highest = -1
    for a in assessments:
        if a.eligible:
            highest = a.level

    # Collect next_actions from first non-eligible level
    all_actions: list[str] = []
    for a in assessments:
        if not a.eligible:
            all_actions.extend(a.next_actions)
            break

    return ReadinessReport(
        version=1,
        scope="job",
        job_id=str(job.id),
        project_id=job.metadata.get("project_id", ""),
        highest_eligible_level=highest,
        levels=assessments,
        next_actions=tuple(all_actions),
    )


def assess_project_readiness(
    project_id: str,
    jobs: list[Job],
    all_events: dict[str, list[dict[str, Any]]],
) -> ReadinessReport:
    """Assess autonomy readiness across all linked jobs in a project."""
    if not jobs:
        empty_levels = tuple(
            LevelAssessment(
                level=ld["level"], name=ld["name"], eligible=(ld["level"] == 0),
                present_signals=("read_access",) if ld["level"] == 0 else (),
                missing_signals=() if ld["level"] == 0 else ("no_linked_jobs",),
                blockers=(), next_actions=(),
            )
            for ld in LEVELS
        )
        return ReadinessReport(
            version=1, scope="project", job_id="",
            project_id=project_id, highest_eligible_level=0,
            levels=empty_levels, next_actions=("Create a linked job",),
        )

    # Aggregate: level eligible if ANY linked job is eligible at that level
    level_results: list[LevelAssessment] = []
    for ld in LEVELS:
        per_job = [_assess_level(ld, j, all_events.get(str(j.id), [])) for j in jobs]
        any_eligible = any(a.eligible for a in per_job)
        all_present = set()
        all_missing = set()
        all_blockers = set()
        all_actions: list[str] = []
        for a in per_job:
            all_present.update(a.present_signals)
            all_missing.update(a.missing_signals)
            all_blockers.update(a.blockers)
            all_actions.extend(a.next_actions)
        if any_eligible:
            all_missing.clear()
        level_results.append(LevelAssessment(
            level=ld["level"], name=ld["name"], eligible=any_eligible,
            present_signals=tuple(sorted(all_present)),
            missing_signals=tuple(sorted(all_missing)),
            blockers=tuple(sorted(all_blockers)),
            next_actions=tuple(dict.fromkeys(all_actions)),
        ))

    highest = max((a.level for a in level_results if a.eligible), default=-1)
    first_missing_actions: tuple[str, ...] = ()
    for a in level_results:
        if not a.eligible:
            first_missing_actions = a.next_actions
            break

    return ReadinessReport(
        version=1, scope="project", job_id="",
        project_id=project_id, highest_eligible_level=highest,
        levels=tuple(level_results),
        next_actions=first_missing_actions,
    )


def export_readiness_json(report: ReadinessReport) -> dict[str, Any]:
    """Export readiness report as safe JSON dict."""
    return {
        "version": report.version,
        "scope": report.scope,
        "job_id": report.job_id,
        "project_id": report.project_id,
        "highest_eligible_level": report.highest_eligible_level,
        "levels": [
            {
                "level": a.level,
                "name": a.name,
                "eligible": a.eligible,
                "present_signals": list(a.present_signals),
                "missing_signals": list(a.missing_signals),
                "blockers": list(a.blockers),
                "next_actions": list(a.next_actions),
            }
            for a in report.levels
        ],
        "next_actions": list(report.next_actions),
    }


def summarize_readiness(report: ReadinessReport) -> str:
    """Human-readable text summary of readiness."""
    lines = [f"Autonomy Readiness ({report.scope}: {report.job_id[:8] or report.project_id[:8]})"]
    lines.append(f"Highest eligible level: {report.highest_eligible_level}")
    lines.append("")
    for a in report.levels:
        mark = "✓" if a.eligible else "✕"
        lines.append(f"  [{mark}] Level {a.level}: {a.name}")
        if a.present_signals:
            lines.append(f"      present: {', '.join(a.present_signals)}")
        if a.missing_signals:
            lines.append(f"      missing: {', '.join(a.missing_signals)}")
        if a.blockers:
            lines.append(f"      blockers: {', '.join(a.blockers)}")
    if report.next_actions:
        lines.append("")
        lines.append("Next actions:")
        for act in report.next_actions:
            lines.append(f"  → {act}")
    return "\n".join(lines)
