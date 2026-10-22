"""One stop, one question: what a budget stop puts in front of the operator (F310, DECISION F310 D5).

A job that a budget stopped raises ONE decision, and this module answers the three things that decision
needs beside its two options: the mission's open blocking criteria it names (`budget_stop_blockers`),
the limits an `extend` without an answer doubles (`doubled_limit_answers`), and the run that starts
at once when the public API's twin command answers `extended` (`resume_after_budget_extend`). Every
import of a sibling module sits inside the function that needs it, so no import cycle can form.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

#: The four ceilings an `extend` without an answer may double, in the order the answer lists them.
_DOUBLED_LIMITS = ("max_total_tokens", "max_provider_calls", "max_wall_clock_minutes", "max_cost_usd")


# WHY: the budget decision names the mission's open blockers, so one question carries the whole stop.
def budget_stop_blockers(job: Any) -> list[str]:
    """The `<id>: <text>` of each blocking criterion of the job's mission contract, or `[]`."""
    from packages.orchestration.mission_contract import (
        ContractError,
        contract_blocking_criteria,
        read_mission_contract,
    )
    from packages.orchestration.mission_state import mission_for_job

    mission = mission_for_job(str(getattr(job, "job_id", "")))
    if mission is None:
        return []
    try:
        criteria = contract_blocking_criteria(read_mission_contract(mission))
    except ContractError:
        return []
    return [f"{criterion.id}: {criterion.text}" for criterion in criteria]


# WHY: the walk names a budget stop's one question and its answering command, and raises no second decision.
def budget_stop_walk_note(ctx: Any, job: Any) -> str:
    """The detail's tail for a job its budget stopped, or "" (DECISION F310 D6); the Next line joins ``ctx``."""
    from packages.orchestration.decision_queue import open_budget_decision_id

    if str(getattr(job, "stop_source", "") or "") != "budget":
        return ""
    decision_id = open_budget_decision_id(job)
    if not decision_id:
        return ""
    ctx.next_lines.append(f"remedy decision resolve {job.job_id} {decision_id} --reason extend")
    note = (f"; its budget stopped it: budget decision {decision_id} is its one open question, "
            "answered extend or abandon")
    if budget_stop_blockers(job):
        note += ", and it names the mission's open blocking criteria"
    return note


# WHY: the mission's remainder decision waits until the budget stop is final, which is the `abandon` answer.
def raise_remainder_for_final_job(job: Any) -> str | None:
    """The id of the remainder decision raised for a cancelled job's mission, or None (DECISION F310 D6)."""
    from packages.orchestration.mission_contract import ContractError, raise_contract_remainder_decision
    from packages.orchestration.mission_state import mission_for_job

    if getattr(job, "state", None) != "cancelled":
        return None
    mission = mission_for_job(str(getattr(job, "job_id", "")))
    if mission is None:
        return None
    try:
        return raise_contract_remainder_decision(str(mission.project_id), str(mission.id))
    except ContractError:
        return None


# WHY public: the budget stop and the insight (DECISION F311 D1) measure worked time alike.
def budget_work_seconds(actuals: dict[str, Any], now: datetime, *, in_flight: bool = False) -> float:
    """The seconds of work a decoded record holds: the moment it was last active, less the start and the waiting.

    A job in flight is active now, so it is measured to `now`; one that does not run was last active
    at `active_until` (R-1423).
    """
    until = now if in_flight else (actuals["active_until"] or now)
    return (until - actuals["started_at"]).total_seconds() - actuals["waited_s"]


def _exhausted_limits(job: Any, limits: Any, now: datetime) -> set[str]:
    """The limit the stop reason names, and each of the four that the job's saved actuals had reached."""
    from packages.orchestration.budget_guard import BudgetCounterError, decode_persisted_budget_actuals

    stop_reason = str(getattr(job, "stop_reason", "") or "")
    exhausted = {stop_reason.rsplit(":", 1)[-1]} if ":" in stop_reason else set()
    record = getattr(job, "budget_actuals", None)
    if not isinstance(record, dict) or not record:
        return exhausted
    try:
        actuals = decode_persisted_budget_actuals(
            record, first_running_at=getattr(job, "first_running_at", "") or None)
    except BudgetCounterError:
        return exhausted
    used = {
        "max_total_tokens": actuals["total_tokens"],
        "max_provider_calls": actuals["provider_call_count"],
        "max_wall_clock_minutes": budget_work_seconds(actuals, now),
        "max_cost_usd": actuals["measured_cost_usd"],
    }
    scale = {"max_wall_clock_minutes": 60}
    return exhausted | {
        name for name, spent in used.items()
        if spent is not None and getattr(limits, name) is not None
        and spent >= getattr(limits, name) * scale.get(name, 1)}


# WHY: `extend` without an answer raises every limit the stop exhausted to twice what the run read.
def doubled_limit_answers(job: Any, *, now: datetime | None = None) -> list[str]:
    """`<limit>=<doubled value>` for each exhausted limit of the four, or `[]` when none can be told."""
    from packages.orchestration.budget_profiles import effective_job_budgets

    try:
        limits = effective_job_budgets(job)
    except ValueError:
        return []
    if limits is None:
        return []
    exhausted = _exhausted_limits(job, limits, now or datetime.now(timezone.utc))
    answers = []
    for name in _DOUBLED_LIMITS:
        value = getattr(limits, name)
        if name in exhausted and value is not None:
            doubled = max(60, 2 * value) if name == "max_wall_clock_minutes" else 2 * value
            answers.append(f"{name}={doubled}")
    return answers


# WHY: over the public API an `extended` answer starts the job's run, as `POST /api/v1/jobs/{job}/run` would.
def resume_after_budget_extend(
    twin: str, segments: dict[str, str], envelope: dict[str, Any], start_run: Any,
) -> dict[str, Any]:
    """ENVELOPE, with the run it started under `resumed` or why it could not start under `resume_refused`."""
    if (twin != "decision.resolve" or not envelope.get("ok") or envelope.get("outcome") != "extended"
            or start_run is None):
        return envelope
    from packages.orchestration.data_paths import JobIdError, lookup_job_id
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import RunRefused, run_record_payload

    try:
        record = start_run(lookup_job_id(segments["job"]), ())
    except JobIdError as exc:
        refused = {"error": "job_not_found", "message": str(exc)}
    except RunRefused as exc:
        refused = {"error": exc.token, "message": str(exc)}
    except OSError:
        refused = {"error": "api_command_failed", "message": "the run could not be started; nothing runs"}
    else:
        return {**envelope, "resumed": run_record_payload(serve_paths(), record)}
    return {**envelope, "resumed": None, "resume_refused": refused}
