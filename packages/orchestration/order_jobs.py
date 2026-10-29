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
from pathlib import Path
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
#: is a task plan waiting for its approval (`declined` once the person rejected it), `awaiting_apply`
#: a finished result waiting for the person's apply or decline (nothing lands on its own), `blocked`
#: a job its checks or a decision hold, `stopped` a job stopped on purpose that can be resumed,
#: `cancelled` one that ended for good (`job_cancel.py`, exec-1017c), `checked` a job with no build
#: task that ran its checks and has nothing to apply (a verification-only order's, exec-1018).
ORDER_JOB_PHASES = ("running", "waiting", "ready", "needs_plan_approval", "awaiting_apply", "applied",
                    "declined", "blocked", "stopped", "cancelled", "failed", "checked")


#: The keys of one entry of `order_jobs_view`, as the machine client interface declares them;
#: `blocking_criterion` and `mission_id` since 1.29 (DECISION amend1023 D11).
ORDER_JOBS_KEY_TREE: dict[str, Any] = {key: {} for key in (
    "job_id", "title", "state", "phase", "executable", "waits_for", "waiting_reason", "verification",
    "story", "blocking_criterion", "mission_id", "stop_text")} | {"tasks": {"total": {}, "done": {}, "current": {}}}


#: F323: the job metadata key naming, on the awaited job, the job that waits for it.
ORDER_JOB_RELEASES_KEY = "released_job"
#: F323: the stop reason token of a waiting job whose awaited job ended without a result that lands.
ORDER_JOB_AWAITED_ENDED = "awaited_job_ended"
#: F323: the sentence such a job carries (its metadata `job_stop_text.JOB_STOP_TEXT_KEY`).
ORDER_JOB_AWAITED_ENDED_TEXT = ("This job waited for job {job}, which ended {ended}{why}, so its result "
                                "will not be applied and this job did not run. Run it on the repository "
                                "as it is (remedy job run {me}), or cancel it.")


def record_job_waits(job_ids: list[str], waiting_ids: list[str]) -> None:
    """Name, on each waiting job, the job of the same order before it, which it waits for, and on
    that job the one it releases (F323)."""
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    for position, job_id in enumerate(job_ids):
        if position == 0 or job_id not in waiting_ids:
            continue
        job = load_job_plan(job_id)
        if job is not None:
            job.metadata[ORDER_JOB_WAITS_KEY] = job_ids[position - 1]
            save_job_plan(job)
        before = load_job_plan(job_ids[position - 1])
        if before is not None:
            before.metadata[ORDER_JOB_RELEASES_KEY] = job_id
            save_job_plan(before)


#: F323/F324: the job metadata key that says a job runs unattended (`job_unattended`).
JOB_UNATTENDED_KEY = "unattended"


def start_released_job(twin: str, segments: dict[str, str], envelope: dict[str, Any],
                       start_run: Any) -> dict[str, Any]:
    """F323: ENVELOPE of an HTTP apply, with the waiting job it started under `released`.

    After an apply over HTTP that landed a commit, the job of the same order that waited for it is
    released (`release_waiting_job`) and, when it runs unattended, started by the supervisor:
    nobody has to come back to start the rest of an order. A job that asks questions is released
    and left `ready` for its person. A start that is refused is named under `release_refused`.
    The released job runs with the roles the job it waited for ran with (`released_run_options`).
    """
    if twin != "job.apply" or not envelope.get("ok") or not envelope.get("commit_sha") or start_run is None:
        return envelope
    from packages.orchestration.data_paths import JobIdError, lookup_job_id
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import RunRefused, run_record_payload

    try:
        awaited_id = lookup_job_id(segments["job"])
    except JobIdError:
        return envelope
    released = release_waiting_job(awaited_id)
    job = load_job_plan(released) if released else None
    if job is None or job.metadata.get(JOB_UNATTENDED_KEY) is not True:
        return envelope
    try:
        record = start_run(released, released_run_options(load_job_plan(awaited_id)))
    except RunRefused as exc:
        return {**envelope, "released": None, "release_refused": {"error": exc.token, "message": str(exc)}}
    except OSError:
        return {**envelope, "released": None, "release_refused": {
            "error": "api_command_failed", "message": f"job {released} could not be started; nothing runs"}}
    return {**envelope, "released": run_record_payload(serve_paths(), record)}


