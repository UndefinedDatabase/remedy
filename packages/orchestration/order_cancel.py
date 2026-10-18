"""Cancelling an order the supervisor started: one operation for its whole lifecycle (exec-1017c, R-1338).

A client that started an order over `POST /api/v1/orders` could stop only the jobs it could see,
one by one, and none while the order was still planning: the walk (`do_sequence.walk_do_sequence`)
read no request, so a job its shape step saved after the client stopped the listed ones still ran.
`cancel_order` is the one operation, twinned by `remedy client cancel-order` and
`POST /api/v1/orders/{order}/cancel`:

1. The request is written first, create-only, as `cancel.json` in the order's own folder under the
   supervisor's `orders/`. A second cancel finds it and changes nothing (`already_cancelled`).
2. Every job the order's missions list for it is cancelled (`job_cancel.cancel_job`): a job no
   runner holds ends `cancelled` at once, a running one at its next safe point.
3. The walk, which `OrderLauncher` runs from that folder (the fact `serve_runs._process_is_this_order`
   reads to say the order runs), reads the request before every step and after it
   (`cancellable_do_steps`), and before every apply (`walk_cancel_note`). A step that sees it runs nothing; after the step it cancels every job of
   the walk the step made, so a job saved between the client's listing and the walk's reading is
   caught by one of the two (both write before they read). A planner call in flight is ended too
   (`planner_cancel.py`, exec-1018): the walk's reader is bound to it (`walk_cancel_reader`), the
   Ollama planner closes its own request's connection and the Claude CLI planner's child is ended by
   its guard, and the call writes no plan. A running job's Pi call ends through the job's stop
   request, within about a second. No Ollama server or other process outside the call is touched.

What landed stays: an applied result is never reverted. A completed result waiting for its apply is
the person's decision, so it is left as it is unless the request says `decline_results`, which
declines it with the cancel's reason. Nothing is deleted; the order's record and every job's
evidence stay readable. While the walk or a job still runs, the order reads `cancelling`, never
`cancelled`. A supervisor that restarts resumes no order, and a resumed run of a cancelled job is
refused, so a restart brings back nothing that was cancelled.
"""
from __future__ import annotations

import json
import os
import re
from collections.abc import Callable, Mapping
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

#: The order's cancel request, in its own folder beside `order.json`.
ORDER_CANCEL_FILENAME = "cancel.json"

#: The folder of the supervised order the walk in this process runs for, set when the walk starts;
#: None for a `remedy do` run in a terminal, which a person stops with Ctrl-C.
_WALK_ORDER_DIR: ContextVar[Path | None] = ContextVar("walk_order_dir", default=None)
_ORDER_FOLDER_NAME = re.compile(r"[0-9a-f]{16}")

#: An order's `phase`: what a person reads first. `planning` while the walk runs and no job of it
#: does, `running` while a job does, `awaiting_apply` for a result waiting for an apply or a
#: decline, `needs_plan_approval`, `waiting` for a job that waits for its predecessor, `ready` for
#: one that may run now, `blocked`, `failed`, `stopped` (resumable), `cancelling` until nothing of
#: a cancelled order runs any more, `cancelled`, `done` when every job's result was applied or
#: declined or the job only ran its checks, `ended` for a walk that ended with no job (its answer says why), `lost` when the
#: walk's process is gone with no recorded end.
ORDER_PHASES = ("planning", "running", "awaiting_apply", "needs_plan_approval", "waiting", "ready",
                "blocked", "failed", "stopped", "cancelling", "cancelled", "done", "ended", "lost")

#: What one cancel did to each job of the order (`outcome` of an entry of `jobs`).
ORDER_CANCEL_JOB_OUTCOMES = ("cancelled", "cancel_pending", "already_cancelled", "declined",
                             "awaiting_decision", "applied", "ended", "not_requested")

#: The keys of an answer of `cancel_order`, sorted, and the keys under its `cancel` and its `jobs`.
ORDER_CANCEL_ANSWER_KEYS = ("already_cancelled", "cancel", "jobs", "order_id", "phase", "state")
ORDER_CANCEL_ANSWER_TREE: dict[str, Any] = {
    "cancel": {key: {} for key in ("reason", "source", "requested_at")},
    "jobs": {key: {} for key in ("job_id", "before", "job_status", "outcome")}}


