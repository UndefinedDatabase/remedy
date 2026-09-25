"""`remedy job pause` / `remedy job unpause` — F025 T002, DECISION F025 D2.

A pause is never a waiting process (`packages/orchestration/pause_control.py`'s
own docstring): this command writes a durable control entry, or reads one back
off disk, and returns. `job.pause` without `--task` requests a whole-job pause;
with one, it pauses that single task. `job.unpause` is the reverse: with a task
it releases that task, and without one it either withdraws a pending job-scope
pause no safe point has served yet, or — for a job an operator pause has already
parked and saved to disk — answers with the command that relaunches it, because
this door starts no process of its own (operator question Q4).

Modelled on `job_stop_cmd.py`: the same job id resolution, the same usage and
unknown-job exits (2 and 3), and the same JSON envelope with `schema_version` 1.
Both commands share `pause_control.pause_job_command` and `unpause_job_command`
with the write door (`packages/orchestration/ui_server.py`), so the CLI and the
browser answer identically for the same request.
"""
from __future__ import annotations

from apps.cli.json_envelope import emit_ok, fail

EXIT_ERROR = 1
EXIT_USAGE = 2
#: The contract's exit code for a job that does not exist.
EXIT_UNKNOWN_JOB = 3


def _load_job(job_id: str):
    from packages.orchestration.pingpong_job import load_job_plan

    return load_job_plan(job_id)


def _resolve_job_id(job_id: str, *, json_output: bool) -> str:
    """Validate the shape, then resolve a prefix or fail unknown — exactly the
    two steps `job_stop_cmd._cmd_job_stop` runs before it ever touches the job."""
    from packages.orchestration.safe_points import StopControlError, validate_job_id

    job_id = (job_id or "").strip()
    try:
        validate_job_id(job_id)
    except StopControlError as exc:
        fail("invalid_job_id", str(exc), json_output=json_output, exit_code=EXIT_USAGE)

    if _load_job(job_id) is None:
        from apps.cli.job_id_arg import refuse_ambiguous_job_id
        from packages.orchestration.data_paths import JobIdAmbiguous, JobIdError, lookup_job_id

        try:
            job_id = lookup_job_id(job_id)
        except JobIdAmbiguous as exc:
            refuse_ambiguous_job_id(job_id, exc.matches, json_output=json_output)
        except JobIdError:
            fail(
                "job_not_found",
                f"No job matches {job_id!r}. Try: remedy job list.",
                json_output=json_output,
                exit_code=EXIT_UNKNOWN_JOB,
                job_id=job_id,
            )
    return job_id


def _unknown_job(job_id: str, *, json_output: bool) -> None:
    fail(
        "job_not_found",
        f"No job matches {job_id!r}. Try: remedy job list.",
        json_output=json_output,
        exit_code=EXIT_UNKNOWN_JOB,
        job_id=job_id,
    )


def _cmd_job_pause(job_id: str, *, task: str = "", reason: str = "", source: str = "cli",
                   json_output: bool = False) -> None:
    from packages.orchestration.pause_control import pause_job_command

    job_id = _resolve_job_id(job_id, json_output=json_output)
    job = _load_job(job_id)
    if job is None:
        _unknown_job(job_id, json_output=json_output)

    task_id = task.strip() or None
    result = pause_job_command(job, task_id=task_id, reason=reason,
                               source=source or "cli")

    if result["outcome"] == "refused":
        detail = result["reason"]
        subject = f"task {task_id!r}" if task_id else f"job {job_id}"
        fail("job_not_pausable", f"{subject} was not paused — {detail}",
             json_output=json_output, job_id=job_id,
             **{k: v for k, v in result.items() if k != "outcome"})
        return

    if json_output:
        emit_ok(job_id=job_id, **result)
        return

    if task_id:
        print("Task pause requested — it will take effect at the next safe point.")
        print(f"  job: {job_id} · task: {task_id} · request: {result['request_id']}")
    else:
        print("Pause requested — it will take effect at the next safe point.")
        print(f"  job: {job_id} · request: {result['request_id']}")


def _cmd_job_unpause(job_id: str, *, task: str = "", source: str = "cli",
                     json_output: bool = False) -> None:
    from packages.orchestration.pause_control import unpause_job_command

    job_id = _resolve_job_id(job_id, json_output=json_output)
    job = _load_job(job_id)
    if job is None:
        _unknown_job(job_id, json_output=json_output)

    task_id = task.strip() or None
    result = unpause_job_command(job, task_id=task_id, source=source or "cli")

    if result["outcome"] == "refused":
        detail = result["reason"]
        subject = f"task {task_id!r}" if task_id else f"job {job_id}"
        fail("job_not_unpausable", f"{subject} was not unpaused — {detail}",
             json_output=json_output, job_id=job_id,
             **{k: v for k, v in result.items() if k != "outcome"})
        return

    if json_output:
        emit_ok(job_id=job_id, **result)
        return

    outcome = result["outcome"]
    if outcome == "parked":
        print(f"Job {job_id} is paused and saved.")
        print(f"  continue it with: {result['next']}")
    elif outcome == "released":
        print(f"Task {task_id} resumed.")
        print(f"  job: {job_id} · request: {result['request_id']}")
    elif outcome == "withdrawn":
        print("Pause request withdrawn — the job keeps running.")
        print(f"  job: {job_id} · request: {result['request_id']}")
    else:
        subject = f"Task {task_id}" if task_id else f"Job {job_id}"
        print(f"{subject} was not paused — nothing to do.")


COMMAND_HANDLERS = {
    "job.pause": lambda args: _cmd_job_pause(
        getattr(args, "job_id", "") or "",
        task=getattr(args, "task", "") or "",
        reason=getattr(args, "reason", "") or "",
        source=getattr(args, "source", "") or "cli",
        json_output=bool(getattr(args, "json", False)),
    ),
    "job.unpause": lambda args: _cmd_job_unpause(
        getattr(args, "job_id", "") or "",
        task=getattr(args, "task", "") or "",
        source=getattr(args, "source", "") or "cli",
        json_output=bool(getattr(args, "json", False)),
    ),
}