#: F323: the awaited job's role choices a released job starts with, as `ExecutionConfig` field and
#: `remedy job run` flag: the four `do_context._job_run_role_flags` names on a waiting job's Next line.
RELEASED_RUN_ROLE_FLAGS: tuple[tuple[str, str], ...] = (
    ("builder", "--builder-provider"), ("reviewer", "--reviewer-provider"),
    ("builder_model", "--builder-model"), ("reviewer_model", "--reviewer-model"))


def released_run_options(awaited: Any) -> tuple[str, ...]:
    """F323: the `job run` flags of a released job: each role choice the job it waited for (AWAITED)
    ran with that was named, not a default, so the rest of an order runs with its order's roles."""
    ec = getattr(awaited, "execution_config", None)
    named = {field: str(getattr(ec, field, None) or "") for field, _flag in RELEASED_RUN_ROLE_FLAGS
             if getattr(ec, f"{field}_source", "default") not in ("default", "roles")}
    return tuple(f"{flag}={named[field]}" for field, flag in RELEASED_RUN_ROLE_FLAGS if named.get(field))


def awaited_job_end(job: Any) -> str:
    """F323: how *job* ended without a result that will land, in one word, or "" while it still may.

    `blocked`, `stopped`, `failed` and `cancelled` by its state, `declined` by its result's
    decline; "" for a job that is planned, running, finished awaiting its apply, or applied.
    """
    from packages.orchestration.job_apply import job_result_decline

    state = getattr(getattr(job, "state", None), "value", "")
    if state in ("blocked", "stopped", "failed", "cancelled"):
        return state
    return "declined" if state == "completed" and job_result_decline(job) is not None else ""


def _waiting_job(job_id: str, awaited: str) -> Any:
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id) if job_id else None
    if job is None or str(job.metadata.get(ORDER_JOB_WAITS_KEY) or "") != awaited:
        return None
    return job


def settle_waiting_jobs(job_id: str) -> list[str]:
    """F323: end `blocked` every job waiting for *job_id* once it ended without a result that lands.

    The waiting job's stop reason reads `awaited_job_ended:<job>` and its `stop_text` says which
    job it waited for, how that one ended and why, and what the person may do. A job waiting for
    the job just blocked is settled too, down the order's chain. Returns the jobs it blocked.
    """
    from datetime import datetime, timezone

    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    awaited = load_job_plan(job_id)
    ended = awaited_job_end(awaited) if awaited is not None else ""
    waiting = _waiting_job(str(awaited.metadata.get(ORDER_JOB_RELEASES_KEY) or "") if awaited else "", job_id)
    if (awaited is None or not ended or waiting is None
            or getattr(waiting.state, "value", "") not in ("planned", "pending")):
        return []
    from packages.orchestration.job_stop_text import JOB_STOP_TEXT_KEY, job_stop_text

    # F325: a job that recorded neither its own sentence nor a reason still says why it stopped.
    why = str(awaited.metadata.get(JOB_STOP_TEXT_KEY) or "") or awaited.stop_reason or job_stop_text(awaited)
    waiting.state = RunState.BLOCKED
    waiting.stop_reason = f"{ORDER_JOB_AWAITED_ENDED}:{job_id}"
    waiting.metadata[JOB_STOP_TEXT_KEY] = ORDER_JOB_AWAITED_ENDED_TEXT.format(
        job=job_id, ended=ended, why=f" ({why.rstrip('.')})" if why else "", me=waiting.job_id)
    waiting.stopped_at = datetime.now(timezone.utc).isoformat()
    save_job_plan(waiting)
    return [str(waiting.job_id), *settle_waiting_jobs(str(waiting.job_id))]


