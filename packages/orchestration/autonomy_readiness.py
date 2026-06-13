"""
Autonomy Readiness v2 — deterministic readiness assessment for jobs and projects.

Reports which autonomy levels the current job/project can safely support,
based on factual signals (attached repo, permissions, apply proofs, test proofs,
memory, revert snapshots, token policy, etc.).
This is NOT model confidence — it is infrastructure readiness.

Autonomy levels:
  0 observe            — read-only inspection
  1 propose            — can generate plans/artifacts
  2 approved_apply     — can apply approved markdown patches
  3 test_execution     — can run discovered test commands
  4 bounded_loop       — can run agent loop with max_cycles
  5 revert_capable     — can revert applied patches (snapshot-backed)
  6 external_tools     — MCP/external tool use (future only)
  7 provider_autonomy  — provider-level autonomy (future only)

Public API::

    assess_job_readiness(job, events) -> ReadinessReport
    assess_project_readiness(project_id, jobs, all_events) -> ReadinessReport
    export_readiness_json(report) -> dict
    summarize_readiness(report) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
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
    {"level": 5, "name": "revert_capable"},
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
    signals: dict[str, bool] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Signal helpers
# ---------------------------------------------------------------------------

def _resolve_readiness_data_dir() -> Path:
    """Resolve the data root used for durable snapshot-truth checks."""
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root()


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


def _has_token_policy_applied(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "token_policy_applied" for e in events)


def _has_approved_memory() -> bool:
    try:
        from packages.memory.local_gateway import has_approved_memory
        return has_approved_memory()
    except (ImportError, ValueError, OSError):
        return False


def _has_worker_adapters(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "worker_adapters_listed" for e in events)


def _has_agent_loop(events: list[dict[str, Any]]) -> bool:
    return any(
        e.get("event", "").startswith("agent_loop_") for e in events
    )


def _has_revert_snapshot(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "patch_intent_reverted" for e in events)


def _has_verified_snapshot(job: Job, data_dir: Path) -> bool:
    """True only if the job has a durably verified, revert-capable snapshot.

    Authoritative durable check via build_snapshot_truth (Step 1159). A generic
    `snapshot_create_completed` event, or artifact metadata alone, is NOT proof —
    those fallbacks are removed. Readiness requires, for at least one applied
    intent:
      - a loadable DurableApplyRecord (valid apply linkage)
      - a loadable RepositorySnapshot
      - current successful verification (manifest + blobs verify now)
      - recovery material available
      - evidence_status complete (no unresolved evidence failure)
      - no partial/failed revert
      - the apply is still active (not already reverted)
    """
    from packages.orchestration.repository_snapshot import build_snapshot_truth

    job_id = str(job.id)
    # Candidate intents come from artifact apply-record keys; the truth itself is
    # loaded from durable storage, never from the metadata values.
    intent_ids: set[str] = set()
    for art in getattr(job, "artifacts", []):
        recs = (getattr(art, "metadata", {}) or {}).get("patch_intent_apply_records", {})
        intent_ids.update(recs.keys())

    candidates = list(intent_ids) or [None]  # None → job-wide latest apply scan
    for iid in candidates:
        truth = build_snapshot_truth(job_id, intent_id=iid, data_dir=data_dir)
        if (
            truth.apply_state == "applied"
            and truth.snapshot_verified_now
            and truth.recovery_material_available
            and truth.evidence_status == "complete"
            and truth.revert_state not in ("partial_revert", "revert_failed")
        ):
            return True
    return False


def _has_git_status(events: list[dict[str, Any]]) -> bool:
    return any(e.get("event") == "git_status_read" for e in events)


def _has_pending_approvals(events: list[dict[str, Any]]) -> bool:
    """Check if there are unresolved approval blockers."""
    approved = set()
    rejected = set()
    for e in events:
        ev = e.get("event", "")
        iid = e.get("metadata", {}).get("intent_id", "")
        if ev == "patch_intent_approved":
            approved.add(iid)
        elif ev == "patch_intent_rejected":
            rejected.add(iid)
    # If there are patch intents that are neither approved nor rejected
    intent_ids = set()
    for e in events:
        if e.get("event") == "patch_intent_created":
            iid = e.get("metadata", {}).get("intent_id", "")
            if iid:
                intent_ids.add(iid)
    pending = intent_ids - approved - rejected
    return len(pending) > 0


def _has_no_open_decisions(job: Job, events: list[dict[str, Any]]) -> bool:
    """True when there are no open human decisions pending."""
    try:
        from packages.orchestration.decision_queue import build_decision_summary, list_decisions
        decisions = list_decisions(job, events)
        summary = build_decision_summary(decisions)
        return summary.get("open_count", 0) == 0
    except (ImportError, OSError):
        return True  # If module unavailable, don't block


def _collect_signals(
    job: Job, events: list[dict[str, Any]], data_dir: Path | None = None
) -> dict[str, bool]:
    """Collect all readiness signals into a flat dict."""
    data_dir = data_dir if data_dir is not None else _resolve_readiness_data_dir()
    return {
        "attached_repo": _has_attached_repo(job),
        "project_link": bool(job.metadata.get("project_id")),
        "constitution": _has_constitution(events),
        "tasks_defined": _has_tasks(job),
        "command_discovery": _has_command_discovery(events),
        "repo_generated_write": _has_permission(job, "repo_generated_write"),
        "repo_test_run": _has_permission(job, "repo_test_run"),
        "approved_patch": _has_approved_patch(events),
        "apply_proof": _has_apply_proof(events),
        "test_proof": _has_test_proof(events),
        "approved_memory": _has_approved_memory(),
        "token_policy": _has_token_policy(events),
        "token_policy_applied": _has_token_policy_applied(events),
        "run_contract": _has_run_contract(events),
        "agent_loop": _has_agent_loop(events),
        "revert_snapshot": _has_revert_snapshot(events),
        "verified_snapshot": _has_verified_snapshot(job, data_dir),
        "no_pending_approvals": not _has_pending_approvals(events),
        "git_status": _has_git_status(events),
        "no_open_decisions": _has_no_open_decisions(job, events),
    }


# ---------------------------------------------------------------------------
# Level assessment
# ---------------------------------------------------------------------------

def _assess_level(
    level_def: dict[str, Any],
    job: Job,
    events: list[dict[str, Any]],
    signals: dict[str, bool],
) -> LevelAssessment:
    """Assess a single autonomy level for a job."""
    lvl = level_def["level"]
    name = level_def["name"]

    present: list[str] = []
    missing: list[str] = []
    blockers: list[str] = []
    actions: list[str] = []

    def _check(signal_key: str, action: str | None = None) -> None:
        if signals.get(signal_key, False):
            present.append(signal_key)
        else:
            missing.append(signal_key)
            if action:
                actions.append(action)

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
        _check("attached_repo", "remedy job attach-repo <job_id> <path>")
        _check("tasks_defined", "remedy job create ... --task-type <type>")

    elif lvl == 2:
        # approved_apply: need repo + permission + approved patch + proof
        _check("attached_repo")
        _check("repo_generated_write", "remedy job permit <job_id> repo_generated_write allow")
        _check("approved_patch")
        _check("apply_proof")

    elif lvl == 3:
        # test_execution: need command discovery + permission + test proof
        _check("command_discovery", "remedy test discover <job_id>")
        _check("repo_test_run", "remedy job permit <job_id> repo_test_run allow")
        _check("test_proof")

    elif lvl == 4:
        # bounded_loop: need agent loop + run contract + token policy + no open decisions
        _check("agent_loop", "remedy job run-loop <job_id>")
        _check("run_contract")
        _check("token_policy")
        _check("token_policy_applied")
        _check("no_open_decisions", "remedy decision list <job_id>")

    elif lvl == 5:
        # revert_capable: need apply proof + verified snapshot + test proof (Step 1150)
        _check("apply_proof")
        _check("verified_snapshot")
        _check("test_proof")
        _check("approved_memory")

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
    data_dir: Path | None = None,
) -> ReadinessReport:
    """Assess autonomy readiness for a single job.

    data_dir is used for authoritative durable snapshot-truth checks (Step 1159);
    defaults to the resolved data root when omitted.
    """
    data_dir = data_dir if data_dir is not None else _resolve_readiness_data_dir()
    signals = _collect_signals(job, events, data_dir)
    assessments = tuple(_assess_level(ld, job, events, signals) for ld in LEVELS)
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
        version=2,
        scope="job",
        job_id=str(job.id),
        project_id=job.metadata.get("project_id", ""),
        highest_eligible_level=highest,
        levels=assessments,
        next_actions=tuple(all_actions),
        signals=signals,
    )


def assess_project_readiness(
    project_id: str,
    jobs: list[Job],
    all_events: dict[str, list[dict[str, Any]]],
    data_dir: Path | None = None,
) -> ReadinessReport:
    """Assess autonomy readiness across all linked jobs in a project."""
    data_dir = data_dir if data_dir is not None else _resolve_readiness_data_dir()
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
            version=2, scope="project", job_id="",
            project_id=project_id, highest_eligible_level=0,
            levels=empty_levels, next_actions=("Create a linked job",),
            signals={},
        )

    # Aggregate: level eligible if ANY linked job is eligible at that level
    # Collect signals from all jobs
    agg_signals: dict[str, bool] = {}
    job_signals_list = []
    for j in jobs:
        js = _collect_signals(j, all_events.get(str(j.id), []), data_dir)
        job_signals_list.append(js)
        for k, v in js.items():
            agg_signals[k] = agg_signals.get(k, False) or v

    level_results: list[LevelAssessment] = []
    for ld in LEVELS:
        per_job = [_assess_level(ld, j, all_events.get(str(j.id), []), js) for j, js in zip(jobs, job_signals_list)]
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
        version=2, scope="project", job_id="",
        project_id=project_id, highest_eligible_level=highest,
        levels=tuple(level_results),
        next_actions=first_missing_actions,
        signals=agg_signals,
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
        "eligible_levels": [a.level for a in report.levels if a.eligible],
        "blocked_levels": [a.level for a in report.levels if a.blockers],
        "next_actions": list(report.next_actions),
        "signals": report.signals,
    }


def summarize_readiness(report: ReadinessReport) -> str:
    """Human-readable text summary of readiness."""
    lines = [f"Autonomy Readiness ({report.scope}: {report.job_id[:8] or report.project_id[:8]})"]
    lines.append(f"Highest eligible level: {report.highest_eligible_level}")
    lines.append("")
    for a in report.levels:
        mark = "\u2713" if a.eligible else "\u2715"
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
            lines.append(f"  \u2192 {act}")
    return "\n".join(lines)
