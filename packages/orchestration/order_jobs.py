"""What one order is made of, read without knowing a job id: its jobs, which one runs, which wait and why.

An HTTP client starts an order and gets an order id back; the jobs the walk plans appear only in
the answer `remedy do` prints at its very end. While the walk runs, a client could not say what
was happening, and once it ended, a job that waited for its predecessor's apply carried no word
of what it was waiting for. This module reads the order's jobs from the records that already hold
them, the batches of the repositories' missions (DECISION amend1011b D3: a job link names its
batch by `order_id`, and a batch records the order file it came from), and writes the one fact no
record held: which job a waiting job waits for (`ORDER_JOB_WAITS_KEY`, written by the run step).

Remedy deliberately keeps no second order-to-job index: the mission chain stays the one record of
which jobs exist, so a job is never listed under an order it does not belong to.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

#: The job metadata key naming the job of the same order a waiting job runs after.
ORDER_JOB_WAITS_KEY = "waits_for_job"
#: Why such a job waits, in the words of DECISION F268 D12.
ORDER_JOB_WAIT_REASON = ("its workspace is cut from the repository's HEAD commit, so it runs once "
                         "job {job} is applied and committed")
#: Why it still waits when that job ended without its result landing (exec-1017c): nothing will
#: release it, so the person cancels it or runs it on the repository as it is.
ORDER_JOB_ORPHANED_REASON = ("job {job} was {ended} and its result will not be applied, so nothing "
                             "releases this job: cancel it, or run it on the repository as it is")

#: The `phase` of a job in an order's view: what a person needs to know first. `needs_plan_approval`
#: is a task plan waiting for its approval, `awaiting_apply` a finished result waiting for the
#: person's apply or decline (nothing lands on its own), `blocked` a job its checks or a decision hold,
#: `stopped` a job stopped on purpose that can be resumed, `cancelled` one that ended for good
#: (`job_cancel.py`, exec-1017c).
ORDER_JOB_PHASES = ("running", "waiting", "ready", "needs_plan_approval", "awaiting_apply", "applied",
                    "declined", "blocked", "stopped", "cancelled", "failed")


#: The keys of one entry of `order_jobs_view`, as the machine client interface declares them.
ORDER_JOBS_KEY_TREE: dict[str, Any] = {key: {} for key in (
    "job_id", "title", "state", "phase", "executable", "waits_for", "waiting_reason", "verification",
    "story")} | {"tasks": {"total": {}, "done": {}, "current": {}}}


def record_job_waits(job_ids: list[str], waiting_ids: list[str]) -> None:
    """Name, on each waiting job, the job of the same order before it, which it waits for."""
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    for position, job_id in enumerate(job_ids):
        if position == 0 or job_id not in waiting_ids:
            continue
        job = load_job_plan(job_id)
        if job is not None:
            job.metadata[ORDER_JOB_WAITS_KEY] = job_ids[position - 1]
            save_job_plan(job)


def order_file_job_ids(source_path: str, *, since: str = "") -> list[str]:
    """The jobs of the order run from *source_path*, in planned order, over every repository it touched.

    *source_path* is compared as the mission batch records it (a resolved absolute path). With
    *since*, only batches created at or after it count, so an order file sent again (a key) lists
    the jobs of this run, not of an earlier one.
    """
    from packages.orchestration.mission_state import list_missions, project_ids_with_missions

    if not source_path:
        return []
    start = _moment(since)
    found: list[str] = []
    for project_id in project_ids_with_missions():
        for mission in list_missions(project_id):
            batches = {batch.order_id for batch in mission.orders
                       if batch.source_path == source_path and _not_before(batch.created_at, start)}
            found += [link.job_id for link in mission.job_links if link.order_id in batches]
    return list(dict.fromkeys(found))


def _moment(text: str) -> datetime | None:
    """*text* as a time ("...Z" and "+00:00" alike), or None when it is empty or not one."""
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")) if text else None
    except ValueError:
        return None


def _not_before(text: str, start: datetime | None) -> bool:
    moment = _moment(text)
    return start is None or (moment is not None and moment >= start)


def order_jobs_view(job_ids: list[str]) -> list[dict[str, Any]]:
    """One entry per job: its title, state, phase, tasks, what it waits for and its verification.

    `phase` (one of `ORDER_JOB_PHASES`) is what a person reads first; `state` is the job's own
    lifecycle word. `executable` is true for the job that may run now; `waits_for` names the job
    it runs after and `waiting_reason` why. A job whose record cannot be read is listed with
    state `missing`, never left out.
    """
    from packages.orchestration.pingpong_job import load_job_plan

    view: list[dict[str, Any]] = []
    for job_id in job_ids:
        job = load_job_plan(job_id)
        view.append(_missing(job_id) if job is None else _job_entry(job))
    return view


def _missing(job_id: str) -> dict[str, Any]:
    return {"job_id": job_id, "title": "", "state": "missing", "phase": "failed", "executable": False,
            "tasks": {"total": 0, "done": 0, "current": ""}, "waits_for": None, "waiting_reason": "",
            "verification": None, "story": f"/api/v1/jobs/{job_id}/story"}


def _wait_reason(waits_for: str) -> str:
    """Why a job waits for *waits_for*: its apply, or nothing any more when that job ended without one."""
    from packages.orchestration.job_apply import job_result_decline
    from packages.orchestration.pingpong_job import load_job_plan

    before = load_job_plan(waits_for)
    state = getattr(getattr(before, "state", None), "value", "")
    ended = ("cancelled" if state == "cancelled" else "failed" if state == "failed" else
             "declined" if before is not None and job_result_decline(before) is not None else "")
    return (ORDER_JOB_ORPHANED_REASON.format(job=waits_for, ended=ended) if ended
            else ORDER_JOB_WAIT_REASON.format(job=waits_for))


def _job_entry(job: Any) -> dict[str, Any]:
    from packages.orchestration.job_apply import job_apply_landed, job_result_decline
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.order_verification import job_verification
    from packages.orchestration.pingpong_job import TASK_DONE_STATUSES, TASK_RUNNING

    state = getattr(job.state, "value", str(job.state))
    waits_for = str(job.metadata.get(ORDER_JOB_WAITS_KEY) or "") or None
    waiting = bool(waits_for) and state in ("planned", "pending") and not job_apply_landed(waits_for)
    done = sum(1 for task in job.tasks if task.status in TASK_DONE_STATUSES)
    current = next((task.title for task in job.tasks if task.status == TASK_RUNNING), "")
    if state == "running":
        phase = "running"
    elif waiting:
        phase = "waiting"
    elif state in ("planned", "pending"):
        phase = "needs_plan_approval" if task_plan_blocks_execution(job) is not None else "ready"
    elif state == "completed":
        phase = ("applied" if job_apply_landed(str(job.job_id))
                 else "declined" if job_result_decline(job) is not None else "awaiting_apply")
    elif state in ("stopped", "cancelled"):
        phase = state
    elif state == "blocked":
        phase = "blocked"
    else:
        phase = "failed"
    return {
        "job_id": str(job.job_id), "title": job.job_title, "state": state, "phase": phase,
        "executable": phase == "ready",
        "tasks": {"total": len(job.tasks), "done": done, "current": current},
        "waits_for": waits_for if waiting else None,
        "waiting_reason": _wait_reason(waits_for) if waiting else "",
        "verification": job_verification(job)["status"],
        "story": f"/api/v1/jobs/{job.job_id}/story",
    }