def release_waiting_job(job_id: str) -> str:
    """F323: the job that waited for *job_id*, ready to run now that its result was applied, or "".

    A waiting job blocked by `settle_waiting_jobs` (the awaited job was stopped or blocked and
    later finished and landed after all) is planned again, its stop cleared. The caller starts it.
    """
    from packages.core.models import RunState
    from packages.orchestration.job_apply import job_apply_landed
    from packages.orchestration.job_stop_text import JOB_STOP_TEXT_KEY
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    awaited = load_job_plan(job_id)
    if awaited is None or not job_apply_landed(job_id):
        return ""
    waiting = _waiting_job(str(awaited.metadata.get(ORDER_JOB_RELEASES_KEY) or ""), job_id)
    if waiting is None:
        return ""
    state = getattr(waiting.state, "value", "")
    if state == "blocked" and waiting.stop_reason == f"{ORDER_JOB_AWAITED_ENDED}:{job_id}":
        waiting.state = RunState.PLANNED
        waiting.stop_reason = waiting.stopped_at = ""
        waiting.metadata.pop(JOB_STOP_TEXT_KEY, None)
        save_job_plan(waiting)
        state = "planned"
    return str(waiting.job_id) if state in ("planned", "pending") else ""


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

    missions = job_mission_ids(job_ids)
    view: list[dict[str, Any]] = []
    for job_id in job_ids:
        job = load_job_plan(job_id)
        entry = _missing(job_id) if job is None else _job_entry(job)
        view.append({**entry, "mission_id": missions.get(job_id)})
    return view


def job_mission_ids(job_ids: list[str]) -> dict[str, str]:
    """The mission each of *job_ids* is linked to, read in one pass over the missions' chains."""
    from packages.orchestration.mission_state import list_missions, project_ids_with_missions

    wanted, found = set(job_ids), {}
    for project_id in project_ids_with_missions() if wanted else []:
        for mission in list_missions(project_id):
            found.update({link.job_id: str(mission.id) for link in mission.job_links if link.job_id in wanted})
    return found


#: How many characters of a batch's id name its order over HTTP: the length of the id
#: `POST /api/v1/orders` answers, so `POST /api/v1/orders/{order}/cancel` takes it (amend1027b A3).
ORDER_ID_LENGTH = 16


# WHY: a job made on the command line had only its batch's 32-character id, which no order route
# takes, so an app could not cancel its order (amend1027b A3; F036 of the edition, review 1).
def http_order_id_of_batch(batch_id: str, source_path: str, job_id: str) -> str:
    """The 16-character order id of the batch BATCH_ID that JOB_ID belongs to.

    An order the supervisor started has its own id: the folder of its order file under `orders/`,
    or, for an order sent with a key (its file under `order-keys/`), the newest order record that
    lists JOB_ID. Every other batch is named by the first `ORDER_ID_LENGTH` characters of its id,
    which the order routes resolve back to it (`serve_runs.resolve_order_record`).
    """
    from packages.orchestration.serve_paths import ORDER_KEYS_NAME, serve_paths
    from packages.orchestration.serve_runs import order_record_for_job

    paths = serve_paths()
    source = Path(source_path) if source_path else None
    if source is not None and source.parent.parent.resolve() == paths.orders_dir.resolve():
        return source.parent.name
    if source is not None and source.parent.resolve() == (paths.root / ORDER_KEYS_NAME).resolve():
        record = order_record_for_job(paths, job_id)
        if record is not None:
            return record.order_id
    return batch_id[:ORDER_ID_LENGTH]


