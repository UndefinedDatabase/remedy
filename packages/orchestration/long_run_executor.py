"""Multi-cycle loop conductor (F046 T001).

Remedy can work in bounded CYCLES instead of a single pass::

    check should_stop -> determine the ready task batch -> execute up to
    batch_size tasks -> run the verify step -> persist -> repeat

until a terminal condition is reached.  This module is the CONDUCTOR only.
It sequences parts that already exist and reimplements none of them:

  * should_stop      ``safe_points.should_stop`` (operator stop + budgets in
                     ONE evaluation per safe point)
  * task execution   ``task_runner.run_next_task`` — rollback-on-failure stays
                     that module's concern
  * verification     ``verifier.verify_task_output`` + ``task_runner.finalize_task``
  * persistence      ``storage.save_job`` — no new persistence path
  * job status       the ``pingpong_job.JOB_*`` constants

Readiness is LINEAR: the ready set is the PENDING tasks in ``job.tasks``
order.  DAG readiness is a later feature and is deliberately absent here.

Terminal statuses and how they map onto job state:

    | terminal status     | pingpong job status | core RunState |
    |---------------------|---------------------|---------------|
    | all_green           | completed           | COMPLETED     |
    | stopped_by_operator | stopped             | PAUSED        |
    | budget_exhausted    | stopped             | PAUSED        |
    | deadline_reached    | stopped             | PAUSED        |
    | blocked             | blocked             | PAUSED        |
    | max_cycles_reached  | running             | RUNNING       |

``blocked`` maps to PAUSED rather than FAILED because "no ready task and not
green" also covers a job awaiting a decision — nothing has failed, so the job
must stay resumable.  ``RunState`` has no BLOCKED member; the exact status
lives in ``job.metadata["cycle_terminal_status"]`` and in the ledger event.

``max_cycles_reached`` is not a stop CAUSE — it is the loop honoring its cycle
budget with work still pending.  It leaves job state untouched, which is what
makes ``max_cycles=1`` (the rollout default until the F075 gate) behave exactly
like today's single pass.

Nothing in here sleeps.  Wall-clock and deadline evaluation go through the
injected ``clock``, so a deadline is provable in a unit test.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from packages.core.models import Job, JobBudgets, RunState
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_RUNNING,
    JOB_STOPPED,
)
from packages.orchestration.safe_points import should_stop as _should_stop
from packages.orchestration.storage import save_job as _save_job
from packages.orchestration.task_runner import (
    finalize_task,
    materialize_task_output,
    run_next_task,
)
from packages.orchestration.verifier import verify_task_output

# ---------------------------------------------------------------------------
# Terminal statuses
# ---------------------------------------------------------------------------

TERMINAL_ALL_GREEN = "all_green"
TERMINAL_STOPPED_BY_OPERATOR = "stopped_by_operator"
TERMINAL_BUDGET_EXHAUSTED = "budget_exhausted"
TERMINAL_DEADLINE_REACHED = "deadline_reached"
TERMINAL_BLOCKED = "blocked"
TERMINAL_MAX_CYCLES_REACHED = "max_cycles_reached"

#: terminal status -> pingpong_job job status constant.
TERMINAL_JOB_STATUS: dict[str, str] = {
    TERMINAL_ALL_GREEN: JOB_COMPLETED,
    TERMINAL_STOPPED_BY_OPERATOR: JOB_STOPPED,
    TERMINAL_BUDGET_EXHAUSTED: JOB_STOPPED,
    TERMINAL_DEADLINE_REACHED: JOB_STOPPED,
    TERMINAL_BLOCKED: JOB_BLOCKED,
    TERMINAL_MAX_CYCLES_REACHED: JOB_RUNNING,
}

#: terminal status -> core RunState written on the Job, or None to leave the
#: state exactly as the task runner left it.
TERMINAL_RUN_STATE: dict[str, RunState | None] = {
    TERMINAL_ALL_GREEN: RunState.COMPLETED,
    TERMINAL_STOPPED_BY_OPERATOR: RunState.PAUSED,
    TERMINAL_BUDGET_EXHAUSTED: RunState.PAUSED,
    TERMINAL_DEADLINE_REACHED: RunState.PAUSED,
    TERMINAL_BLOCKED: RunState.PAUSED,
    TERMINAL_MAX_CYCLES_REACHED: None,
}

#: Ledger event names emitted through the injected run-log writer.
LEDGER_EVENT_CYCLE_COMPLETED = "cycle_completed"
LEDGER_EVENT_LOOP_TERMINAL = "cycle_loop_terminal"

#: Verify-step outcomes.  "not_run" is recorded verbatim — a cycle that ran no
#: verification never claims a passing one.
VERIFY_NOT_RUN = "not_run"
VERIFY_PASSED = "passed"
VERIFY_FAILED = "failed"
#: Verify outcomes that deny the job the all_green status.
_VERIFY_DENIES_GREEN = frozenset({VERIFY_FAILED, "timeout"})

#: Rollout rule (F046): one cycle until the F075 milestone gate flips it.
DEFAULT_MAX_CYCLES = 1
DEFAULT_BATCH_SIZE = 1


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CycleLimits:
    """Bounds for one ``run_cycles`` invocation.

    max_cycles:     maximum number of cycles this call may run.  The rollout
                    cap that keeps production at one cycle lives in the
                    caller (see ``resolve_max_cycles``), not here, so tests and
                    the post-gate configuration can drive the real loop.
    batch_size:     maximum tasks executed per cycle.
    budgets:        F018 limits handed to ``should_stop``; None disables the
                    budget half of the safe point (operator stop still applies).
    verify_command: recorded on every cycle record and passed to the verify
                    callable; None means "no override configured".
    """

    max_cycles: int = DEFAULT_MAX_CYCLES
    batch_size: int = DEFAULT_BATCH_SIZE
    budgets: JobBudgets | None = None
    verify_command: str | None = None

    def __post_init__(self) -> None:
        if self.max_cycles < 0:
            raise ValueError(f"max_cycles must be >= 0, got {self.max_cycles}")
        if self.batch_size < 1:
            raise ValueError(f"batch_size must be >= 1, got {self.batch_size}")


ProviderCall = Callable[[TaskExecutionContext], BuilderOutput]
#: (job, provider_call) -> TaskAttempt.  Executes exactly ONE ready task.
TaskStep = Callable[[Job, ProviderCall], "TaskAttempt"]
#: (job, cycle_index, verify_command) -> one of the VERIFY_* strings.
VerifyStep = Callable[[Job, int, str | None], str]


@dataclass(frozen=True)
class TaskAttempt:
    """Outcome of one single-task step inside a cycle."""

    task_id: UUID | None = None
    executed: bool = False
    verified: bool = False
    error: str = ""


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CycleRecord:
    """One cycle's own summary — the unit the evidence area stores (T002)."""

    cycle_index: int
    tasks_attempted: int
    tasks_completed: int
    tasks_failed: int
    verify_result: str
    tokens_so_far: int
    started_at: str
    ended_at: str
    verify_command: str | None = None
    errors: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "cycle_index": self.cycle_index,
            "tasks_attempted": self.tasks_attempted,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "verify_result": self.verify_result,
            "verify_command": self.verify_command,
            "tokens_so_far": self.tokens_so_far,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "errors": list(self.errors),
        }


