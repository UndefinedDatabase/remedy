"""One budget authority for a whole `remedy do` order (2026-10-17 scale audit P1-4).

A job's budget (`JobBudgets`) used to be handed unchanged to every job of a walk, and the planning
calls before the first job (study narration, mission plan, intake, task plan) were outside every
budget, so an order's real spend was its cap times its jobs plus whatever planning cost. The
order's caps (`ctx.budgets`: the flags or the order file's header) are now the ORDER's caps:

- every planner call the walk makes is recorded here, with its reason, attempt, elapsed seconds,
  size, outcome and an ESTIMATED token count (the planner interface returns text, not usage, so the
  tokens of a planning call are never claimed as measured);
- each job runs with what is left of the caps after the planning calls and the jobs before it;
- a planning call that would pass the remaining call or token cap is refused, which the planner's
  callers already read as a provider failure and answer with the deterministic plan;
- when nothing is left, the walk stops before the next job instead of starting it.

Remedy deliberately does not retry, escalate or loop on a refused call: the refusal is final for
that order, and the entry says why.
"""
from __future__ import annotations

import contextlib
import contextvars
import math
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

#: The schema a planner call is bound to, read as the reason the call was made.
CALL_REASONS = {
    "JobIntake": "intake",
    "TaskPlan": "task_plan",
    "MissionPlanDraft": "mission_plan",
    "StudyCategoryNarration": "study_narration",
}
#: Characters per token for the estimate of a planning call; labelled an estimate wherever shown.
CHARS_PER_ESTIMATED_TOKEN = 4

_BOUND: contextvars.ContextVar[OrderCallLedger | None] = contextvars.ContextVar(
    "remedy_order_call_ledger", default=None)


#: This many planner calls failing one after the other end planner use for the order: a provider that
#: is down or hung is not asked a third time by the next step, and the step falls back or fails.
PLANNER_FAILURE_LIMIT = 2


class OrderCallRefusedError(RuntimeError):
    """A planning call was refused: the order's own caps are spent, or the planner keeps failing."""


