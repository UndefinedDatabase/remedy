"""Review reports: one file per `remedy do` walk that asked for it, written without anyone naming a job.

`remedy do run --capture-review` (and `capture_review: true` on `POST /api/v1/orders`, which passes
that flag) makes the walk leave `<data root>/review_reports/<report id>.json`: the effective order
and configuration, the lane and why, the planning calls, every job and task with its runs, their
phase times, the providers' measured usage, each Pi call's model turns and tool calls, the
verification, the changed files, the review verdicts, the errors and the outcome. A reviewer reads
the last ten of them in every review ZIP (`scripts/stage_review_reports.py`), so nobody has to
record a job id or run an export command.

The report is written twice, atomically and under one stable id: once when the walk starts, with
`status` `running`, and once when it ends, whatever ended it: success, a failed or stopped step, a
budget, an exception, Ctrl-C or SIGTERM (`cancelled`). A process killed outright leaves the first
write, which says honestly that it never finished. Nothing is invented: a figure a provider did
not report is null, and `not_measured` names what this report cannot know.

What a report never holds: a credential (every string passes `stream_evidence.redact_json_value`),
a whole model prompt (only the run records' prompt sizes and hashes stay where they are), the
operator's home directory (written as `~`), or the run records' working-directory paths.
These reports are Remedy's own review evidence, unrelated to Universe's Improve tasks or Luna's
reports.
"""
from __future__ import annotations

import contextlib
import json
import os
import secrets
import signal
import threading
from collections import Counter
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration import data_paths

#: The data-root class the reports live in (registered in `data_paths.DURABLE_CLASSES`).
REVIEW_REPORTS_CLASS = "review_reports"
REVIEW_REPORT_SCHEMA = "remedy_review_report_v1"

#: What a report cannot measure from inside the walk, said once in every report.
NOT_MEASURED = (
    "queue time before the walk's process started (an HTTP order's wait is in its order record)",
    "inference time apart from tool time inside one Pi call (Pi's stream has no response-end time)",
    "planner tokens (local planners report none; the order budget's planning figures are estimates)",
)


def review_reports_dir(root: Path | None = None) -> Path:
    """`<data root>/review_reports`, git-ignored with the rest of the data root."""
    return (root if root is not None else data_paths.resolve_data_root()) / REVIEW_REPORTS_CLASS


def _now() -> datetime:
    return datetime.now(timezone.utc)


def new_review_report_id(moment: datetime | None = None) -> str:
    """`rr-<UTC time>-<8 hex>`: sorts by start time, unique without a lock."""
    return f"rr-{(moment or _now()):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}"


def redact_review_report(value: Any) -> Any:
    """Secrets redacted, the home directory written as `~`, in every string of *value*."""
    from packages.orchestration.stream_evidence import redact_json_value

    home = os.path.expanduser("~")
    text = json.dumps(redact_json_value(value), ensure_ascii=False)
    if home and home != "/":
        text = text.replace(json.dumps(home)[1:-1], "~")
    return json.loads(text)


def _seconds(start: str | None, end: str | None) -> float | None:
    try:
        return round((datetime.fromisoformat(str(end)) - datetime.fromisoformat(str(start))).total_seconds(), 3)
    except (TypeError, ValueError):
        return None


