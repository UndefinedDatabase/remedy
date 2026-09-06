"""`remedy job stop` — the F011 kill switch, from a second terminal.

This command does not kill anything. It writes one durable control file and returns; the
runner picks it up at its next safe point, lets the provider call in flight finish, starts
nothing new, and persists a resumable STOPPED job. That is the whole point: an operator
should be able to stop a job without wondering what was half-written when they did.

`--status` answers the only other question worth asking: is a stop pending, was one already
consumed, and is this job actually stopped?
"""
from __future__ import annotations

import json as _json
import sys

EXIT_ERROR = 1
EXIT_USAGE = 2
#: The contract's exit code for a job that does not exist.
EXIT_UNKNOWN_JOB = 3

#: A job that will never run again cannot be stopped, and saying "stop requested" would be
#: a lie the operator has no way to catch.
_FINISHED_STATES = frozenset({"completed"})


class _CoreJobAdapter:
    """Adapt a Core Job (storage.load_job) to the interface _cmd_job_stop expects."""

    __slots__ = ("status", "stop_request_id", "stop_reason", "stop_source", "stopped_at")

    def __init__(self, core_job):
        self.status = core_job.state.value
        self.stop_request_id = ""
        self.stop_reason = ""
        self.stop_source = ""
        self.stopped_at = ""



def _load_job(job_id: str):
    from packages.orchestration.pingpong_job import load_job_plan

    plan = load_job_plan(job_id)
    if plan is not None:
        return plan

    try:
        from uuid import UUID

        from packages.orchestration.storage import load_job

        core = load_job(UUID(job_id))
        return _CoreJobAdapter(core)
    except Exception:
        return None


def _print_status(job_id: str, *, json_output: bool) -> None:
    from packages.orchestration.safe_points import stop_status

    job = _load_job(job_id)
    if job is None:
        _unknown_job(job_id, json_output=json_output)

    status = stop_status(job_id)
    payload = status.to_json()
    payload["job_status"] = job.status
    payload["stopped"] = job.status == "stopped"

    if json_output:
        print(_json.dumps(payload, indent=2))
        return

    print(f"Job {job_id} — state: {job.status}")
    if status.pending is not None:
        p = status.pending
        print(f"Stop request PENDING — {p.request_id} · reason: {p.reason} "
              f"· source: {p.source} · requested: {p.requested_at or 'unknown'}")
    else:
        print("Stop request: none pending")
    if status.archived:
        print(f"Consumed stop requests: {status.consumed_count}")
        for s in status.archived:
            print(f"  {s.request_id} · reason: {s.reason} · source: {s.source} "
                  f"· requested: {s.requested_at or 'unknown'}")
    else:
        print("Consumed stop requests: none")


def _unknown_job(job_id: str, *, json_output: bool) -> None:
    if json_output:
        print(_json.dumps({"ok": False, "error": "job_not_found", "job_id": job_id},
                          indent=2))
    else:
        print(f"Error: job not found: {job_id}", file=sys.stderr)
    raise SystemExit(EXIT_UNKNOWN_JOB)


def _cmd_job_stop(job_id: str, *, reason: str = "", source: str = "cli",
                  status: bool = False, json_output: bool = False) -> None:
    from packages.orchestration.safe_points import StopControlError, request_stop

    job_id = (job_id or "").strip()

    try:
        from packages.orchestration.safe_points import validate_job_id

        validate_job_id(job_id)
    except StopControlError as exc:
        if json_output:
            print(_json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE) from None

    if _load_job(job_id) is None:
        from packages.orchestration.data_paths import resolve_job_id
        try:
            job_id = resolve_job_id(job_id)
        except SystemExit as exc:
            if exc.code == 2:
                raise
            _unknown_job(job_id, json_output=json_output)

    if status:
        _print_status(job_id, json_output=json_output)
        return

    job = _load_job(job_id)
    if job is None:
        _unknown_job(job_id, json_output=json_output)

    if job.status == "stopped":
        # The reviewed build happily wrote a NEW request here — a trap: the operator's next
        # resume would stop again immediately, for a stop that had already happened. A stop
        # request for a job that is already stopped is the same stop, and it is idempotent.
        from packages.orchestration.safe_points import stop_requested

        pending = stop_requested(job_id)
        if pending is None:
            if json_output:
                print(_json.dumps({
                    "ok": True, "already_stopped": True, "job_id": job_id,
                    "job_status": job.status,
                    "stop": {
                        "request_id": job.stop_request_id,
                        "reason": job.stop_reason,
                        "source": job.stop_source,
                        "stopped_at": job.stopped_at,
                    },
                }, indent=2))
            else:
                print(f"Job {job_id} is already stopped — no new stop was requested.")
                print(f"  last stop: {job.stop_request_id or 'unknown'} · reason: "
                      f"{job.stop_reason or 'unknown'} · at: {job.stopped_at or 'unknown'}")
            return
        # A pending request on a stopped job is an unfinished finalization, not a new
        # episode: report it as it is.

    if job.status in _FINISHED_STATES:
        # No safe point will ever arrive. Pretending otherwise would leave an operator
        # waiting for a stop that cannot happen.
        message = (f"job {job_id} is already {job.status}; there is no work left to stop "
                   f"and no stop was requested")
        if json_output:
            print(_json.dumps({"ok": False, "error": "job_not_stoppable",
                               "job_id": job_id, "job_status": job.status}, indent=2))
        else:
            print(f"Error: {message}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR)

    try:
        signal = request_stop(job_id, reason=reason, source=source or "cli")
    except StopControlError as exc:
        # An unwritable control area is never a silent no-op: the operator must know that
        # NOTHING asked this job to stop.
        if json_output:
            print(_json.dumps({"ok": False, "error": "stop_not_requested",
                               "detail": str(exc), "job_id": job_id}, indent=2))
        else:
            print(f"Error: no stop was requested — {exc}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR) from None

    if json_output:
        print(_json.dumps({"ok": True, "job_id": job_id, "job_status": job.status,
                           "stop": signal.to_json()}, indent=2))
    else:
        print("Stop requested — it will take effect at the next safe point.")
        print(f"  job: {job_id} · request: {signal.request_id} · reason: {signal.reason}")


COMMAND_HANDLERS = {
    "job.stop": lambda args: _cmd_job_stop(
        getattr(args, "job_id", "") or "",
        reason=getattr(args, "reason", "") or "",
        source=getattr(args, "source", "") or "cli",
        status=bool(getattr(args, "status", False)),
        json_output=bool(getattr(args, "json", False)),
    ),
}
