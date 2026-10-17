"""`remedy job abandon` and `remedy client cancel-order`: work the person no longer wants ends for good.

`remedy job stop` pauses a job so that `remedy job run` can resume it. A cancel is the other ending:
the job is `cancelled`, never runs again and leaves the active views, while its record and evidence
stay readable (`packages/orchestration/job_cancel.py`). `remedy client cancel-order` cancels an
order the supervisor started, whatever it is doing: planning, running or waiting
(`packages/orchestration/order_cancel.py`). Both are idempotent, and both are twinned over HTTP by
`POST /api/v1/jobs/{job}/abandon` and `POST /api/v1/orders/{order}/cancel`.

Neither forwards to the supervisor: each writes its request durably and directly, and a running
job or walk reads it at its next safe point, as it reads a stop.
"""
from __future__ import annotations

from typing import Any

from apps.cli.json_envelope import emit_ok, fail
from packages.orchestration.order_cancel import ORDER_CANCEL_ANSWER_KEYS, ORDER_CANCEL_ANSWER_TREE

#: The refusal tokens and answer keys of `remedy job abandon`, as the machine client interface declares them.
JOB_CANCEL_REFUSAL_TOKENS = ("ambiguous_job_id", "cancel_not_requested", "invalid_job_id",
                             "job_not_cancellable", "job_not_found")
JOB_CANCEL_ANSWER_KEYS = ("already_cancelled", "cancel", "cancel_pending", "job_id", "job_status", "matches")
JOB_CANCEL_ANSWER_TREE: dict[str, Any] = {"cancel": {key: {} for key in ("job_id", "reason", "source",
                                                                        "requested_at")}}
#: The refusal tokens of `remedy client cancel-order`.
ORDER_CANCEL_REFUSAL_TOKENS = ("cancel_not_requested", "order_not_found")

#: Both operations' tokens, answer keys and answer trees, as `apps/cli/client_interface.py` lists them.
CANCEL_REFUSAL_TOKENS = {"job.abandon": JOB_CANCEL_REFUSAL_TOKENS, "client.cancel-order": ORDER_CANCEL_REFUSAL_TOKENS}
CANCEL_ANSWER_KEYS = {"job.abandon": JOB_CANCEL_ANSWER_KEYS, "client.cancel-order": ORDER_CANCEL_ANSWER_KEYS}
CANCEL_ANSWER_TREES = {"job.abandon": JOB_CANCEL_ANSWER_TREE, "client.cancel-order": ORDER_CANCEL_ANSWER_TREE}


def _job_runner_alive(job_id: str) -> bool:
    """False only when the supervisor's own run of *job_id* is known to have ended or been lost."""
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import read_run_record, run_state

    paths = serve_paths()
    run = read_run_record(paths, job_id)
    return run is None or run_state(paths, run) == "running"


def _cmd_job_cancel(job_id: str, *, reason: str = "", source: str = "cli", json_output: bool = False) -> None:
    from apps.cli.job_id_arg import refuse_ambiguous_job_id
    from packages.orchestration.data_paths import JobIdAmbiguous, JobIdError, lookup_job_id
    from packages.orchestration.job_cancel import JobCancelRefused, cancel_job
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.safe_points import StopControlError, validate_job_id

    job_id = (job_id or "").strip()
    try:
        validate_job_id(job_id)
    except StopControlError as exc:
        fail("invalid_job_id", str(exc), json_output=json_output, exit_code=2)
    if load_job_plan(job_id) is None:
        try:
            job_id = lookup_job_id(job_id)
        except JobIdAmbiguous as exc:
            refuse_ambiguous_job_id(job_id, exc.matches, json_output=json_output)
        except JobIdError:
            pass
    job = load_job_plan(job_id)
    if job is None:
        fail("job_not_found", f"No job matches {job_id!r}. Try: remedy job list.",
             json_output=json_output, exit_code=3, job_id=job_id)
    try:
        answer = cancel_job(job, reason=reason, source=source or "cli",
                            runner_alive=_job_runner_alive(job_id))
    except JobCancelRefused as refusal:
        fail(refusal.token, str(refusal), json_output=json_output, job_id=job_id,
             job_status=getattr(job.state, "value", str(job.state)))
    except StopControlError as exc:
        # An unwritable control area is never a silent no-op: nothing asked this job to end.
        fail("cancel_not_requested", f"no cancel was requested — {exc}", json_output=json_output,
             job_id=job_id)
    if json_output:
        emit_ok(**answer)
        return
    if answer["already_cancelled"]:
        print(f"Job {job_id} was cancelled already — nothing changed.")
    elif answer["cancel_pending"]:
        print(f"Cancel requested — job {job_id} is running; it ends cancelled at its next safe point.")
    else:
        print(f"Cancelled — job {job_id} never runs again; its record and evidence stay.")


def _cmd_order_cancel(order_id: str, *, reason: str = "", source: str = "cli",
                      decline_results: bool = False, json_output: bool = False) -> None:
    from packages.orchestration.order_cancel import OrderCancelError, cancel_order
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_not_found_message, read_order_record

    paths = serve_paths()
    record = read_order_record(paths, (order_id or "").strip())
    if record is None:
        fail("order_not_found", order_not_found_message(order_id), json_output=json_output, exit_code=3)
    try:
        answer = cancel_order(paths, record, reason=reason, source=source or "cli",
                              decline_results=decline_results)
    except OrderCancelError as exc:
        fail("cancel_not_requested", f"no cancel was requested — {exc}", json_output=json_output,
             order_id=record.order_id)
    if json_output:
        emit_ok(**answer)
        return
    print(f"Order {record.order_id}: {answer['phase']}"
          + (" (it was cancelled already)" if answer["already_cancelled"] else ""))
    for entry in answer["jobs"]:
        print(f"  job {entry['job_id']}: {entry['before']} -> {entry['job_status']} ({entry['outcome']})")


COMMAND_HANDLERS = {
    "job.abandon": lambda args: _cmd_job_cancel(
        getattr(args, "job_id", "") or "",
        reason=getattr(args, "reason", "") or "",
        source=getattr(args, "source", "") or "cli",
        json_output=bool(getattr(args, "json", False)),
    ),
    "client.cancel-order": lambda args: _cmd_order_cancel(
        getattr(args, "order", "") or "",
        reason=getattr(args, "reason", "") or "",
        source=getattr(args, "source", "") or "cli",
        decline_results=bool(getattr(args, "decline_results", False)),
        json_output=bool(getattr(args, "json", False)),
    ),
}
