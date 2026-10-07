"""F295 R13 — DECISION F295 D12: a budget decision answered `extend` or `abandon`.

`remedy decision resolve <job> <decision> --reason extend --answer <limit>=<value>`
raises one or more of a job's budget limits and records the answer, so the
job's open budget decision and the resume guard of DECISION F295 D9 read the
stop as answered until the job stops again (D11 (4)). `remedy decision resolve
<job> <decision> --reason abandon` cancels the job instead: its state becomes
`cancelled`, the answer is recorded the same way, and D12 (3) makes a
cancelled job refuse to run again through `run_job`, `remedy job run` or
`remedy job resume`.

Public API::

    answer_budget_decision(job, decision_id, option, answers, *, now) -> dict
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from packages.core.models import JobBudgets, RunState
from packages.orchestration.budget_resolution import BudgetConfigError, parse_budget_limit
from packages.orchestration.decision_queue import budget_decision_id, budget_stop_answer

__all__ = ["answer_budget_decision"]

#: D11 (1): the five limits a budget decision may raise.
_LIMIT_NAMES = (
    "max_total_tokens", "max_provider_calls", "max_wall_clock_minutes",
    "max_cost_usd", "deadline",
)

#: D11 (2): the one limit that is never raised per job — it is a floor set in
#: configuration, not a per-job ceiling (`packages.core.models.JobBudgets`).
_UNRAISABLE_LIMIT = "min_free_disk_bytes"

#: The record's `actor`: this round lands the CLI route only (D11 (6) leaves the
#: cockpit's write door untouched), so nothing here receives an actor to carry.
_ACTOR = "cli"


def _refuse(code: str, detail: str) -> dict[str, Any]:
    return {"outcome": "refused", "code": code, "detail": detail}


def _stop_reason_limit(stop_reason: str) -> str:
    """The limit a stop reason names after its last colon (`budget_exhausted:deadline`,
    `predicted_budget_exhausted:max_cost_usd`), or "" when it names none."""
    if ":" not in stop_reason:
        return ""
    return stop_reason.rsplit(":", 1)[-1]


def answer_budget_decision(
    job: Any, decision_id: str, option: str, answers: list[str], *, now: datetime,
) -> dict[str, Any]:
    """D11 (2) to (4): answer one budget decision of `job`.

    Never raises for a refusal: checks in order the decision id, whether it is
    already answered, the option, that at least one answer was given, whether
    the stop is by the unraisable floor, that every answer parses, that the
    stop's own limit (if it names one) is among the answered limits, and that
    every answered limit actually raises the job's current value. Each refusal
    answers ``{"outcome": "refused", "code", "detail"}`` with `code` one of the
    D11 (2) tokens. On success it applies D11 (3)'s effect to `job` WITHOUT
    saving it and answers ``{"outcome": "extended", "raised", "budgets",
    "record"}``.
    """
    stop_source = str(getattr(job, "stop_source", "") or "")
    expected_id = budget_decision_id(str(getattr(job, "stop_request_id", "") or ""))
    if stop_source != "budget" or str(decision_id) != expected_id:
        return _refuse(
            "decision_not_found",
            f"{decision_id!r} is not this job's open budget decision",
        )

    if budget_stop_answer(job) is not None:
        return _refuse(
            "decision_already_answered",
            f"decision {decision_id} is already answered since the job last stopped",
        )

    if option not in ("extend", "abandon"):
        return _refuse("invalid_argument", "--reason must be 'extend' or 'abandon'.")

    if option == "abandon":
        if answers:
            return _refuse(
                "option_not_applicable",
                "--answer is not valid with --reason abandon; abandon cancels "
                "the job outright and raises nothing.",
            )
        record = {
            "decision_id": decision_id,
            "request_id": str(getattr(job, "stop_request_id", "") or ""),
            "option": "abandon",
            "raised": {},
            "answered_at": now.isoformat(),
            "actor": _ACTOR,
        }
        if not isinstance(getattr(job, "metadata", None), dict):
            job.metadata = {}
        job.metadata.setdefault("budget_decision_answers", []).append(record)
        job.state = RunState.CANCELLED
        return {"outcome": "abandoned", "state": "cancelled", "record": record}

    if not answers:
        return _refuse(
            "missing_argument",
            "at least one --answer is required, e.g. --answer max_cost_usd=2.5",
        )

    stop_reason = str(getattr(job, "stop_reason", "") or "")
    stop_limit = _stop_reason_limit(stop_reason)
    if stop_limit == _UNRAISABLE_LIMIT:
        return _refuse(
            "budget_limit_not_raisable",
            f"{_UNRAISABLE_LIMIT} is a floor set in configuration and is never "
            "raised per job.",
        )

    parsed: dict[str, Any] = {}
    for item in answers:
        text = str(item)
        if "=" not in text:
            return _refuse(
                "invalid_budget",
                f"malformed --answer {text!r}: expected <limit>=<value>, "
                "e.g. --answer max_cost_usd=2.5",
            )
        name, _, raw_value = text.partition("=")
        name = name.strip()
        if name not in _LIMIT_NAMES:
            return _refuse(
                "invalid_budget",
                f"unknown limit {name!r}. Limits: {', '.join(_LIMIT_NAMES)}.",
            )
        if name in parsed:
            return _refuse("invalid_budget", f"duplicate --answer for limit {name!r}.")
        try:
            value = parse_budget_limit(name, raw_value)
        except BudgetConfigError as exc:
            return _refuse("invalid_budget", str(exc))
        if value is None:
            return _refuse("invalid_budget", f"{name} is empty.")
        parsed[name] = value

    if stop_limit and stop_limit in _LIMIT_NAMES and stop_limit not in parsed:
        return _refuse(
            "budget_limit_not_raised",
            f"the stop names {stop_limit}, which --answer did not raise.",
        )

    current_raw = getattr(job, "budgets", None)
    try:
        current = JobBudgets.model_validate(
            current_raw if isinstance(current_raw, dict) else {})
    except ValueError as exc:
        return _refuse("invalid_budget", f"the job's current budgets do not validate: {exc}")

    for name, value in parsed.items():
        if name == "deadline":
            if value <= now:
                return _refuse(
                    "budget_limit_not_raised",
                    f"deadline must be later than now ({now.isoformat()}), "
                    f"got {value.isoformat()}.",
                )
            if current.deadline is not None and value <= current.deadline:
                return _refuse(
                    "budget_limit_not_raised",
                    "deadline must be later than the job's current deadline "
                    f"({current.deadline.isoformat()}).",
                )
        else:
            current_value = getattr(current, name)
            if current_value is not None and not value > current_value:
                return _refuse(
                    "budget_limit_not_raised",
                    f"{name} must be raised above its current value of "
                    f"{current_value}, got {value}.",
                )

    try:
        merged = JobBudgets(**{**current.model_dump(mode="python"), **parsed})
    except ValueError as exc:
        return _refuse("invalid_budget", f"the raised budgets do not validate: {exc}")

    budgets_json = merged.model_dump(mode="json")
    raised = {name: budgets_json[name] for name in parsed}

    record = {
        "decision_id": decision_id,
        "request_id": str(getattr(job, "stop_request_id", "") or ""),
        "option": "extend",
        "raised": dict(raised),
        "answered_at": now.isoformat(),
        "actor": _ACTOR,
    }

    if not isinstance(getattr(job, "metadata", None), dict):
        job.metadata = {}
    job.metadata.setdefault("budget_decision_answers", []).append(record)
    job.budgets = budgets_json

    return {
        "outcome": "extended", "raised": dict(raised), "budgets": budgets_json,
        "record": record,
    }
