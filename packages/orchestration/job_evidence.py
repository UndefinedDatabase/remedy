"""Job evidence bundle — exports a self-contained, redacted proof bundle for an entire job.

Read-only: never calls providers, never mutates target repo, never auto-promotes,
never reruns tasks, never mutates persisted job state.

Reuses single-run evidence redaction from pingpong_evidence. Does not duplicate
weaker redaction logic.

Public API:
    export_job_evidence(job_id, out_dir) -> dict
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from packages.orchestration.pingpong_evidence import (
    _redact_json_value,
    _redact_secrets,
    _sanitize_path,
    _validate_output_path,
    build_evidence_bundle,
    write_evidence_bundle,
)
from packages.orchestration.pingpong_job import (
    _export_apply_manifest,
    _export_execution_config,
    _export_proof_summary,
    _export_target_guard,
    load_job_plan,
)

_TASK_BODY_EVIDENCE_LIMIT = 500
_WORKSPACE_DIFF_MAX_CHARS = 500_000

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")


def _task_evidence_dir(out_base: str, task_id: str) -> Path:
    """Return a contained task evidence directory inside out_base/task_runs/.

    Only allows task IDs matching the expected format (T001, T002, ...).
    Raises ValueError on malicious, corrupt, or unexpected task IDs to prevent
    path traversal via persisted job state or symlink escapes.

    Uses _validate_output_path which calls .resolve() on the full joined path,
    following any symlinks in intermediate directories (e.g. out/task_runs/).
    """
    if not task_id or not _SAFE_TASK_ID_RE.fullmatch(task_id):
        raise ValueError(
            f"Unsafe task ID {task_id!r}: must match T<digits> (e.g. T001). "
            "Aborting evidence export to prevent path traversal."
        )
    return _validate_output_path(out_base, f"task_runs/{task_id}")


def export_job_evidence(
    job_id: str,
    out_dir: str,
) -> dict[str, Any]:
    """Load a persisted job and export a job-level evidence bundle.

    Returns JSON-serializable result with output paths, manifest, and status.
    Does not call providers. Does not mutate target repo or job state.
    """
    job = load_job_plan(job_id)
    if job is None:
        return {"error": f"Job {job_id!r} not found", "job_id": job_id}

    out_path = Path(out_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    written: dict[str, str] = {}

    def _write(filename: str, content: str) -> None:
        target = _validate_output_path(str(out_path), filename)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        written[filename] = str(target)

    def _write_json(filename: str, data: Any) -> None:
        _write(filename, json.dumps(_redact_json_value(data), indent=2) + "\n")

    manifest = _build_job_manifest(job)
    _write_json("manifest.json", manifest)

    summary_md = _build_job_summary_md(job)
    _write("summary.md", _redact_secrets(summary_md))

    job_report = _build_job_report_safe(job)
    _write_json("job_report.json", job_report)

    timeline = _build_job_timeline(job)
    _write_json("job_timeline.json", timeline)

    tasks_data = _build_tasks_json(job)
    _write_json("tasks.json", tasks_data)

    ec = _export_execution_config(job.execution_config)
    _write_json("execution_config.json", ec or {})

    cs = {
        "strategy": "task_bounded_sequential_job",
        "previous_task_summary_limit": 5,
        "full_job_history_in_prompt": False,
        "full_repo_in_prompt": False,
    }
    if job.execution_config:
        cs["strategy"] = job.execution_config.context_strategy
    _write_json("context_strategy.json", cs)

    tg = _export_target_guard(job.target_guard)
    _write_json("target_guard.json", tg or {"target_mutated": None, "note": "no guard data"})

    wa = _build_workspace_apply_json(job)
    _write_json("workspace_apply.json", wa)

    ws_diff = _build_workspace_diff(job)
    _write("workspace.diff", _redact_secrets(ws_diff))

    for task in job.tasks:
        _write_task_run_evidence(task, str(out_path), written)

    # Job-level prompt trace aggregate
    _write_job_prompt_trace_summary(job, str(out_path), written)

    from datetime import datetime, timezone
    manifest["bundle_generated_at"] = datetime.now(timezone.utc).isoformat()

    _write_json("manifest.json", manifest)

    return _redact_json_value({
        "job_id": job_id,
        "out_dir": str(out_path),
        "files": written,
        "manifest": manifest,
    })


def _build_job_manifest(job: Any) -> dict[str, Any]:
    return {
        "bundle_version": "0.1.0",
        "bundle_type": "job_evidence",
        "job_id": job.job_id,
        "job_title": job.job_title,
        "job_file_sha256": job.job_file_sha256,
        "status": job.status,
        "repo_identity": _sanitize_path(job.repo_path),
        "job_workspace_path": _sanitize_path(job.job_workspace_path) if job.job_workspace_path else "",
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "task_count": len(job.tasks),
        "task_ids": [t.task_id for t in job.tasks],
        "task_statuses": {t.task_id: t.status for t in job.tasks},
        "task_run_ids": {t.task_id: t.run_id for t in job.tasks if t.run_id},
        "execution_config": _export_execution_config(job.execution_config),
        "context_strategy": job.execution_config.context_strategy if job.execution_config else "task_bounded_sequential_job",
        "target_guard": _export_target_guard(job.target_guard),
        "error": job.error,
    }


def _build_job_summary_md(job: Any) -> str:
    lines = [
        f"# Remedy Job Evidence — {job.job_id}",
        "",
        f"**Title:** {job.job_title}",
        f"**Status:** {job.status}",
        f"**Repo:** {_sanitize_path(job.repo_path)}",
        f"**Created:** {job.created_at}",
    ]
    if job.finished_at:
        lines.append(f"**Finished:** {job.finished_at}")
    lines.append("")

    ec = job.execution_config
    if ec:
        lines.append("## Execution Config")
        lines.append(f"- Builder: {ec.builder} (source: {ec.builder_source})")
        lines.append(f"- Reviewer: {ec.reviewer} (source: {ec.reviewer_source})")
        lines.append(f"- Max rounds: {ec.max_rounds} (source: {ec.max_rounds_source})")
        lines.append(f"- Repair rounds: {ec.repair_rounds_allowed} (source: {ec.repair_rounds_source})")
        lines.append(f"- Context strategy: {ec.context_strategy}")
        lines.append("")

    lines.append("## Task Timeline")
    lines.append("")
    lines.append(f"1. Job planned at {job.created_at}")
    for task in job.tasks:
        status_str = task.status
        run_str = f" (run: {task.run_id})" if task.run_id else ""
        verdict_str = f", reviewer: {task.reviewer_verdict}" if task.reviewer_verdict else ""
        repair_str = f", repair: {task.repair_rounds_used}/{task.repair_rounds_allowed}" if task.repair_rounds_used else ""
        lines.append(f"2. {task.task_id}: {task.title} — {status_str}{run_str}{verdict_str}{repair_str}")
    if job.finished_at:
        lines.append(f"3. Job {job.status} at {job.finished_at}")
    lines.append("")

    tg = job.target_guard
    if tg:
        lines.append("## Target Guard")
        lines.append(f"- Target mutated: {tg.target_mutated}")
        if tg.changed_target_files:
            lines.append(f"- Changed files: {', '.join(tg.changed_target_files)}")
        lines.append("")

    lines.append("## Tasks")
    lines.append("")
    for task in job.tasks:
        lines.append(f"### {task.task_id}: {task.title}")
        lines.append(f"- Status: {task.status}")
        if task.run_id:
            lines.append(f"- Run ID: {task.run_id}")
        if task.final_status:
            lines.append(f"- Final: {task.final_status}")
        if task.test_passed is not None:
            lines.append(f"- Tests: {'passed' if task.test_passed else 'failed'}")
        if task.reviewer_verdict:
            lines.append(f"- Reviewer: {task.reviewer_verdict}")
        if task.repair_rounds_used:
            lines.append(f"- Repair: {task.repair_rounds_used}/{task.repair_rounds_allowed}")
        if task.apply_manifest and task.apply_manifest.applied_files:
            lines.append(f"- Applied: {len(task.apply_manifest.applied_files)} files")
        if task.error:
            lines.append(f"- Error: {task.error}")
        lines.append("")

    lines.append("---")
    lines.append("WARNING: Real target repo was NOT mutated. Changes exist only in the isolated job workspace.")

    return "\n".join(lines) + "\n"


def _build_job_report_safe(job: Any) -> dict[str, Any]:
    tasks = []
    for t in job.tasks:
        body_bounded = t.body[:_TASK_BODY_EVIDENCE_LIMIT] if t.body else ""
        if len(t.body) > _TASK_BODY_EVIDENCE_LIMIT:
            body_bounded += f"... (truncated, {len(t.body)} chars total)"
        tasks.append({
            "task_id": t.task_id,
            "title": t.title,
            "body_excerpt": body_bounded,
            "status": t.status,
            "run_id": t.run_id,
            "final_status": t.final_status,
            "test_passed": t.test_passed,
            "reviewer_verdict": t.reviewer_verdict,
            "repair_rounds_used": t.repair_rounds_used,
            "repair_rounds_allowed": t.repair_rounds_allowed,
            "error": t.error,
            "apply_manifest": _export_apply_manifest(t.apply_manifest),
            "proof_summary": _export_proof_summary(t.proof_summary),
        })
    return {
        "job_id": job.job_id,
        "job_title": job.job_title,
        "status": job.status,
        "repo_identity": _sanitize_path(job.repo_path),
        "created_at": job.created_at,
        "finished_at": job.finished_at,
        "error": job.error,
        "tasks": tasks,
    }


def _build_job_timeline(job: Any) -> dict[str, Any]:
    events: list[dict[str, str]] = []
    events.append({
        "event": "job_planned",
        "timestamp": job.created_at or "unavailable",
        "detail": f"Job {job.job_id} planned with {len(job.tasks)} tasks",
    })

    prev_applied_id = ""
    for task in job.tasks:
        if task.status in ("pending", "skipped"):
            events.append({
                "event": f"task_{task.status}",
                "timestamp": "unavailable",
                "detail": f"{task.task_id}: {task.title} — {task.status}",
            })
            continue

        if prev_applied_id:
            events.append({
                "event": "sequencing_proof",
                "timestamp": "unavailable",
                "detail": f"{task.task_id} started after {prev_applied_id} applied",
            })

        events.append({
            "event": "task_completed",
            "timestamp": "unavailable",
            "detail": (
                f"{task.task_id}: {task.title} — {task.status}"
                f" (run: {task.run_id})" if task.run_id else
                f"{task.task_id}: {task.title} — {task.status}"
            ),
            "run_id": task.run_id,
        })

        if task.status == "applied_to_job_workspace":
            prev_applied_id = task.task_id

    events.append({
        "event": "job_final",
        "timestamp": job.finished_at or "unavailable",
        "detail": f"Job {job.status}",
    })

    return {
        "job_id": job.job_id,
        "events": events,
        "sequencing_valid": _check_sequencing(job),
        "timestamps_available": bool(job.created_at and job.finished_at),
    }


def _check_sequencing(job: Any) -> bool:
    applied_seen = False
    for task in job.tasks:
        if task.status == "applied_to_job_workspace":
            applied_seen = True
        elif task.status in ("blocked", "failed") and applied_seen:
            return True
        elif task.status == "applied_to_job_workspace" and applied_seen:
            pass
    if job.status == "completed":
        return all(
            t.status in ("applied_to_job_workspace", "skipped")
            for t in job.tasks
        )
    return True


def _build_tasks_json(job: Any) -> list[dict[str, Any]]:
    tasks = []
    for t in job.tasks:
        tasks.append({
            "task_id": t.task_id,
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
        })
    return tasks


def _build_workspace_apply_json(job: Any) -> list[dict[str, Any]]:
    manifests = []
    for t in job.tasks:
        m = _export_apply_manifest(t.apply_manifest)
        manifests.append({
            "task_id": t.task_id,
            "status": t.status,
            "apply_manifest": m,
        })
    return manifests


def _build_workspace_diff(job: Any) -> str:
    ws_path = job.job_workspace_path
    repo_path = job.repo_path
    if not ws_path or not repo_path:
        return "# Workspace diff unavailable: no workspace or repo path\n"

    ws = Path(ws_path)
    repo = Path(repo_path)
    if not ws.exists():
        return "# Workspace diff unavailable: workspace directory does not exist\n"
    if not repo.exists():
        return "# Workspace diff unavailable: repo directory does not exist\n"

    diff_lines = ["# Job workspace diff (workspace vs original target repo)"]
    diff_lines.append(f"# Workspace: {_sanitize_path(ws_path)}")
    diff_lines.append(f"# Repo: {_sanitize_path(repo_path)}")
    diff_lines.append("")

    applied_files: list[str] = []
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.applied_files:
            applied_files.extend(t.apply_manifest.applied_files)

    if not applied_files:
        diff_lines.append("# No files applied to workspace")
        return "\n".join(diff_lines) + "\n"

    total_chars = sum(len(line) + 1 for line in diff_lines)
    capped = False
    for rel_path in sorted(set(applied_files)):
        if total_chars >= _WORKSPACE_DIFF_MAX_CHARS:
            capped = True
            break
        ws_file = ws / rel_path
        repo_file = repo / rel_path

        diff_lines.append(f"--- a/{rel_path}")
        diff_lines.append(f"+++ b/{rel_path}")

        if not ws_file.exists():
            diff_lines.append("# File missing from workspace")
            diff_lines.append("")
            continue

        try:
            ws_content = ws_file.read_text(errors="replace")
        except OSError:
            diff_lines.append("# Could not read workspace file")
            diff_lines.append("")
            continue

        if repo_file.exists():
            try:
                repo_content = repo_file.read_text(errors="replace")
            except OSError:
                repo_content = ""
        else:
            repo_content = ""

        if ws_content == repo_content:
            diff_lines.append("# No difference")
        else:
            ws_lines = ws_content.splitlines(keepends=True)
            repo_lines = repo_content.splitlines(keepends=True)

            import difflib
            unified = list(difflib.unified_diff(
                repo_lines, ws_lines,
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            ))
            if unified:
                for line in unified:
                    text = line.rstrip()
                    diff_lines.append(text)
                    total_chars += len(text) + 1
                    if total_chars >= _WORKSPACE_DIFF_MAX_CHARS:
                        capped = True
                        break
            else:
                diff_lines.append("# Files differ (binary or encoding)")
        diff_lines.append("")
        if capped:
            break

    if capped:
        diff_lines.append(
            f"# Workspace diff truncated at {_WORKSPACE_DIFF_MAX_CHARS} char total cap"
        )

    return "\n".join(diff_lines) + "\n"


def _write_task_run_evidence(
    task: Any,
    out_base: str,
    written: dict[str, str],
) -> None:
    task_out = _task_evidence_dir(out_base, task.task_id)
    task_rel = f"task_runs/{task.task_id}"

    if not task.run_id:
        _write_unavailable(task_out, task_rel, task.task_id, written,
                          f"No run_id for task {task.task_id} (status: {task.status})")
        return

    from packages.orchestration.pingpong_loop import load_run

    run_data = load_run(task.run_id)
    if run_data is None:
        _write_unavailable(task_out, task_rel, task.task_id, written,
                          f"Run data not found for {task.run_id}")
        return

    from packages.orchestration.pingpong_promote import load_promotion
    promotion_data = load_promotion(task.run_id)

    bundle = build_evidence_bundle(run_data, promotion_data)

    # Include prompt traces from persisted run dir
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir
    trace_file = _pingpong_runs_dir() / task.run_id / "prompt_trace.jsonl"
    if trace_file.exists():
        bundle["prompt_trace_jsonl_path"] = str(trace_file)

    task_written = write_evidence_bundle(bundle, str(task_out))

    for filename, path in task_written.items():
        written[f"{task_rel}/{filename}"] = path


def _write_unavailable(
    task_out: Path,
    task_rel: str,
    task_id: str,
    written: dict[str, str],
    reason: str,
) -> None:
    task_out.mkdir(parents=True, exist_ok=True)

    manifest = {
        "task_id": task_id,
        "evidence_available": False,
        "reason": reason,
    }
    manifest_path = task_out / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    written[f"{task_rel}/manifest.json"] = str(manifest_path)

    summary = f"# Task {task_id} Evidence\n\nEvidence unavailable: {reason}\n"
    summary_path = task_out / "summary.md"
    summary_path.write_text(summary)
    written[f"{task_rel}/summary.md"] = str(summary_path)


def _write_job_prompt_trace_summary(
    job: Any,
    out_base: str,
    written: dict[str, str],
) -> None:
    """Write aggregate prompt trace summary across all tasks."""
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir

    total_builder = 0
    total_reviewer = 0
    total_chars = 0
    total_tokens_est = 0
    task_traces: list[dict[str, Any]] = []

    for task in job.tasks:
        if not task.run_id:
            continue
        summary_file = _pingpong_runs_dir() / task.run_id / "prompt_trace_summary.json"
        if not summary_file.exists():
            task_traces.append({
                "task_id": task.task_id,
                "run_id": task.run_id,
                "prompt_trace_available": False,
            })
            continue
        try:
            data = json.loads(summary_file.read_text())
            total_builder += data.get("builder_prompts", 0)
            total_reviewer += data.get("reviewer_prompts", 0)
            total_chars += data.get("total_prompt_chars", 0)
            total_tokens_est += data.get("total_prompt_tokens_estimated", 0)
            task_traces.append({
                "task_id": task.task_id,
                "run_id": task.run_id,
                "prompt_trace_available": True,
                "builder_prompts": data.get("builder_prompts", 0),
                "reviewer_prompts": data.get("reviewer_prompts", 0),
            })
        except (OSError, json.JSONDecodeError):
            task_traces.append({
                "task_id": task.task_id,
                "run_id": task.run_id,
                "prompt_trace_available": False,
                "error": "parse_failed",
            })

    aggregate = {
        "total_builder_prompts": total_builder,
        "total_reviewer_prompts": total_reviewer,
        "total_prompts": total_builder + total_reviewer,
        "total_prompt_chars": total_chars,
        "total_prompt_tokens_estimated": total_tokens_est,
        "task_traces": task_traces,
    }

    out_path = Path(out_base).resolve()
    target = _validate_output_path(str(out_path), "prompt_trace_summary.json")
    target.write_text(json.dumps(_redact_json_value(aggregate), indent=2) + "\n")
    written["prompt_trace_summary.json"] = str(target)