@dataclass
class OrderCallLedger:
    """The planner calls of one order and the share of its caps they and its jobs have used."""

    caps: dict[str, Any] | None = None
    clock: Callable[[], float] = time.monotonic
    started: float = field(default=0.0)
    entries: list[dict[str, Any]] = field(default_factory=list)
    #: job id -> what that job's persisted actuals say it used.
    jobs: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Planner calls that raised since the last one that answered.
    failures_in_a_row: int = 0

    def __post_init__(self) -> None:
        self.started = self.clock()

    # --- recording -------------------------------------------------------------------------

    def record_planner_call(self, reason: str, *, attempt: int, seconds: float, prompt_chars: int,
                            response_chars: int, outcome: str) -> None:
        self.entries.append({
            "role": "planner", "reason": reason, "attempt": attempt, "seconds": round(seconds, 3),
            "prompt_chars": prompt_chars, "response_chars": response_chars, "outcome": outcome,
            "estimated_tokens": (prompt_chars + response_chars) // CHARS_PER_ESTIMATED_TOKEN,
            "tokens_estimated": True})

    def record_job(self, job: Any) -> None:
        """Take the job's persisted actuals (calls, tokens, money) into the order's spend."""
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            decode_persisted_budget_actuals,
        )
        raw = getattr(job, "budget_actuals", None)
        used: dict[str, Any] = {"calls": 0, "tokens": 0, "cost_usd": None, "measured": False,
                                "unpriced_calls": 0}
        if raw:
            try:
                actuals = decode_persisted_budget_actuals(raw)
            except BudgetCounterError:
                actuals = None
            if actuals is not None:
                calls, cost = actuals["provider_call_count"], actuals.get("measured_cost_usd")
                # a job that made calls and reported no price is unpriced, not free
                unpriced = actuals.get("unpriced_call_count", 0) or (calls if cost is None else 0)
                used = {"calls": calls, "tokens": actuals["total_tokens"], "cost_usd": cost,
                        "measured": True, "unpriced_calls": unpriced}
        if not used["measured"]:
            used["unpriced_calls"] = 1      # nothing says what it spent, so it is not known to be free
        self.jobs[str(job.job_id)] = used

    def wrap(self, reason: str, call_fn: Callable[[str, int], str]) -> Callable[[str, int], str]:
        """*call_fn* recorded here, and refused with `OrderCallRefusedError` once the caps are spent."""
        def recorded(prompt: str, attempt: int) -> str:
            # The study's narration passes its token limit in the attempt slot; it has no retries.
            attempt = 0 if reason == "study_narration" else attempt
            refusal = self.exhausted()
            if not refusal and self.failures_in_a_row >= PLANNER_FAILURE_LIMIT:
                refusal = (f"the planner failed {self.failures_in_a_row} calls in a row; it is not "
                           "asked again for this order")
            if refusal:
                self.record_planner_call(reason, attempt=attempt, seconds=0.0,
                                         prompt_chars=len(prompt), response_chars=0,
                                         outcome=f"refused: {refusal}")
                raise OrderCallRefusedError(refusal)
            began = self.clock()
            try:
                text = call_fn(prompt, attempt)
            except Exception as exc:
                self.failures_in_a_row += 1
                self.record_planner_call(reason, attempt=attempt, seconds=self.clock() - began,
                                         prompt_chars=len(prompt), response_chars=0,
                                         outcome=f"error: {type(exc).__name__}")
                raise
            self.failures_in_a_row = 0
            self.record_planner_call(reason, attempt=attempt, seconds=self.clock() - began,
                                     prompt_chars=len(prompt), response_chars=len(text or ""),
                                     outcome="ok")
            return text
        for name in ("resolved_model",):
            if hasattr(call_fn, name):
                setattr(recorded, name, getattr(call_fn, name))
        return recorded

    # --- the shares --------------------------------------------------------------------------

    @property
    def planner_calls(self) -> int:
        return sum(1 for entry in self.entries if not entry["outcome"].startswith("refused"))

    def used(self) -> dict[str, Any]:
        """Calls, tokens (measured by jobs, estimated for planning) and measured money spent so far."""
        planning_tokens = sum(e["estimated_tokens"] for e in self.entries
                              if not e["outcome"].startswith("refused"))
        cost = [j["cost_usd"] for j in self.jobs.values() if j["cost_usd"] is not None]
        return {
            "calls": self.planner_calls + sum(j["calls"] for j in self.jobs.values()),
            "tokens": planning_tokens + sum(j["tokens"] for j in self.jobs.values()),
            "cost_usd": sum(cost) if cost else None,
            "elapsed_minutes": (self.clock() - self.started) / 60.0,
        }

    def unpriced_calls(self) -> int:
        """Calls whose money is unknown: every planner call (the planner reports text, not a price)
        and the calls of a job that reported none."""
        return self.planner_calls + sum(j["unpriced_calls"] for j in self.jobs.values())

    def cost_summary(self) -> dict[str, Any]:
        """What the order can say about its money: the measured floor and whether the cap held."""
        cap = (self.caps or {}).get("max_cost_usd")
        unpriced = self.unpriced_calls()
        return {"cap_usd": cap, "measured_usd": self.used()["cost_usd"], "unpriced_calls": unpriced,
                "enforced": cap is not None and unpriced == 0}

    def exhausted(self) -> str:
        """Why the order has nothing left to spend on another call, or "" while it has."""
        caps = self.caps or {}
        if (cap := caps.get("max_cost_usd")) is not None and (unpriced := self.unpriced_calls()):
            # Unknown spend is not zero spend: a money cap that cannot be checked is not a cap
            # that holds, so nothing more starts under it (token, call and time caps still work).
            return (f"the order's cap of {cap} USD cannot be enforced: {unpriced} call(s) so far "
                    "carry no price, so the spend is unknown")
        used = self.used()
        for cap_key, used_key, unit in (("max_provider_calls", "calls", "provider calls"),
                                        ("max_total_tokens", "tokens", "tokens"),
                                        ("max_cost_usd", "cost_usd", "USD")):
            cap = caps.get(cap_key)
            if cap is not None and used[used_key] is not None and used[used_key] >= cap:
                return f"the order's cap of {cap} {unit} is spent ({used[used_key]} used)"
        minutes = caps.get("max_wall_clock_minutes")
        if minutes is not None and used["elapsed_minutes"] >= minutes:
            return f"the order's cap of {minutes} minute(s) of wall-clock time is spent"
        return ""

    def remaining(self) -> dict[str, Any] | None:
        """The order's caps less what is spent: the budgets the next job runs with (None: uncapped)."""
        if not self.caps:
            return None
        used = self.used()
        left = dict(self.caps)
        for cap_key, used_key in (("max_provider_calls", "calls"), ("max_total_tokens", "tokens")):
            if left.get(cap_key) is not None:
                left[cap_key] = max(1, left[cap_key] - used[used_key])
        if left.get("max_cost_usd") is not None and used["cost_usd"] is not None:
            left["max_cost_usd"] = max(left["max_cost_usd"] - used["cost_usd"], 1e-9)
        if left.get("max_wall_clock_minutes") is not None:
            left["max_wall_clock_minutes"] = max(
                1, math.ceil(left["max_wall_clock_minutes"] - used["elapsed_minutes"]))
        return left

    def summary(self) -> dict[str, Any]:
        """The order's planning calls and spend, for the walk's JSON and its evidence."""
        by_reason: dict[str, int] = {}
        for entry in self.entries:
            if not entry["outcome"].startswith("refused"):
                by_reason[entry["reason"]] = by_reason.get(entry["reason"], 0) + 1
        used = self.used()
        return {
            "caps": self.caps,
            "planner_calls": self.planner_calls,
            "planner_calls_by_reason": by_reason,
            "refused_calls": len(self.entries) - self.planner_calls,
            "estimated_planning_tokens": sum(e["estimated_tokens"] for e in self.entries),
            "used": {**used, "elapsed_minutes": round(used["elapsed_minutes"], 3)},
            "cost": self.cost_summary(),
            "jobs": dict(self.jobs),
            "unmeasured_jobs": [job_id for job_id, job in self.jobs.items() if not job["measured"]],
            "calls": list(self.entries),
        }