@dataclass(frozen=True)
class CycleLoopResult:
    """What the whole loop did."""

    job: Job
    terminal_status: str
    job_status: str
    stop_reason: str = ""
    cycles: tuple[CycleRecord, ...] = ()

    @property
    def cycles_run(self) -> int:
        return len(self.cycles)

    def to_json(self) -> dict[str, Any]:
        return {
            "job_id": str(self.job.id),
            "terminal_status": self.terminal_status,
            "job_status": self.job_status,
            "stop_reason": self.stop_reason,
            "cycles_run": self.cycles_run,
            "cycles": [c.to_json() for c in self.cycles],
        }


# ---------------------------------------------------------------------------
# Default steps (the existing single-task path — nothing new)
# ---------------------------------------------------------------------------


def default_task_step(job: Job, provider_call: ProviderCall) -> TaskAttempt:
    """Run ONE ready task through the existing single-task path.

    run_next_task -> materialize -> verify_task_output -> finalize_task, which
    is exactly what ``remedy job run-next`` does.  Rollback on builder failure
    is ``run_next_task``'s concern; the exception is translated into a failed
    attempt so the conductor can end the cycle and record it.
    """
    from packages.orchestration.workspace import LocalWorkspaceRuntime

    try:
        result = run_next_task(job, provider_call)
    except Exception as exc:  # noqa: BLE001 — the cycle records any failure cause
        return TaskAttempt(error=f"{type(exc).__name__}: {exc}")

    if not result.changed or result.task_id is None:
        return TaskAttempt()

    runtime = LocalWorkspaceRuntime(job_id=job.id)
    materialize_task_output(result, runtime)
    vr = verify_task_output(result.job, result.task_id)
    finalize_task(result, vr)
    return TaskAttempt(
        task_id=result.task_id,
        executed=True,
        verified=vr.passed,
        error="" if vr.passed else f"verification_failed: {len(vr.failures)} check(s)",
    )