def order_id_of_job(job: Any) -> str | None:
    """The order JOB serves (operator amendment amend1027-green-builds E1), or None.

    The batch its mission links it under, named by `http_order_id_of_batch`: the id of the HTTP
    order the supervisor started, or the batch's 16-character id for a job made elsewhere, which
    the order routes take as well (amend1027b A3).
    """
    from packages.orchestration.mission_state import list_missions, project_ids_with_missions

    job_id, project = str(job.job_id), str(getattr(job, "project_id", "") or "")
    for project_id in [project] if project else project_ids_with_missions():
        for mission in list_missions(project_id):
            batch_id = next((link.order_id for link in mission.job_links if link.job_id == job_id), None)
            if not batch_id:
                continue
            batch = next((b for b in mission.orders if b.order_id == batch_id), None)
            return http_order_id_of_batch(batch_id, batch.source_path if batch is not None else "", job_id)
    return None


def order_batch_by_http_id(order_id: str) -> tuple[Any, list[str], list[str]] | None:
    """The mission batch whose id begins with the 16-character ORDER_ID, with the ids of its jobs
    and of the projects that hold it, or None (amend1027b A3)."""
    from packages.orchestration.mission_state import list_missions, project_ids_with_missions

    if len(order_id) != ORDER_ID_LENGTH:
        return None
    found, job_ids, project_ids = None, [], []
    for project_id in project_ids_with_missions():
        for mission in list_missions(project_id):
            batch = next((b for b in mission.orders if b.order_id[:ORDER_ID_LENGTH] == order_id), None)
            if batch is None:
                continue
            found = found or batch
            job_ids += [link.job_id for link in mission.job_links if link.order_id == batch.order_id]
            project_ids.append(str(project_id))
    return (found, list(dict.fromkeys(job_ids)), project_ids) if found is not None else None


def _missing(job_id: str) -> dict[str, Any]:
    return {"job_id": job_id, "title": "", "state": "missing", "phase": "failed", "executable": False,
            "tasks": {"total": 0, "done": 0, "current": ""}, "waits_for": None, "waiting_reason": "",
            "verification": None, "story": f"/api/v1/jobs/{job_id}/story", "blocking_criterion": None}


def job_blocking_criterion(job: Any) -> str | None:
    """The criterion a blocked or failed job did not meet: the acceptance of its first task that ended
    blocked or failed, in the planner's own words, or None (DECISION amend1023 D11)."""
    from packages.orchestration.pingpong_job import TASK_BLOCKED, TASK_FAILED

    task = next((task for task in job.tasks if task.status in (TASK_BLOCKED, TASK_FAILED)), None)
    return (str(task.acceptance).strip() or None) if task is not None else None


def _wait_reason(waits_for: str) -> str:
    """Why a job waits for *waits_for*: its apply, or nothing any more when that job ended without one."""
    from packages.orchestration.pingpong_job import load_job_plan

    before = load_job_plan(waits_for)
    ended = awaited_job_end(before) if before is not None else ""     # F323: blocked and stopped too
    return (ORDER_JOB_ORPHANED_REASON.format(job=waits_for, ended=ended) if ended
            else ORDER_JOB_WAIT_REASON.format(job=waits_for))


def _job_entry(job: Any) -> dict[str, Any]:
    from packages.orchestration.job_apply import job_apply_landed, job_result_decline
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.job_stop_text import job_stop_text
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
        # rel-1019 (R-1366): a rejected plan never runs; nothing is left to approve.
        blocked_by = task_plan_blocks_execution(job)
        phase = "declined" if blocked_by == "rejected" else "needs_plan_approval" if blocked_by else "ready"
    elif state == "completed" and not job.tasks:
        phase = "checked"
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
        "blocking_criterion": job_blocking_criterion(job) if phase in ("blocked", "failed") else None,
        # F325: why a blocked, stopped, cancelled or failed job stopped, the story's `stop.text`.
        "stop_text": job_stop_text(job) if phase in ("blocked", "failed", "stopped", "cancelled") else "",
    }
