"""The job report: a job's JSON export, its plain-text page, and a blocked task's findings.

F307 moved it here from ``pingpong_job.py`` as that file's structural step (2) in
``docs/system/structure-ledger-v1.md``; the job model, its store and ``run_job`` stay there.

Public API:
    export_job_report(job) -> dict
    format_job_report_text(job) -> str
    collect_blocked_task_findings(job, full=False) -> list[dict]
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.core.models import RunState
from packages.orchestration.execution_config import _export_execution_config
from packages.orchestration.pingpong_job import (
    _PREVIOUS_SUMMARY_LIMIT,
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    JOB_PLANNED,
    TASK_APPLIED,
    TASK_BLOCKED,
    TASK_FAILED,
    TASK_PASSED,
    TASK_PENDING,
    TASK_RUNNING,
    TASK_SKIPPED,
    TASK_VETOED,
    JobPlan,
    _export_apply_manifest,
    _export_proof_summary,
    _export_target_guard,
)


def _task_veto_report_map(job: JobPlan) -> dict[str, dict[str, Any]]:
    """The report's and the export's own veto lookup (DECISION F027 D7 (3)): the fold's
    own `job.metadata["task_vetoes"]` record for a task first, and the control files for a
    veto no run has folded yet — mirrors `task_veto._event_unreachable`'s own unreachable
    reading for an entry not already folded. A `TaskVetoError` reading the control files is
    swallowed: it costs the report nothing beyond the entries it could not read, and a job
    with no veto at all sees no key here, so its report and export stay byte for byte
    unchanged."""
    out: dict[str, Any] = dict((job.metadata or {}).get("task_vetoes") or {})

    from packages.orchestration import task_veto as _tv

    try:
        entries = _tv.vetoed_tasks(job.job_id)
    except _tv.TaskVetoError:
        return out

    all_ids = {e.task_id for e in entries}
    for entry in entries:
        if entry.task_id in out:
            continue
        other_ids = all_ids - {entry.task_id}
        unreachable = [
            tid for tid in _tv.veto_unreachable(job.tasks, [entry.task_id])
            if tid not in other_ids
        ]
        out[entry.task_id] = {**entry.to_json(), "unreachable_task_ids": unreachable}
    return out


def _task_steering_not_consumed_map(job: JobPlan) -> dict[str, list[dict[str, Any]]]:
    """The report's and the export's own steering-note lookup (F030 T001, DECISION F030 D1):
    for every task whose status is neither ``TASK_PENDING`` nor ``TASK_RUNNING`` — its round
    loop is done and will never consume another note — the notes addressed to it that no round
    ever consumed, each as ``{"message_id", "text", "received_at"}`` in arrival order. A task
    with none is omitted, so a job with no such note exports the same keys as before. The job's
    steering records and consumption markers are read ONCE for the whole job, not once per
    task, mirroring `_task_veto_report_map`'s own single read. A `SteeringError` reading them
    (a tampered record) is swallowed exactly as that function swallows a `TaskVetoError`: it
    costs the report nothing beyond the notes it could not read.
    """
    from packages.orchestration import steering as _st

    try:
        records = _st.list_steering_messages(job.job_id)
        markers = _st.list_steering_consumptions(job.job_id)
    except _st.SteeringError:
        return {}

    out: dict[str, list[dict[str, Any]]] = {}
    for task in job.tasks:
        if task.status in (TASK_PENDING, TASK_RUNNING):
            continue
        notes = [
            {"message_id": r["message_id"], "text": r["text"], "received_at": r["received_at"]}
            for r in records
            if _st.note_task_id(r) == task.task_id and r["message_id"] not in markers
        ]
        if notes:
            out[task.task_id] = notes
    return out


def export_job_report(job: JobPlan) -> dict[str, Any]:
    """Export a JSON-serializable job report."""
    # Function-scoped, like every other data_paths import in this module. The
    # single use below sits inside a compound boolean, where a missing import is
    # a runtime NameError on the worktree path only — so it is bound HERE, at
    # the top of the function, where it is visible to a reader.
    from packages.orchestration.data_paths import job_dir

    veto_map = _task_veto_report_map(job)
    steering_map = _task_steering_not_consumed_map(job)
    task_reports = []
    for t in job.tasks:
        report = {
            "task_id": t.task_id,
            "source_heading_number": t.source_heading_number,
            "title": t.title,
            "status": t.status,
            "run_id": t.run_id,
            "final_status": t.final_status,
            "test_passed": t.test_passed,
            "reviewer_verdict": t.reviewer_verdict,
            "repair_rounds_used": t.repair_rounds_used,
            "repair_rounds_allowed": t.repair_rounds_allowed,
            "safe_diff_files": t.safe_diff_files,
            "error": t.error,
            "apply_manifest": _export_apply_manifest(t.apply_manifest),
            "proof_summary": _export_proof_summary(t.proof_summary),
        }
        veto_info = veto_map.get(t.task_id)
        if veto_info is not None:
            report["veto"] = {
                "reason": veto_info.get("reason", ""),
                "actor": veto_info.get("actor", ""),
                "requested_at": veto_info.get("requested_at", ""),
                "unreachable_task_ids": list(veto_info.get("unreachable_task_ids") or []),
            }
        notes = steering_map.get(t.task_id)
        if notes is not None:
            report["steering_not_consumed"] = notes
        task_reports.append(report)

    # F006: a completed worktree job's execution workspace is deliberately gone.
    # Availability of the hand-off is decided by the worktree cleanup status plus a
    # verified job-level result.diff — never by "is that directory still there?".
    # The recorded relative worktree path is kept as audit data.
    has_workspace_changes = False
    handoff_available = False
    if job.isolation_mode == "worktree":
        handoff_available = bool(
            job.result_diff_path
            and job.result_diff_sha256
            and (job_dir(job.job_id) / job.result_diff_path).is_file()
        )
        has_workspace_changes = handoff_available and any(
            t.status == TASK_APPLIED for t in job.tasks
        )
    elif job.job_workspace_path:
        ws = Path(job.job_workspace_path)
        if ws.exists():
            has_workspace_changes = any(
                t.status == TASK_APPLIED for t in job.tasks
            )
            handoff_available = has_workspace_changes

    next_cmd = _suggest_next_command(job)

    pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)

    return {
        "job_id": job.job_id,
        "job_title": job.job_title,
        "status": job.state.value if isinstance(job.state, RunState) else job.state,
        "repo_path": job.repo_path,
        "job_workspace_path": job.job_workspace_path,
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "tasks": task_reports,
        "has_workspace_changes": has_workspace_changes,
        "isolation_mode": job.isolation_mode,
        "worktree": {
            "branch": job.worktree_branch,
            "path": job.worktree_path,          # repo-relative audit path
            "base_commit": job.worktree_base_commit,
            "head": job.worktree_head,
            "cleanup_status": job.worktree_cleanup_status,
            "workspace_expected_present": (
                job.isolation_mode == "worktree"
                and job.worktree_cleanup_status != "clean"
            ),
        },
        "handoff_available": handoff_available,
        "result_diff": (
            {
                "path": job.result_diff_path,
                "sha256": job.result_diff_sha256,
                "size_bytes": job.result_diff_size_bytes,
            }
            if job.result_diff_path else None
        ),
        "next_command": next_cmd,
        "target_guard": _export_target_guard(job.target_guard),
        # F010: the job-level post-mortem, and the reason one could not be written. A
        # recording failure that did not survive `_persist_job` was a recording failure the
        # evidence export could never see.
        "postmortem": {
            "path": job.postmortem_path,      # evidence-relative, never absolute
            "error": job.postmortem_error,
        },
        "repair_rounds_allowed": job.repair_rounds_allowed,
        "repair_rounds_source": job.repair_rounds_source,
        "pending_tasks": pending_count,
        "execution_config": _export_execution_config(job.execution_config),
        "context_strategy": {
            "strategy": "task_bounded_sequential_job",
            "previous_task_summary_limit": _PREVIOUS_SUMMARY_LIMIT,
            "full_job_history_in_prompt": False,
            "full_repo_in_prompt": False,
        },
        "warning": (
            "Real target repo was NOT mutated. "
            "Changes exist only in the isolated job workspace."
        ),
    }


#: How many of one blocked task's last-round findings `job show` prints; `--full`
#: prints every one (R-0806).
BLOCKED_TASK_FINDINGS_CAP = 10


def collect_blocked_task_findings(job: JobPlan, *, full: bool = False) -> list[dict[str, Any]]:
    """The reviewer findings of the LAST round of every blocked task (R-0806).

    One entry per task whose status is ``blocked``, in task order. Each finding is
    copied verbatim from the task's run record (``id``, ``severity``, ``file``,
    ``summary``), at most ``BLOCKED_TASK_FINDINGS_CAP`` of them unless ``full``.
    This feeds a read view, so it never raises: a task with no run id, or whose run
    record is missing or unreadable, reports no findings.
    """
    from packages.orchestration.pingpong_loop import load_run

    entries: list[dict[str, Any]] = []
    for task in job.tasks:
        if task.status != TASK_BLOCKED:
            continue
        round_number = None
        findings: list[dict[str, Any]] = []
        try:
            run = load_run(task.run_id) if task.run_id else None
        except (OSError, ValueError):
            run = None
        rounds = run.get("rounds") if isinstance(run, dict) else None
        if isinstance(rounds, list) and rounds and isinstance(rounds[-1], dict):
            last = rounds[-1]
            round_number = last.get("round")
            reviewer = last.get("reviewer")
            recorded = reviewer.get("findings") if isinstance(reviewer, dict) else None
            if isinstance(recorded, list):
                findings = [
                    {key: finding.get(key, "") for key in ("id", "severity", "file", "summary")}
                    for finding in recorded
                    if isinstance(finding, dict)
                ]
        shown = findings if full else findings[:BLOCKED_TASK_FINDINGS_CAP]
        entries.append({
            "task_id": task.task_id,
            "run_id": task.run_id,
            "round": round_number,
            "findings": shown,
            "findings_total": len(findings),
            "findings_omitted": len(findings) - len(shown),
        })
    return entries


def format_job_report_text(job: JobPlan) -> str:
    """Format a human-readable job report."""
    lines = [
        f"Job {job.job_id}: {job.job_title}",
        f"Status: {job.state}",
        f"Repo: {job.repo_path}",
        "",
        "Tasks:",
    ]

    steering_map = _task_steering_not_consumed_map(job)
    for t in job.tasks:
        status_icon = {
            TASK_PENDING: " ",
            TASK_RUNNING: ">",
            TASK_PASSED: "+",
            TASK_APPLIED: "*",
            TASK_BLOCKED: "!",
            TASK_FAILED: "X",
            TASK_SKIPPED: "-",
            TASK_VETOED: "/",
        }.get(t.status, "?")

        line = f"  [{status_icon}] {t.task_id}: {t.title} — {t.status}"
        if t.run_id:
            line += f" (run: {t.run_id})"
        lines.append(line)

        if t.reviewer_verdict:
            lines.append(f"      Reviewer: {t.reviewer_verdict}")
        if t.repair_rounds_used:
            lines.append(
                f"      Repair: {t.repair_rounds_used}/{t.repair_rounds_allowed}"
            )
        if t.apply_manifest and t.apply_manifest.applied_files:
            lines.append(
                f"      Applied: {len(t.apply_manifest.applied_files)} files"
            )
        if t.error:
            lines.append(f"      Error: {t.error}")
        for note in steering_map.get(t.task_id, []):
            lines.append(
                "      Steering not consumed: “" + note["text"].replace("\n", "\n        ") + "”"
            )

    lines.append("")

    # F035 T002 (DECISION F035 D3): the whole ownership ledger, worded through the one
    # catalog in `ownership_phrases.py`, replaces the per-task `Vetoed by` line above — one
    # dialect for who did what, instead of the same fact stated twice in two wordings. A job
    # with no entry prints no section at all, so its report is byte for byte unchanged; a
    # ledger that cannot be read prints one line naming the error rather than silently
    # dropping the section.
    from packages.orchestration.ownership import OwnershipError, build_ownership_ledger
    from packages.orchestration.ownership_phrases import ownership_sentences

    try:
        ledger = build_ownership_ledger(job)
    except (OwnershipError, OSError) as exc:
        lines.append(f"Ownership: the ledger could not be read — {exc}")
        lines.append("")
    else:
        titles = {t.task_id: t.title for t in job.tasks}
        sentences = ownership_sentences(ledger, titles=titles)
        if sentences:
            lines.append("Ownership:")
            for sentence in sentences:
                lines.append("  - " + sentence.replace("\n", "\n    "))
            lines.append("")

    if job.repair_rounds_source:
        disabled = " (disabled)" if job.repair_rounds_allowed == 0 else ""
        lines.append(
            f"Repair: {job.repair_rounds_allowed} rounds"
            f" (source: {job.repair_rounds_source}){disabled}"
        )

    pending_count = sum(1 for t in job.tasks if t.status == TASK_PENDING)
    if job.state == JOB_PAUSED and pending_count > 0:
        lines.append(f"Paused: {pending_count} tasks pending")
        # F025 S6: an OPERATOR pause says who paused it and why; a task-scope one
        # also names what it withheld. A `max_tasks` pause carries no record (S1),
        # so this block is silent for it, unchanged from before this round.
        if job.pause:
            lines.append(
                f"Paused by {job.pause.get('source', '')}: {job.pause.get('reason', '')}"
            )
            if job.pause.get("scope") == "task":
                withheld = job.pause.get("withheld_task_ids") or []
                lines.append(f"Withheld tasks: {', '.join(withheld)}")

    ec = job.execution_config
    if ec:
        lines.append(f"Builder: {ec.builder} (source: {ec.builder_source})")
        lines.append(f"Reviewer: {ec.reviewer} (source: {ec.reviewer_source})")
        lines.append(f"Max rounds: {ec.max_rounds} (source: {ec.max_rounds_source})")
        tc = ec.test_command
        if tc:
            tc_display = tc[:80] + "..." if len(tc) > 80 else tc
            lines.append(f"Test command: {tc_display} (source: {ec.test_command_source})")
        if ec.claude_cli_write_mode != "none":
            lines.append(
                f"Write mode: {ec.claude_cli_write_mode}"
                f" (source: {ec.claude_cli_write_mode_source})"
            )
        if job.state == JOB_PAUSED:
            lines.append("Continuation config: persisted from previous run")

    if any(t.status == TASK_APPLIED for t in job.tasks):
        lines.append("Job workspace has accumulated changes.")
    lines.append(
        "WARNING: Real target repo was NOT mutated. "
        "Changes exist only in the isolated job workspace."
    )

    next_cmd = _suggest_next_command(job)
    if next_cmd:
        lines.append(f"\nNext: {next_cmd}")

    return "\n".join(lines)


def _suggest_next_command(job: JobPlan) -> str:
    """Suggest the next CLI command based on job state.

    For paused jobs with persisted config, the short command is safe — config
    is restored from persistence. The report text shows the config that will
    be used.
    """
    if job.state == JOB_PLANNED:
        return f"remedy job run {job.job_id}"
    if job.state == JOB_PAUSED:
        return f"remedy job run {job.job_id}"
    if job.state == JOB_COMPLETED:
        return f"remedy job apply {job.job_id} --repo . --dry-run"
    if job.state == JOB_BLOCKED:
        return f"remedy job show {job.job_id} --full"
    pending = [t for t in job.tasks if t.status == TASK_PENDING]
    if pending:
        return f"remedy job run {job.job_id}"
    return ""