def _no_verify(job: Job, cycle_index: int, verify_command: str | None) -> str:
    """The default verify step: none configured, and it says so."""
    return VERIFY_NOT_RUN


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ready_tasks(job: Job, batch_size: int) -> list[UUID]:
    """The ready batch: PENDING tasks in job order, capped at batch_size.

    Linear on purpose — DAG readiness is a later feature.  A batch larger than
    the number of remaining tasks is fine; the list is simply shorter.
    """
    pending = [t.id for t in job.tasks if t.status == RunState.PENDING]
    return pending[:batch_size]


def _is_green(job: Job, last_verify: str) -> bool:
    """Every task completed AND the last verify step did not fail."""
    if not job.tasks:
        return False
    if not all(t.status == RunState.COMPLETED for t in job.tasks):
        return False
    return last_verify not in _VERIFY_DENIES_GREEN


def _default_counters(
    job: Job,
    *,
    now: datetime,
    started_at: datetime,
    provider_calls: int,
) -> BudgetCounters:
    """Counters for the budget half of the safe point.

    Prefers the actuals persisted by the job runner (the same source
    ``remedy job budget`` reads).  When there are none, it reports what this
    loop can honestly observe: the provider calls it made itself, all of them
    UNMEASURED — a token total this loop never measured is never claimed.
    """
    try:
        from packages.orchestration.budget_guard import (
            counters_from_persisted,
            decode_persisted_budget_actuals,
        )
        from packages.orchestration.pingpong_job import load_job_plan

        plan = load_job_plan(str(job.id))
        actuals = getattr(plan, "budget_actuals", None) if plan is not None else None
        if actuals is not None:
            validated = decode_persisted_budget_actuals(
                actuals, first_running_at=getattr(plan, "first_running_at", "") or None)
            return counters_from_persisted(validated, now=now)
    except Exception:  # noqa: BLE001 — corrupt/absent actuals must not stop the loop
        pass

    return BudgetCounters(
        provider_calls=provider_calls,
        unmeasured_call_count=provider_calls,
        elapsed_seconds=max(0.0, (now - started_at).total_seconds()),
        evaluated_at=now,
        started_at=started_at,
    )


def _terminal_from_stop(reason: str, source: str) -> str:
    """Translate a ShouldStopResult into a terminal status.

    ``should_stop`` reports budget exhaustion as ``budget_exhausted:<limit>``;
    the deadline limit is its own terminal status because operators read those
    two very differently.
    """
    if source == "operator":
        return TERMINAL_STOPPED_BY_OPERATOR
    if reason.endswith(":deadline"):
        return TERMINAL_DEADLINE_REACHED
    return TERMINAL_BUDGET_EXHAUSTED


def _apply_terminal(job: Job, terminal_status: str, stop_reason: str) -> str:
    """Write the terminal status onto the job and return the job status."""
    job_status = TERMINAL_JOB_STATUS[terminal_status]
    run_state = TERMINAL_RUN_STATE[terminal_status]
    if run_state is not None:
        job.state = run_state
    job.metadata["cycle_terminal_status"] = terminal_status
    job.metadata["cycle_job_status"] = job_status
    if stop_reason:
        job.metadata["cycle_stop_reason"] = stop_reason
    else:
        job.metadata.pop("cycle_stop_reason", None)
    return job_status


def _emit(log: Any, event: str, **meta: Any) -> None:
    """Emit a ledger event when a writer was injected; never raise into the loop."""
    if log is None:
        return
    try:
        log.log(event, **meta)
    except Exception:  # noqa: BLE001 — a ledger write must not break execution
        pass


# ---------------------------------------------------------------------------
# The loop
# ---------------------------------------------------------------------------