def _pi_calls(run_id: str) -> dict[str, list[dict[str, Any]]]:
    """Each Pi call of a run by role: turns, tool calls by name, tool errors, its limit and duration."""
    calls: dict[str, list[dict[str, Any]]] = {}
    for path in sorted((data_paths.run_dir(run_id) / "pi").glob("*.jsonl")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            tools = record.get("tool_calls") if isinstance(record.get("tool_calls"), list) else []
            calls.setdefault(str(record.get("role") or path.stem), []).append({
                "model_turns": record.get("model_turns"), "tool_calls": len(tools),
                "tool_calls_by_name": dict(sorted(Counter(map(str, tools)).items())),
                "tool_errors": record.get("tool_errors"), "duration_ms": record.get("duration_ms"),
                "usage": record.get("usage") or None, "model": record.get("model"),
                "stop_reason": record.get("stop_reason"), "error": record.get("error") or "",
                "loop_limits": record.get("loop_limits"), "loop_limit_tripped": record.get("loop_limit_tripped") or ""})
    return calls


def _run_report(run_id: str) -> dict[str, Any]:
    """One task run as its result.json records it, reduced to what a reviewer needs."""
    try:
        run = json.loads((data_paths.run_dir(run_id) / "result.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"run_id": run_id, "missing": "the run's result.json could not be read"}
    evidence = run.get("provider_evidence") or {}
    rounds = [{
        "round": rd.get("round"), "kind": rd.get("kind"), "started_at": rd.get("started_at"),
        "finished_at": rd.get("finished_at"),
        "builder_ms": (rd.get("builder") or {}).get("duration_ms"),
        "reviewer_ms": (rd.get("reviewer") or {}).get("duration_ms"),
        "test_passed": rd.get("test_passed"), "test_summary": rd.get("test_summary"),
        "reviewer_verdict": (rd.get("reviewer") or {}).get("verdict"),
        "reviewer_findings": (rd.get("reviewer") or {}).get("finding_count"),
        "reviewer_summary": str((rd.get("reviewer") or {}).get("summary") or "")[:600],
    } for rd in run.get("rounds") or []]
    return {
        "run_id": run_id, "final_status": run.get("final_status"), "error": run.get("error") or "",
        "started_at": run.get("started_at"), "finished_at": run.get("finished_at"),
        "duration_s": _seconds(run.get("started_at"), run.get("finished_at")),
        "goal": str(run.get("goal") or "")[:600], "rounds": rounds,
        "changed_files": list(run.get("staged_files") or run.get("safe_diff_files") or []),
        "provider_calls": [{key: attempt.get(key) for key in ("role", "provider", "round", "usage", "error",
                                                              "is_retry", "is_parse_retry")}
                           for attempt in evidence.get("provider_attempts") or []],
        "usage": evidence.get("usage"), "usage_source": evidence.get("parse_source"),
        "pi_calls": _pi_calls(run_id), "rate_limit_waits": run.get("rate_limit_waits") or [],
    }


def _job_report(job_id: str) -> dict[str, Any]:
    from packages.orchestration.dod_gate import load_gate_result
    from packages.orchestration.execution_config import _export_execution_config
    from packages.orchestration.order_verification import job_verification
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.task_deliverables import task_deliverable

    job = load_job_plan(job_id)
    if job is None:
        return {"job_id": job_id, "missing": "the job record could not be read"}
    gate = load_gate_result(job_id) or {}
    from packages.orchestration.order_jobs import ORDER_JOB_WAITS_KEY

    return {
        "job_id": job_id, "title": job.job_title, "state": getattr(job.state, "value", str(job.state)),
        "waits_for": str(job.metadata.get(ORDER_JOB_WAITS_KEY) or "") or None, "error": job.error or "",
        "stop_reason": getattr(job, "stop_reason", "") or "", "stop_source": getattr(job, "stop_source", "") or "",
        "created_at": job.created_at, "first_running_at": job.first_running_at, "finished_at": job.finished_at,
        "duration_s": _seconds(job.first_running_at, job.finished_at),
        "execution_config": _export_execution_config(job.execution_config),
        "budgets": job.budgets if isinstance(job.budgets, dict) or job.budgets is None else job.budgets.model_dump(),
        "budget_actuals": job.budget_actuals,
        "verification": job_verification(job),
        "dod_checks": [{key: check.get(key) for key in ("check_id", "kind", "status", "reason", "blocking",
                                                       "exit_code", "duration_ms", "cwd")}
                       for check in gate.get("checks") or [] if isinstance(check, dict)],
        "tasks": [{"task_id": str(task.task_id), "title": task.title, "deliverable": task_deliverable(task),
                   "files": list(task.files_hint) or [task_deliverable(task)],
                   "final_status": task.final_status, "reviewer_verdict": task.reviewer_verdict,
                   "test_passed": task.test_passed, "changed_files": list(task.safe_diff_files or []),
                   "runs": [_run_report(str(task.run_id))] if task.run_id else []}
                  for task in job.tasks],
    }


def _outcome(ctx: Any, ended_by: str) -> dict[str, str]:
    """The walk's outcome word and why: `completed`, `failed`, `stopped`, `budget_exhausted`, `cancelled`."""
    if ended_by:
        return {"status": "cancelled" if ended_by in ("SIGTERM", "KeyboardInterrupt") else "crashed",
                "reason": ended_by}
    failed = next((r for r in ctx.results if r.status == "failed"), None)
    stopped = next((r for r in ctx.results if r.status == "stopped" and r.name != "apply"), None)
    end = failed or stopped
    budget = "budget" in (end.detail if end else "") or any(
        getattr(job, "stop_source", "") == "budget" for job in _loaded_jobs(ctx))
    if end is None:
        return {"status": "completed", "reason": "every step ran; nothing is applied without approval"
                if ctx.stopped_before_apply else "every step ran and the apply step applied"}
    status = "budget_exhausted" if budget else ("failed" if failed else "stopped")
    return {"status": status, "reason": f"{end.name}: {end.detail}"[:600]}


def _loaded_jobs(ctx: Any) -> list[Any]:
    from packages.orchestration.pingpong_job import load_job_plan

    return [job for job in (load_job_plan(job_id) for job_id in ctx.job_ids) if job is not None]


def build_review_report(ctx: Any, report_id: str, started_at: str, *, ended_by: str = "",
                        running: bool = False) -> dict[str, Any]:
    """The report of the walk *ctx* as it stands; `running` marks the write made when it starts."""
    from packages.orchestration.do_summary import do_cost_summary

    lane = getattr(ctx, "lane", None)
    ended_at = None if running else _now().isoformat()
    report: dict[str, Any] = {
        "schema": REVIEW_REPORT_SCHEMA, "report_id": report_id,
        "started_at": started_at, "ended_at": ended_at, "duration_s": _seconds(started_at, ended_at),
        "outcome": {"status": "running", "reason": "the walk has not ended; a report that stays so was "
                    "left by a process that did not finish"} if running else _outcome(ctx, ended_by),
        "order": {"text": ctx.order, "source": "order_file" if ctx.order_source_path else "text",
                  "source_sha256": ctx.order_source_sha256 or None, "order_id": ctx.order_id or None,
                  "mission_id": ctx.mission_id or None},
        "configuration": {
            "repository": ctx.repo_root or ctx.repo, "lane": getattr(lane, "lane", None),
            "lane_reason": getattr(lane, "reason", None), "shape": ctx.shape or None,
            "shape_source": ctx.shape_source or None,
            "providers": {"builder": ctx.builder_provider, "reviewer": ctx.reviewer_provider,
                          "planner": ctx.planner_provider, "builder_model": ctx.builder_model,
                          "reviewer_model": ctx.reviewer_model, "planner_model": ctx.planner_model},
            "flags": {name: getattr(ctx, name) for name in (
                "no_llm", "run_unattended", "force_job", "force_mission", "plan_only", "rehearse", "apply",
                "commit_auto", "commit_with_history", "push", "capture_review")},
            "commit_mode": ctx.commit_mode or None, "budgets": ctx.budgets},
        "planning": ctx.ledger.summary() if ctx.ledger is not None else None,
        "steps": [result.to_json() for result in ctx.results],
        "job_ids": list(ctx.job_ids), "waiting_job_ids": list(ctx.waiting_job_ids),
        "jobs": [] if running else [_job_report(job_id) for job_id in ctx.job_ids],
        "usage_by_role": None if running else do_cost_summary(ctx),
        "landed": list(ctx.landed), "next": list(ctx.next_lines),
        "not_measured": list(NOT_MEASURED),
    }
    return redact_review_report(report)


def write_review_report(report: dict[str, Any], root: Path | None = None) -> Path:
    """Write *report*, redacted, atomically under its id; the same id always names the same file."""
    from packages.common.secure_fs import durable_write_json

    path = review_reports_dir(root) / f"{report['report_id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    durable_write_json(path, redact_review_report(report))
    return path


@contextlib.contextmanager
def capture_review_report(ctx: Any) -> Iterator[None]:
    """Around a walk: a `running` report first, the final one whatever ends the walk (see the module text)."""
    if not getattr(ctx, "capture_review", False):
        yield
        return
    started = _now()
    report_id = new_review_report_id(started)
    write_review_report(build_review_report(ctx, report_id, started.isoformat(), running=True))
    previous = None
    if threading.current_thread() is threading.main_thread():
        def _on_sigterm(_signum: int, _frame: Any) -> None:
            raise KeyboardInterrupt("SIGTERM")
        previous = signal.signal(signal.SIGTERM, _on_sigterm)
    ended_by = ""
    try:
        yield
    except BaseException as exc:
        ended_by = str(exc) if str(exc) == "SIGTERM" else type(exc).__name__
        raise
    finally:
        if previous is not None:
            signal.signal(signal.SIGTERM, previous)
        try:
            report = build_review_report(ctx, report_id, started.isoformat(), ended_by=ended_by)
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:   # the walk's own end wins
            report = redact_review_report({"schema": REVIEW_REPORT_SCHEMA, "report_id": report_id,
                             "started_at": started.isoformat(), "ended_at": _now().isoformat(),
                             "outcome": {"status": "incomplete", "reason": f"the report could not be "
                                         f"built: {type(exc).__name__}: {exc}"[:600]},
                             "job_ids": list(ctx.job_ids), "not_measured": list(NOT_MEASURED)})
        write_review_report(report)
        ctx.review_report = {"report_id": report_id, "status": report["outcome"]["status"],
                             "file": f"{REVIEW_REPORTS_CLASS}/{report_id}.json"}
