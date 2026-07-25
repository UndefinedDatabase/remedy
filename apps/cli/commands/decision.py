"""Decision group command handlers (human decision queue)."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from packages.orchestration.data_paths import resolve_job_id

if TYPE_CHECKING:
    import argparse


def _load_job_events(job_id_str: str):
    """Load job and events. Returns (job, events, job_id_str)."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import JobNotFoundError, load_job
    from packages.orchestration.timeline import load_run_events

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    return job, events, job_id_str


def _cmd_decision_list(job_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.decision_queue import export_decision_json, list_decisions

    job, events, jid = _load_job_events(job_id_str)
    decisions = list_decisions(job, events)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": jid,
            "decisions": [export_decision_json(d) for d in decisions],
        }, sort_keys=True))
    else:
        if not decisions:
            print(f"No pending decisions for job {jid[:8]}.")
            return
        for d in decisions:
            status_mark = "[open]" if d.status == "open" else "[resolved]"
            print(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}  (id={d.id})")


def _cmd_decision_show(job_id_str: str, decision_id: str, *, json_output: bool = False) -> None:
    from packages.orchestration.decision_queue import export_decision_json, get_decision

    job, events, jid = _load_job_events(job_id_str)
    d = get_decision(job, events, decision_id)

    if d is None:
        print(f"Error: decision not found: {decision_id}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": jid,
            "decision": export_decision_json(d),
        }, sort_keys=True))
    else:
        print(f"Decision: {d.id}")
        print(f"  Type: {d.type}")
        print(f"  Status: {d.status}")
        print(f"  Severity: {d.severity}")
        print(f"  Summary: {d.safe_summary}")
        if d.next_actions:
            print("  Next actions:")
            for a in d.next_actions:
                print(f"    - {a}")


def _cmd_decision_resolve(job_id_str: str, decision_id: str, *, reason: str | None = None) -> None:
    # Decisions are derived — resolve the underlying record if possible
    if decision_id.startswith("sr:"):
        from packages.orchestration.stop_reasons import resolve_stop_reason
        stop_id = decision_id[3:]
        sr = resolve_stop_reason(job_id_str, stop_id, reason or "manually resolved")
        if sr is None:
            print(f"Error: stop reason not found: {stop_id}", file=sys.stderr)
            sys.exit(1)
        print(f"Resolved stop reason: {sr.id[:8]} ({sr.reason_code})")
    elif decision_id.startswith("fp:"):
        from packages.orchestration.data_paths import resolve_job_id as _rji
        from packages.orchestration.storage import JobNotFoundError, load_job, save_job

        job_id = _rji(job_id_str)
        try:
            job = load_job(job_id)
        except JobNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        fp = getattr(job, "flight_plan", None)
        if not isinstance(fp, dict) or fp.get("_approval") != "pending":
            print("Error: no pending flight plan approval for this job.", file=sys.stderr)
            sys.exit(1)

        if reason not in ("approve", "reject"):
            print(
                "Error: --reason must be 'approve' or 'reject'.\n"
                f"  remedy decision resolve {job_id_str} fp:approval --reason approve\n"
                f"  remedy decision resolve {job_id_str} fp:approval --reason reject",
                file=sys.stderr,
            )
            sys.exit(1)

        if reason == "approve":
            fp["_approval"] = "approved"
            job.flight_plan = fp
            save_job(job)
            print(f"Flight plan approved for job {job_id_str}.")
        else:
            fp["_approval"] = "rejected"
            job.flight_plan = fp
            save_job(job)
            print(f"Flight plan rejected for job {job_id_str}.")
            print(f"Run: remedy do replan {job_id_str}")
    else:
        print(f"Decision '{decision_id}' is derived and cannot be directly resolved.", file=sys.stderr)
        print("Resolve the underlying record (patch intent, test, etc.) instead.", file=sys.stderr)
        sys.exit(1)


def _cmd_decision_explain(job_id_str: str) -> None:
    from packages.orchestration.decision_queue import explain_decisions

    job, events, _jid = _load_job_events(job_id_str)
    print(explain_decisions(job, events))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "decision.list": lambda args: _cmd_decision_list(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "decision.show": lambda args: _cmd_decision_show(
        args.job_id,
        args.decision_id,
        json_output=getattr(args, "json", False),
    ),
    "decision.resolve": lambda args: _cmd_decision_resolve(
        args.job_id,
        args.decision_id,
        reason=getattr(args, "reason", None),
    ),
    "decision.explain": lambda args: _cmd_decision_explain(args.job_id),
}