def run_cycles(
    job: Job,
    limits: CycleLimits,
    provider_call: ProviderCall,
    *,
    task_step: TaskStep | None = None,
    verify: VerifyStep | None = None,
    clock: Callable[[], datetime] | None = None,
    save: Callable[[Job], None] | None = None,
    log: Any = None,
    control_root_path: Any = None,
) -> CycleLoopResult:
    """Run bounded cycles over *job* until a terminal condition.

    One cycle is: safe point -> ready batch -> execute -> verify -> persist.
    The safe point is evaluated BEFORE any work of a cycle begins, so a cycle
    never starts after should_stop says stop.

    Seams (all default to the existing production path):
      task_step  one ready task through run_next_task + verify + finalize
      verify     the per-cycle verify step; the default runs nothing and
                 records ``not_run``
      clock      the only source of "now" — the loop never sleeps
      save       ``storage.save_job``
      log        anything with ``.log(event, **meta)`` (a RunLogWriter); when
                 omitted, no ledger events are emitted

    A failed verify ends the cycle with its failure recorded and denies the job
    the all_green status; self-healing is a later feature.  A task step that
    fails ends the cycle too — the task runner has already rolled the task back
    to PENDING, so the next cycle (if the budget allows one) retries it.
    """
    step = task_step or default_task_step
    verify_step = verify or _no_verify
    now_fn = clock or (lambda: datetime.now(timezone.utc))
    save_fn = save or _save_job

    loop_started_at = now_fn()
    provider_calls = 0
    cycles: list[CycleRecord] = []
    last_verify = VERIFY_NOT_RUN

    def counted_provider_call(context: TaskExecutionContext) -> BuilderOutput:
        nonlocal provider_calls
        provider_calls += 1
        return provider_call(context)

    while True:
        now = now_fn()

        # 1. Safe point FIRST — operator stop and budgets in one evaluation.
        stop = _should_stop(
            str(job.id),
            budgets=limits.budgets,
            counters=_default_counters(
                job, now=now, started_at=loop_started_at,
                provider_calls=provider_calls),
            now=now,
            control_root_path=control_root_path,
        )
        if stop.should_stop:
            terminal = _terminal_from_stop(stop.reason, stop.source)
            stop_reason = stop.reason
            break

        # 2. Terminal by job shape: green, or nothing ready and not green.
        batch = ready_tasks(job, limits.batch_size)
        if not batch:
            if _is_green(job, last_verify):
                terminal, stop_reason = TERMINAL_ALL_GREEN, ""
            else:
                terminal = TERMINAL_BLOCKED
                stop_reason = (
                    "no_tasks" if not job.tasks
                    else f"no_ready_tasks; last_verify={last_verify}"
                )
            break

        # 3. Cycle budget.  Not a stop cause — pending work simply remains.
        if len(cycles) >= limits.max_cycles:
            terminal, stop_reason = TERMINAL_MAX_CYCLES_REACHED, ""
            break

        # 4. Run the cycle.
        cycle_index = len(cycles) + 1
        started_at = now
        attempted = completed = failed = 0
        errors: list[str] = []

        for _ in batch:
            attempt = step(job, counted_provider_call)
            if not attempt.executed and not attempt.error:
                break                      # nothing ready any more; not an attempt
            attempted += 1
            if attempt.verified:
                completed += 1
                continue
            # A failed task step or a failed verification ends the cycle with
            # the failure recorded.  The task runner already rolled the task
            # back to PENDING; retrying it inside the same cycle would be a
            # retry policy, which is not this module's concern.
            failed += 1
            if attempt.error:
                errors.append(attempt.error)
            break

        last_verify = verify_step(job, cycle_index, limits.verify_command)
        if last_verify == VERIFY_FAILED:
            errors.append("verify_failed")

        ended_at = now_fn()
        counters = _default_counters(
            job, now=ended_at, started_at=loop_started_at,
            provider_calls=provider_calls)
        record = CycleRecord(
            cycle_index=cycle_index,
            tasks_attempted=attempted,
            tasks_completed=completed,
            tasks_failed=failed,
            verify_result=last_verify,
            tokens_so_far=counters.measured_token_total,
            started_at=started_at.isoformat(),
            ended_at=ended_at.isoformat(),
            verify_command=limits.verify_command,
            errors=tuple(errors),
        )
        cycles.append(record)

        # 5. Persist.
        save_fn(job)
        _emit(log, LEDGER_EVENT_CYCLE_COMPLETED, **record.to_json())

    job_status = _apply_terminal(job, terminal, stop_reason)
    save_fn(job)
    _emit(
        log, LEDGER_EVENT_LOOP_TERMINAL,
        terminal_status=terminal, job_status=job_status,
        stop_reason=stop_reason, cycles_run=len(cycles),
    )
    return CycleLoopResult(
        job=job,
        terminal_status=terminal,
        job_status=job_status,
        stop_reason=stop_reason,
        cycles=tuple(cycles),
    )