class OrderCancelError(Exception):
    """The order's folder cannot hold a cancel request."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def order_cancel_request(order_dir: Path) -> dict[str, str] | None:
    """The cancel request in *order_dir*, or None. Unreadable content still cancels."""
    try:
        raw = (order_dir / ORDER_CANCEL_FILENAME).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError:
        raw = ""
    try:
        data = json.loads(raw)
    except ValueError:
        data = {}
    data = data if isinstance(data, dict) else {}
    return {"reason": str(data.get("reason") or "unknown")[:500],
            "source": str(data.get("source") or "unknown")[:120],
            "requested_at": str(data.get("requested_at") or "")[:64]}


def _publish_order_cancel(order_dir: Path, *, reason: str, source: str) -> tuple[dict[str, str], bool]:
    """Write the request once; ``(request, already)`` where *already* says one was there before."""
    from packages.common import secure_fs as _fs

    request = {"reason": (reason or "cancelled")[:500], "source": (source or "cli")[:120],
               "requested_at": _now()}
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        dir_fd = os.open(order_dir, flags)
    except OSError as exc:
        raise OrderCancelError(f"the order's folder cannot be opened: {exc}") from exc
    try:
        published = _fs.write_file_atomically(dir_fd, ORDER_CANCEL_FILENAME, _fs.json_bytes(request),
                                              create_only=True, file_mode=0o600,
                                              error_cls=OrderCancelError, noun="order cancel request")
    finally:
        os.close(dir_fd)
    return (order_cancel_request(order_dir) or request), not published


def _runner_alive(paths: Any, job_id: str, walk_alive: bool) -> bool:
    """True when a process may still run *job_id*: the order's walk, or a run the supervisor started."""
    from packages.orchestration.serve_runs import read_run_record, run_state

    if walk_alive:
        return True
    run = read_run_record(paths, job_id)
    return run is not None and run_state(paths, run) == "running"


def _cancel_one(job: Any, request: dict[str, str], *, runner_alive: bool,
                decline_results: bool) -> str:
    """Cancel one job of the order; its outcome (one of `ORDER_CANCEL_JOB_OUTCOMES`)."""
    from packages.orchestration.job_apply import decline_job_result, job_apply_landed, job_result_decline
    from packages.orchestration.job_cancel import JobCancelRefused, cancel_job
    from packages.orchestration.pingpong_job import save_job_plan
    from packages.orchestration.safe_points import StopControlError

    state = getattr(job.state, "value", str(job.state))
    if state == "completed":
        if job_apply_landed(str(job.job_id)):
            return "applied"
        if job_result_decline(job) is None and decline_results:
            decline_job_result(job, reason=f"the order was cancelled: {request['reason']}",
                               source=request["source"], now=datetime.now(timezone.utc))
            save_job_plan(job)
        return "declined" if job_result_decline(job) is not None else "awaiting_decision"
    try:
        answer = cancel_job(job, reason=request["reason"], source=request["source"],
                            runner_alive=runner_alive)
    except JobCancelRefused:
        return "ended"
    except StopControlError:
        return "not_requested"          # its control area cannot be written: the job is unchanged
    if answer["already_cancelled"]:
        return "already_cancelled"
    return "cancel_pending" if answer["cancel_pending"] else "cancelled"


def cancel_order(paths: Any, record: Any, *, reason: str, source: str,
                 decline_results: bool = False) -> dict[str, Any]:
    """Cancel the order *record* names; the answer `remedy client cancel-order --json` prints.

    Raises `OrderCancelError` when the request cannot be written; nothing is cancelled then.
    """
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.serve_runs import order_record_job_ids, order_state

    order_dir = paths.orders_dir / record.order_id
    request, already = _publish_order_cancel(order_dir, reason=reason, source=source)
    state = order_state(paths, record)
    jobs: list[dict[str, str]] = []
    for job_id in order_record_job_ids(record):
        job = load_job_plan(job_id)
        if job is None:
            continue
        before = getattr(job.state, "value", str(job.state))
        outcome = _cancel_one(job, request, runner_alive=_runner_alive(paths, job_id, state == "running"),
                              decline_results=decline_results)
        after = load_job_plan(job_id)
        jobs.append({"job_id": job_id, "before": before, "outcome": outcome,
                     "job_status": getattr(after.state, "value", str(after.state)) if after else before})
    from packages.orchestration.order_jobs import order_jobs_view

    phase = order_phase(state, request, order_jobs_view([entry["job_id"] for entry in jobs]), record.exit_code)
    return {"order_id": record.order_id, "state": state, "phase": phase,
            "already_cancelled": already, "cancel": request, "jobs": jobs}


def order_phase(state: str, cancel: dict[str, str] | None, jobs: list[dict[str, Any]],
                exit_code: int | None) -> str:
    """The order's `phase` (one of `ORDER_PHASES`) from its process *state* and its jobs' view."""
    phases = [job["phase"] for job in jobs]
    if cancel is not None:
        # Cancelled once nothing of the order can run: no walk, no running job, no job a cancel
        # could not reach (its control area unwritable). A result waiting for its apply is the
        # person's to answer and runs nothing.
        still = {"running", "ready", "waiting", "needs_plan_approval", "blocked", "stopped"}
        return "cancelling" if state == "running" or still & set(phases) else "cancelled"
    if state == "running":
        return "running" if "running" in phases else "planning"
    if state == "lost":
        return "lost"
    for phase in ("running", "awaiting_apply", "needs_plan_approval", "blocked", "failed", "stopped",
                  "ready", "waiting"):
        if phase in phases:
            return phase
    if phases and all(phase in ("applied", "declined", "cancelled", "checked") for phase in phases):
        return "cancelled" if all(phase == "cancelled" for phase in phases) else "done"
    return "failed" if exit_code not in (0, None) else "ended"