def reserve_waiting_budgets(job_ids: list[str], budgets: dict[str, Any] | None,
                            spent: str = "") -> list[str]:
    """Split what the walk leaves of the order's caps among the jobs it leaves waiting.

    A waiting job runs later, in another process, by `remedy job run`, and nothing makes those runs
    wait for one another. So the leftover is divided, not repeated: each job's share is the leftover
    over the number of jobs (calls, tokens, minutes and money; a deadline is shared as it is), and
    the shares add up to no more than the leftover however the jobs are run. When a whole-number cap
    cannot give every job one unit, the jobs after the first that can be funded get an already-passed
    deadline: they stop before their first call and wait for an operator's budget decision, the
    existing way to extend a cap; so do all of them when *spent* says the order has nothing left.
    Jobs that already carry budgets keep them. Returns the funded ids.
    """
    from datetime import datetime, timezone

    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    jobs = [job for job_id in job_ids if (job := load_job_plan(job_id)) is not None
            and job.budgets is None]
    if budgets is None or not jobs:
        return []
    slots = 0 if spent else len(jobs)
    for key in ("max_provider_calls", "max_total_tokens", "max_wall_clock_minutes"):
        if budgets.get(key) is not None:
            slots = min(slots, budgets[key])
    share = dict(budgets)
    for key in ("max_provider_calls", "max_total_tokens", "max_wall_clock_minutes"):
        if share.get(key) is not None:
            share[key] = share[key] // max(slots, 1)
    if share.get("max_cost_usd") is not None:
        share["max_cost_usd"] = share["max_cost_usd"] / max(slots, 1)
    given: list[str] = []
    for position, job in enumerate(jobs):
        job.budgets = dict(share)
        if position >= slots:
            job.budgets["deadline"] = datetime.now(timezone.utc).isoformat()
        save_job_plan(job)
        if position < slots:
            given.append(str(job.job_id))
    return given


def reason_for(model_cls: Any) -> str:
    """The reason a planner call bound to *model_cls* is made."""
    name = getattr(model_cls, "__name__", str(model_cls))
    return CALL_REASONS.get(name, name)


def bound_order_ledger() -> OrderCallLedger | None:
    """The ledger of the walk running in this context, or None outside a `remedy do` walk."""
    return _BOUND.get()


@contextlib.contextmanager
def bind_order_ledger(ledger: OrderCallLedger) -> Iterator[OrderCallLedger]:
    """Make *ledger* the one every planner call made inside the block is recorded on."""
    token = _BOUND.set(ledger)
    try:
        yield ledger
    finally:
        _BOUND.reset(token)