# ---------------------------------------------------------------------------
# The walk's side: it reads the request; it never writes one.
# ---------------------------------------------------------------------------


def walk_order_dir() -> Path | None:
    """The supervised order folder this process runs from, or None.

    `OrderLauncher` starts every order's walk with that folder as its working directory, so a walk
    running from `<serve>/orders/<order id>/` is that order's walk; any other folder is not.
    """
    from packages.orchestration.serve_paths import serve_paths

    try:
        cwd = Path.cwd().resolve()
        orders = serve_paths().orders_dir.resolve()
    except OSError:
        return None
    if cwd.parent != orders or not _ORDER_FOLDER_NAME.fullmatch(cwd.name):
        return None
    return cwd if (cwd / "order.json").is_file() else None


def walk_cancel_request() -> dict[str, str] | None:
    """The cancel request of the order this walk runs for, or None (none, or not a supervised order)."""
    order_dir = _WALK_ORDER_DIR.get()
    return order_cancel_request(order_dir) if order_dir is not None else None


def walk_cancel_reader() -> Callable[[], str] | None:
    """For a supervised walk, the reader of its order's cancel reason ("" while none); else None.

    A planner call binds it (`planner_cancel.planner_call_scope`), so a cancel ends that call in
    flight (exec-1018, R-1346); outside a supervised order no planner call is made cancellable.
    """
    if _WALK_ORDER_DIR.get() is None:
        return None

    def reason() -> str:
        request = walk_cancel_request()
        return "" if request is None else f"the order was cancelled ({request['reason']})"
    return reason


def walk_cancel_note() -> str:
    """Why the walk must not apply now ("" when it may): the words of the order's cancel request."""
    request = walk_cancel_request()
    return "" if request is None else f"the order was cancelled ({request['reason']}); nothing was applied"


def _cancel_walk_jobs(ctx: Any, request: dict[str, str]) -> str:
    """Cancel every job of the walk that has not ended; the note naming them, or ""."""
    from packages.orchestration.pingpong_job import load_job_plan

    cancelled: list[str] = []
    for job_id in list(ctx.job_ids):
        job = load_job_plan(job_id)
        # No job of this walk runs while the walk is between steps: it runs them in this process.
        if job is not None and _cancel_one(job, request, runner_alive=False,
                                           decline_results=False) == "cancelled":
            cancelled.append(job_id)
    return f"; cancelled job(s) {', '.join(cancelled)}" if cancelled else ""


def cancellable_do_steps(steps: Mapping[str, Callable[[Any], tuple[str, str]]]
                         ) -> Mapping[str, Callable[[Any], tuple[str, str]]]:
    """*steps*, each reading the order's cancel request before and after it runs.

    The order's folder is read once, when the walk starts (`walk_order_dir`); outside a supervised
    order the table is returned unchanged.
    """
    order_dir = walk_order_dir()
    _WALK_ORDER_DIR.set(order_dir)
    if order_dir is None:
        return steps
    return {name: _cancellable_step(name, step) for name, step in steps.items()}


def _cancellable_step(name: str, step: Callable[[Any], tuple[str, str]]) -> Callable[[Any], tuple[str, str]]:
    from packages.orchestration.do_context import DO_STEP_FAILED, DO_STEP_STOPPED

    def run(ctx: Any) -> tuple[str, str]:
        request = walk_cancel_request()
        if request is not None:
            return DO_STEP_STOPPED, (f"not run: the order was cancelled ({request['reason']})"
                                     f"{_cancel_walk_jobs(ctx, request)}")
        from packages.orchestration.planner_cancel import PlannerCallCancelled

        try:
            status, detail = step(ctx)
        except PlannerCallCancelled as ended:      # exec-1018 (R-1346): its planner call ended in flight
            status, detail = DO_STEP_STOPPED, (f"its planner call was ended after {ended.seconds:.1f} s "
                                               f"and wrote no plan")
        request = walk_cancel_request()
        if request is None:
            return status, detail
        note = _cancel_walk_jobs(ctx, request)
        if status in (DO_STEP_FAILED, DO_STEP_STOPPED) or note:
            # A job the cancel ended reads failed to the step that ran it: say what ended it.
            return DO_STEP_STOPPED, f"the order was cancelled during {name} ({request['reason']}): {detail}{note}"
        return status, detail
    return run
