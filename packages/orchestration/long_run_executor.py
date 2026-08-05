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

Readiness is TOPOLOGICAL (F050): the ready set is the PENDING tasks whose
Flight Plan dependencies are all COMPLETED, in plan order — computed by the
pure ``dag_schedule`` module.  Plans without dependency metadata keep behaving
exactly linearly, because the rule there is "each task depends on its
predecessor".  A task whose attempt executed and failed blocks its own
transitive downstream for the rest of the run and nothing else, so independent
branches keep running; those withheld ids are named in the cycle record.
Execution itself stays SEQUENTIAL — the ready set feeds one batch at a time
and this module never starts a thread.

A task may also raise ``needs_decision`` (F051) instead of finishing or
failing.  One decision is enqueued on the existing decision queue, that branch
pauses, and the loop keeps pulling ready tasks from every disjoint branch.  At
each batch boundary the awaiting branches are re-checked once against the job's
open decisions, so a decision answered while the run is still working elsewhere
is picked up without a restart and without a polling loop.  A run that ends
with open decisions is ``blocked`` — PAUSED, resumable, and the report says
which command answers what.

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

import contextlib
import inspect
import json
from collections.abc import Callable, Collection
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.core.models import Job, JobBudgets, RunState
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.dag_schedule import blocked_downstream
from packages.orchestration.dag_schedule import ready_set as dag_ready_set
from packages.orchestration.escalation import awaiting_decision_task_ids
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
#: F048: the idle loop took (or failed to take) a queued entry.
LEDGER_EVENT_QUEUE_PULL = "queue_pull"
#: F051: a task raised a question, and what happened to it.
LEDGER_EVENT_TASK_NEEDS_DECISION = "task_needs_decision"
LEDGER_EVENT_DECISION_ANSWERED = "task_decision_answered"
#: F052: one event per repair round that really ran, and one when a cycle healed.
LEDGER_EVENT_CYCLE_REPAIR_ROUND = "cycle_repair_round"
LEDGER_EVENT_CYCLE_HEALED = "cycle_healed"

#: Verify-step outcomes.  "not_run" is recorded verbatim — a cycle that ran no
#: verification never claims a passing one.
VERIFY_NOT_RUN = "not_run"
VERIFY_PASSED = "passed"
VERIFY_FAILED = "failed"
#: F052: the verify step itself could not run (command missing, bad config), and
#: the outcome where nothing said which.  These are NOT test failures — they deny
#: green like any failure, but they say something different about the run, and
#: F052's self-healing never spends a repair round on them.
VERIFY_CONFIG_ERROR = "config"
VERIFY_UNKNOWN_ERROR = "unknown"
#: Verify outcomes that deny the job the all_green status.
_VERIFY_DENIES_GREEN = frozenset(
    {VERIFY_FAILED, "timeout", VERIFY_CONFIG_ERROR, VERIFY_UNKNOWN_ERROR})
#: The ONLY verify outcome a repair round may be spent on (F052).  Repairing a
#: broken harness spends provider money on a problem no patch can fix.
_VERIFY_REPAIRABLE = frozenset({VERIFY_FAILED})

#: Rollout rule (F046): one cycle until the F075 milestone gate flips it.
DEFAULT_MAX_CYCLES = 1
DEFAULT_BATCH_SIZE = 1

#: The rollout CAP.  Config value and CLI flag are both clamped to it, so the
#: shipped default stays a single pass no matter what is configured.  Only the
#: F075 milestone gate raises this, via an explicit change with an ADR.
CYCLE_SAFETY_CAP = 1

#: F052 rollout rule: two bounded repair rounds on a failed verify, and never
#: more — the rounds are provider work like any other and stop where it stops.
DEFAULT_REPAIR_ROUNDS = 2

#: Config keys this feature owns.
CONFIG_KEY_MAX_CYCLES = "cycles.max_cycles"
CONFIG_KEY_BATCH_SIZE = "cycles.batch_size"
CONFIG_KEY_VERIFY_COMMAND = "cycles.verify_command"
CONFIG_KEY_REPAIR_ROUNDS = "cycles.repair_rounds"

#: Where a cycle's own evidence record lands, and how it is named.
CYCLE_EVIDENCE_DIRNAME = "cycles"
CYCLE_RECORD_FILENAME = "cycle_{index:04d}.json"


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
    repair_rounds:  F052 — how many bounded repair rounds a FAILED verify may
                    spend before the cycle keeps its failure.  0 disables
                    self-healing.

                    This field defaults to 0 while the CONFIG key defaults to
                    ``DEFAULT_REPAIR_ROUNDS`` on purpose: a caller that builds
                    its limits by hand asked for exactly the bounds it named,
                    and silently spending provider calls it never requested is
                    the one thing an auto-repair feature must not do.  The
                    product surface goes through ``limits_from_config``, which
                    supplies the configured default.
    """

    max_cycles: int = DEFAULT_MAX_CYCLES
    batch_size: int = DEFAULT_BATCH_SIZE
    budgets: JobBudgets | None = None
    verify_command: str | None = None
    repair_rounds: int = 0

    def __post_init__(self) -> None:
        if self.max_cycles < 0:
            raise ValueError(f"max_cycles must be >= 0, got {self.max_cycles}")
        if self.batch_size < 1:
            raise ValueError(f"batch_size must be >= 1, got {self.batch_size}")
        if self.repair_rounds < 0:
            raise ValueError(f"repair_rounds must be >= 0, got {self.repair_rounds}")


ProviderCall = Callable[[TaskExecutionContext], BuilderOutput]
#: (job, provider_call) -> TaskAttempt.  Executes exactly ONE ready task.
TaskStep = Callable[[Job, ProviderCall], "TaskAttempt"]
#: (job, cycle_index, verify_command) -> one of the VERIFY_* strings, or a
#: :class:`VerifyOutcome` when the step can also report WHAT failed (F052).
#: Returning a bare string is the pre-F052 contract and stays supported.
VerifyStep = Callable[[Job, int, str | None], "str | VerifyOutcome"]
#: (job, cycle_index, findings) -> RepairOutcome.  ONE repair round (F052).
RepairStep = Callable[[Job, int, dict[str, Any]], "RepairOutcome"]


@dataclass(frozen=True)
class VerifyOutcome:
    """What a verify step observed, for steps that can say more than pass/fail.

    A bare ``"failed"`` says a cycle is broken but not what broke, which is
    exactly what a later reader — or a repair round — needs.  Steps written
    before F052 keep returning the string; the loop normalizes both shapes
    through :func:`as_verify_outcome`, so no existing caller changes.
    """

    result: str
    #: The tail of the failure text, already bounded by the step that owns it.
    output: str = ""
    failing_test_ids: tuple[str, ...] = ()
    #: Files this cycle changed — the hint a later reader starts from.
    changed_files: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepairOutcome:
    """What ONE repair round did (F052).

    ``ran`` is False when the round never started — no repair path is reachable
    in this deployment, for instance.  A round that did not start is never
    counted against the cap and never claimed in the evidence: an uncounted
    round would make "exactly two rounds" unprovable, and a claimed one would
    be a lie about money that was never spent.
    """

    ran: bool = False
    changed_files: tuple[str, ...] = ()
    stop_reason: str = ""
    error: str = ""


@dataclass(frozen=True)
class TaskAttempt:
    """Outcome of one single-task step inside a cycle."""

    task_id: UUID | None = None
    executed: bool = False
    verified: bool = False
    error: str = ""
    #: F051: the task cannot proceed without a human answer.  This is NOT a
    #: failure — nothing was attempted and lost — so the conductor enqueues one
    #: decision, pauses this branch only, and keeps pulling ready tasks from
    #: every other branch.  Every step written before F051 omits these and
    #: behaves exactly as it did.
    needs_decision: bool = False
    question: str = ""
    options: tuple[str, ...] = ()
    safe_default: str = ""


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
    #: F051: attempts that ended in ``needs_decision`` this cycle.  Counted
    #: separately from ``tasks_failed`` on purpose — an escalation is a question,
    #: not a failure, and a report that mixed the two would lie about the run.
    tasks_escalated: int = 0
    #: Ids of the tasks this cycle actually EXECUTED, in execution order.
    #: They are what makes exactly-once provable across a kill and a resume
    #: (F047 T003) — a counter in a test process cannot span two processes.
    #: A task that executed but failed verification is rolled back to PENDING
    #: and will appear again in a later cycle, which is honest: it really did
    #: execute twice.
    executed_task_ids: tuple[str, ...] = ()
    #: F050: ids withheld from the ready set because a task upstream of them is
    #: blocked in this run, in plan order.  This is what lets a report say WHY
    #: nothing happened on a branch instead of leaving a silent gap.
    skipped_blocked_task_ids: tuple[str, ...] = ()
    #: F051: tasks whose branch is paused on an OPEN decision, in plan order.
    awaiting_task_ids: tuple[str, ...] = ()
    #: F051: ids withheld only because something upstream of them awaits a
    #: decision — the awaiting counterpart of ``skipped_blocked_task_ids``.
    awaiting_downstream_task_ids: tuple[str, ...] = ()
    #: F051: the decisions this cycle raised, in the order they were raised.
    open_decision_ids: tuple[str, ...] = ()
    #: F052: the failure class of a verify that did not pass, from the EXISTING
    #: classifier (``failure_postmortem.classify``) rather than a second
    #: vocabulary.  Empty when the verify passed or never ran.
    verify_failure_class: str = ""
    #: F052: repair rounds this cycle actually spent on a FAILED verify.
    repair_rounds_used: int = 0
    #: F052: the verify passed again after those rounds.  Silent healing hides
    #: risk, so a heal is recorded and rendered rather than implied by a green
    #: cycle.
    healed_after_repair: bool = False
    #: F052 (A9): the heal changed no file.  A test that starts passing on its
    #: own is a flake suspect, and a human has to be able to see that.
    healed_without_changes: bool = False
    #: F052: the one-line account of the repair phase, ready to render.
    repair_summary: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "cycle_index": self.cycle_index,
            "tasks_attempted": self.tasks_attempted,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "tasks_escalated": self.tasks_escalated,
            "verify_result": self.verify_result,
            "verify_command": self.verify_command,
            "tokens_so_far": self.tokens_so_far,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "errors": list(self.errors),
            "executed_task_ids": list(self.executed_task_ids),
            "skipped_blocked_task_ids": list(self.skipped_blocked_task_ids),
            "awaiting_task_ids": list(self.awaiting_task_ids),
            "awaiting_downstream_task_ids": list(self.awaiting_downstream_task_ids),
            "open_decision_ids": list(self.open_decision_ids),
            "verify_failure_class": self.verify_failure_class,
            "repair_rounds_used": self.repair_rounds_used,
            "healed_after_repair": self.healed_after_repair,
            "healed_without_changes": self.healed_without_changes,
            "repair_summary": self.repair_summary,
        }


#: F048 executor binding. OFF by default: without it, this module behaves exactly as it
#: did before the queue existed, and no queued entry is ever consumed behind an operator's
#: back.
QUEUE_BINDING_CONFIG_KEY = "queue.executor_binding"

#: The loop is IDLE at these terminals — it ran out of work rather than being stopped,
#: budget-capped or cut short mid-flight. Only then may it take the next queued entry.
_IDLE_TERMINALS = frozenset({TERMINAL_ALL_GREEN, TERMINAL_BLOCKED})

QUEUE_PULL_PLANNED = "planned"
QUEUE_PULL_FAILED = "failed"


@dataclass(frozen=True)
class QueuePull:
    """One queue entry turned into a job (or honestly not).

    ``status`` is ``planned`` when the entry became a normal PLANNED job, ``failed`` when
    reading the goal or planning refused it — in which case the ENTRY is marked failed
    with the same reason, never left claimed by a consumer that has moved on.
    """

    entry_id: str
    status: str
    job_id: str = ""
    reason: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "status": self.status,
            "job_id": self.job_id,
            "reason": self.reason,
        }


def queue_binding_enabled(config: Any = None) -> bool:
    """Is the executor allowed to consume the queue? Opt-in, and closed on any doubt."""
    if config is None:
        try:
            from packages.orchestration.config import get_config

            config = get_config()
        except Exception:  # noqa: BLE001 — a config problem must not switch this ON
            return False
    try:
        return bool(config.get(QUEUE_BINDING_CONFIG_KEY))
    except Exception:  # noqa: BLE001
        return False


def _goal_text_for(entry: Any) -> str:
    """The prompt this entry stands for. A goal-file reference is read HERE, so an
    unreadable file fails the entry instead of creating a job with an empty prompt."""
    if entry.goal:
        return entry.goal
    try:
        text = Path(entry.goal_path).read_text(encoding="utf-8", errors="replace").strip()
    except OSError as exc:
        raise ValueError(
            f"goal file {entry.goal_path!r} could not be read: "
            f"{type(exc).__name__}: {exc}") from exc
    if not text:
        raise ValueError(f"goal file {entry.goal_path!r} is empty")
    return text


def queued_entry_to_job(entry: Any, *, save: Callable[[Job], None] | None = None) -> Job:
    """Turn a claimed queue entry into a NORMAL job, planned and persisted.

    Deliberately the same shape ``remedy job create`` + ``remedy job plan`` produce, and
    deliberately no further: the job stops at PLANNED. Nothing here executes a task,
    approves a plan or implies ``--yes`` — a queued goal reaches the operator's approval
    gate exactly like a typed one (A9).
    """
    from packages.orchestration.job_runner import plan_job

    prompt = _goal_text_for(entry)
    job = Job(
        name=prompt[:50],
        user_prompt=prompt,
        state=RunState.PENDING,
        metadata={"project_id": entry.project_id, "queue_entry_id": entry.id},
        project_id=entry.project_id,
    )
    plan_job(job)
    (save or _save_job)(job)
    return job


def _pull_queue_when_idle(job: Job, terminal: str, *, log: Any = None) -> QueuePull | None:
    """The binding: an idle loop takes the next entry for THIS job's project.

    Every guard here is a reason to do nothing — not enabled, not idle, no project, no
    queued entry. The default path therefore does exactly what it always did.
    """
    if terminal not in _IDLE_TERMINALS or not job.project_id:
        return None
    if not queue_binding_enabled():
        return None

    from packages.orchestration import job_queue as _queue

    try:
        entry = _queue.claim_next(str(job.project_id))
    except _queue.QueueError as exc:
        _emit(log, LEDGER_EVENT_QUEUE_PULL, outcome="error",
              reason=f"{type(exc).__name__}: {exc}")
        return None
    if entry is None:
        return None

    try:
        queued_job = queued_entry_to_job(entry)
    except Exception as exc:  # noqa: BLE001 — the entry must not stay claimed by nobody
        reason = f"{type(exc).__name__}: {exc}"
        with contextlib.suppress(_queue.QueueError):
            _queue.fail(entry, reason)
        _emit(log, LEDGER_EVENT_QUEUE_PULL, outcome="failed",
              entry_id=entry.id, reason=reason)
        return QueuePull(entry_id=entry.id, status=QUEUE_PULL_FAILED, reason=reason)

    with contextlib.suppress(_queue.QueueError):
        _queue.complete(entry, str(queued_job.id))
    _emit(log, LEDGER_EVENT_QUEUE_PULL, outcome="planned",
          entry_id=entry.id, job_id=str(queued_job.id))
    return QueuePull(entry_id=entry.id, status=QUEUE_PULL_PLANNED,
                     job_id=str(queued_job.id))


@dataclass(frozen=True)
class CycleLoopResult:
    """What the whole loop did."""

    job: Job
    terminal_status: str
    job_status: str
    stop_reason: str = ""
    cycles: tuple[CycleRecord, ...] = ()
    #: F048: what the idle loop pulled from the queue, if the binding is enabled.
    #: ``None`` whenever it is not — which is the default.
    queue_pull: QueuePull | None = None
    #: F051: decisions still open when the loop ended.  A non-empty tuple with
    #: terminal ``blocked`` is the "the run needs you" case.
    open_decision_ids: tuple[str, ...] = ()
    #: F051: how many times the loop re-checked the awaiting branches — exactly
    #: once per batch boundary.  Asserted in tests: it proves the pickup is a
    #: boundary check and not a polling loop.
    awaiting_checks: int = 0

    @property
    def cycles_run(self) -> int:
        return len(self.cycles)

    def to_json(self) -> dict[str, Any]:
        payload = {
            "job_id": str(self.job.id),
            "terminal_status": self.terminal_status,
            "job_status": self.job_status,
            "stop_reason": self.stop_reason,
            "cycles_run": self.cycles_run,
            "cycles": [c.to_json() for c in self.cycles],
            "open_decision_ids": list(self.open_decision_ids),
            "awaiting_checks": self.awaiting_checks,
        }
        # Only present when something was actually pulled: the default shape of this
        # payload is what every existing reader already parses.
        if self.queue_pull is not None:
            payload["queue_pull"] = self.queue_pull.to_json()
        return payload


# ---------------------------------------------------------------------------
# Default steps (the existing single-task path — nothing new)
# ---------------------------------------------------------------------------


def default_task_step(job: Job, provider_call: ProviderCall,
                      task_id: UUID | None = None) -> TaskAttempt:
    """Run ONE ready task through the existing single-task path.

    run_next_task -> materialize -> verify_task_output -> finalize_task, which
    is exactly what ``remedy job run-next`` does.  Rollback on builder failure
    is ``run_next_task``'s concern; the exception is translated into a failed
    attempt so the conductor can end the cycle and record it.

    *task_id* is the task the DAG ready set selected (F050).  Without it this
    runs whatever task is first PENDING, which is what every caller before
    F050 wanted.
    """
    from packages.orchestration.workspace import LocalWorkspaceRuntime

    try:
        result = run_next_task(job, provider_call, task_id=task_id)
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
# Cycle evidence (T002)
# ---------------------------------------------------------------------------


def cycle_evidence_dir(job_id: str) -> Path:
    """The job's own evidence area, ``cycles/`` subdirectory.

    Built on ``pingpong_job.job_evidence_dir`` so cycle records live exactly
    where every other job-level record lives — no second evidence convention.
    """
    from packages.orchestration.pingpong_job import job_evidence_dir
    from packages.orchestration.safe_points import validate_job_id

    return Path(job_evidence_dir(validate_job_id(job_id))) / CYCLE_EVIDENCE_DIRNAME


def write_cycle_record(job_id: str, record: CycleRecord) -> Path:
    """Append one cycle's summary record.  One cycle, one file, one index.

    Indices are the cycle indices themselves, so N cycles produce exactly N
    files named cycle_0001..cycle_000N — monotonic by construction and
    idempotent under a re-run of the same cycle index.
    """
    directory = cycle_evidence_dir(job_id)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / CYCLE_RECORD_FILENAME.format(index=record.cycle_index)
    payload = dict(record.to_json(), job_id=str(job_id))
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def next_cycle_index(job_id: str) -> int:
    """The number the NEXT cycle of this job must take.

    Cycle numbering belongs to the JOB, not to the process that happens to be
    running it.  A resumed run that started counting at 1 again would write
    ``cycle_0001.json`` and ``checkpoint_0001.json`` straight over the records
    the killed run left — destroying exactly the history F047 exists to
    preserve, and making "each task executed once" unprovable (F047 T003).

    Both evidence areas are consulted, because either can be switched off
    independently: whichever got further wins.
    """
    highest = max((int(r.get("cycle_index", 0)) for r in read_cycle_records(job_id)),
                  default=0)
    try:
        from packages.orchestration.checkpoints import _index_of_path, checkpoint_paths

        highest = max(highest,
                      *(_index_of_path(p) for p in checkpoint_paths(job_id)), 0)
    except Exception:  # noqa: BLE001 — numbering must not depend on checkpoints
        pass
    return highest + 1


def read_cycle_records(job_id: str) -> list[dict[str, Any]]:
    """Every persisted cycle record for a job, in cycle order."""
    directory = cycle_evidence_dir(job_id)
    if not directory.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(directory.glob("cycle_*.json")):
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
    records.sort(key=lambda r: r.get("cycle_index", 0))
    return records


# ---------------------------------------------------------------------------
# Config / flag resolution (T002)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResolvedCycles:
    """How many cycles a run may use, where that came from, and whether the
    rollout cap trimmed it."""

    max_cycles: int
    source: str          # "flag" | "config" | "default" | "experiment"
    requested: int
    capped: bool

    @property
    def cap(self) -> int:
        return CYCLE_SAFETY_CAP

    def to_json(self) -> dict[str, Any]:
        """The record that makes an over-cap run impossible to miss.

        Written into the run's evidence by every caller that resolves cycles,
        so "this run used more than the rollout cap" is a fact on disk rather
        than something a reader has to infer.
        """
        return {"max_cycles": self.max_cycles, "source": self.source,
                "requested": self.requested, "capped": self.capped,
                "cap": self.cap, "over_cap": self.max_cycles > self.cap}


def resolve_max_cycles(flag: int | None = None,
                       config_value: int | None = None,
                       *,
                       experiment_max_cycles: int | None = None) -> ResolvedCycles:
    """Flag beats config beats default — and BOTH are capped.

    The cap is the F046 rollout rule: until the F075 milestone gate raises
    ``CYCLE_SAFETY_CAP``, no configuration and no flag can make Remedy run more
    than one cycle.  The requested value is reported alongside so the caller
    can tell the operator their number was trimmed rather than ignored.

    ``experiment_max_cycles`` is the ONE way past the cap, and it exists for
    exactly one caller: the F075 gauntlet runner (R-0187). The gate cannot
    demonstrate ten flawless multi-cycle missions while every job is wedged at
    one cycle, and the cap's own rule says raising the DEFAULT is the job of
    the human-applied ADR that a passing 10/10 produces — so the CAMPAIGN and
    the DEFAULT are separated here rather than conflated. It is deliberately
    NOT reachable from config or a CLI flag: a caller has to pass it in code,
    by name, and the resulting ``ResolvedCycles`` records ``source
    "experiment"`` with ``over_cap`` true so no run can exceed the cap
    silently. Config and flag clamping below is untouched.
    """
    if experiment_max_cycles is not None:
        requested = int(experiment_max_cycles)
        if requested < 1:
            raise ValueError(f"max_cycles must be >= 1, got {requested}")
        return ResolvedCycles(max_cycles=requested, source="experiment",
                              requested=requested, capped=False)
    if flag is not None:
        requested, source = int(flag), "flag"
    elif config_value is not None:
        requested, source = int(config_value), "config"
    else:
        requested, source = DEFAULT_MAX_CYCLES, "default"
    if requested < 1:
        raise ValueError(f"max_cycles must be >= 1, got {requested}")
    allowed = min(requested, CYCLE_SAFETY_CAP)
    return ResolvedCycles(max_cycles=allowed, source=source,
                          requested=requested, capped=allowed < requested)


def limits_from_config(config: Any = None, *, cycles_flag: int | None = None,
                       experiment_max_cycles: int | None = None
                       ) -> tuple[CycleLimits, ResolvedCycles]:
    """Build ``CycleLimits`` from the resolved Remedy config plus a CLI flag.

    ``experiment_max_cycles`` is passed straight through to
    :func:`resolve_max_cycles`; see there for why it exists and who may use it.
    """
    if config is None:
        from packages.orchestration.config import get_config
        config = get_config()
    resolved = resolve_max_cycles(cycles_flag, config.get(CONFIG_KEY_MAX_CYCLES),
                                  experiment_max_cycles=experiment_max_cycles)
    batch_size = config.get(CONFIG_KEY_BATCH_SIZE) or DEFAULT_BATCH_SIZE
    repair_rounds = config.get(CONFIG_KEY_REPAIR_ROUNDS)
    return (
        CycleLimits(
            max_cycles=resolved.max_cycles,
            batch_size=int(batch_size),
            verify_command=config.get(CONFIG_KEY_VERIFY_COMMAND) or None,
            repair_rounds=(DEFAULT_REPAIR_ROUNDS if repair_rounds is None
                           else int(repair_rounds)),
        ),
        resolved,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ready_tasks(job: Job, batch_size: int, *,
                blocked_ids: Collection[UUID] = (),
                awaiting_ids: Collection[UUID] = ()) -> list[UUID]:
    """The ready batch: the DAG ready set in plan order, capped at batch_size.

    F050: a task is ready when every dependency it declares in its Flight Plan
    metadata is COMPLETED (``dag_schedule.ready_set``); plans without that
    metadata keep behaving linearly, because the legacy rule there is "each
    task depends on its predecessor".  A batch larger than the number of ready
    tasks is fine; the list is simply shorter.

    *blocked_ids* are tasks blocked for this run — an attempt executed and
    failed.  They and their transitive dependents are withheld, so a blocked
    branch locks only its own downstream and independent branches keep running.

    *awaiting_ids* are tasks paused on an OPEN human decision (F051).  They are
    withheld exactly like blocked ids — same branch-local effect — but they are
    a separate argument because they mean something entirely different: nothing
    failed, and the moment the decision is answered they become ready again.
    """
    ready = dag_ready_set(job.tasks)
    withheld_seeds = set(blocked_ids) | set(awaiting_ids)
    if withheld_seeds:
        withheld = withheld_seeds | blocked_downstream(job.tasks, withheld_seeds)
        ready = [task_id for task_id in ready if task_id not in withheld]
    return ready[:batch_size]


def skipped_blocked_tasks(job: Job,
                          blocked_ids: Collection[UUID]) -> list[UUID]:
    """Ids withheld only because something upstream is blocked, in plan order.

    This is what the cycle record names so a report can say WHY nothing
    happened on a branch, rather than leaving a silent gap.
    """
    if not blocked_ids:
        return []
    skipped = blocked_downstream(job.tasks, blocked_ids)
    return [task.id for task in job.tasks if task.id in skipped]


def awaiting_downstream_tasks(job: Job,
                              awaiting_ids: Collection[UUID]) -> list[UUID]:
    """Ids withheld only because something upstream awaits a decision (F051).

    Same traversal as ``skipped_blocked_tasks``, reported under its own name so
    a report can distinguish "waiting for an answer" from "blocked by a
    failure" — for a returning human those are opposite situations.
    """
    return skipped_blocked_tasks(job, awaiting_ids)


def _step_target_argument(step: TaskStep) -> bool:
    """True when *step* accepts the ``task_id`` the ready set selected.

    The task-step seam predates F050 and its callables take ``(job,
    provider_call)``.  Passing a third argument to those would break every
    injected step, so the target is offered only to callables that declare it.
    """
    try:
        return "task_id" in inspect.signature(step).parameters
    except (TypeError, ValueError):  # builtins and other unintrospectables
        return False


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


#: F053 T002: the terminal statuses that end a run and therefore get a final
#: report.  ``max_cycles_reached`` is deliberately absent — it maps to
#: JOB_RUNNING, the job has pending work and simply ran out of cycle budget, so
#: writing a "final" report for it would be a lie about the run being over.
REPORTED_TERMINALS: frozenset[str] = frozenset({
    TERMINAL_ALL_GREEN,
    TERMINAL_STOPPED_BY_OPERATOR,
    TERMINAL_BUDGET_EXHAUSTED,
    TERMINAL_DEADLINE_REACHED,
    TERMINAL_BLOCKED,
})


def _apply_terminal(job: Job, terminal_status: str, stop_reason: str, *,
                    write_report: bool = True) -> str:
    """Write the terminal status onto the job and return the job status.

    This is also the ONE place a final run report is written (F053 T002).
    Every terminal transition passes through here, so hooking the report here
    is what makes "exactly one report per terminal job" true by construction
    rather than by remembering to call a writer on five separate paths.
    The write happens after the terminal metadata is on the job, so the report
    describes the state the job is about to be saved with.
    """
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
    if write_report and terminal_status in REPORTED_TERMINALS:
        from packages.orchestration.run_report import write_final_report

        # Never raises, and records its own failure on the job: a run that
        # finished is finished whether or not its account could be written.
        write_final_report(job)
    return job_status


def _write_cycle_checkpoint(job: Job, record: CycleRecord,
                            limits: CycleLimits, *,
                            blocked_ids: Collection[UUID] = (),
                            awaiting_ids: Collection[UUID] = ()) -> None:
    """Write this cycle's checkpoint (F047).  Never raises into the loop.

    The next intent is derived from what the job still has READY at this
    moment: another cycle with a named first task, or nothing left to run.
    A task blocked in this run is not named as the next intent — resuming into
    a task that just failed would be a retry policy this module does not own.
    A task awaiting a decision is not named either: resuming into it before the
    decision is answered would just escalate again (F051).
    A write that fails is recorded on the job as ``checkpoint_error`` and
    logged by the checkpoint module — the run continues and the next cycle
    retries (feature-file A9).
    """
    from packages.orchestration.checkpoints import (
        INTENT_CYCLE,
        INTENT_NONE,
        record_cycle_checkpoint,
    )

    pending = ready_tasks(job, limits.batch_size, blocked_ids=blocked_ids,
                          awaiting_ids=awaiting_ids)
    next_intent: dict[str, Any] = (
        {"kind": INTENT_CYCLE,
         "cycle_index": record.cycle_index + 1,
         "task_id": str(pending[0])}
        if pending else {"kind": INTENT_NONE}
    )
    _, error = record_cycle_checkpoint(
        str(job.id), record.cycle_index,
        budget_spent_tokens=record.tokens_so_far,
        verify_result=record.verify_result,
        verify_command=limits.verify_command,
        next_intent=next_intent,
    )
    if error:
        job.metadata["checkpoint_error"] = error
    else:
        job.metadata.pop("checkpoint_error", None)


def _open_decision_ids(job: Job) -> tuple[str, ...]:
    """Ids of the job's still-open task decisions, in the order they were raised."""
    from packages.orchestration.escalation import open_task_decisions

    return tuple(str(record.get("decision_id", ""))
                 for record in open_task_decisions(job))


def _escalate_task(job: Job, attempt: TaskAttempt, target: UUID, *,
                   now: datetime, unattended: bool,
                   log: Any = None) -> dict[str, Any]:
    """Enqueue ONE decision for the task that raised ``needs_decision`` (F051).

    Attended runs always ask.  An unattended run applies the decision's safe
    default at once — and only then; a decision with no default waits in both
    modes, because inventing an answer is the one thing escalation exists to
    avoid.  The returned record is the one the cycle names in its evidence.
    """
    from packages.orchestration.escalation import (
        auto_apply_safe_default,
        enqueue_task_decision,
    )

    task_id = attempt.task_id if attempt.task_id is not None else target
    record = enqueue_task_decision(
        job,
        task_id=task_id,
        question=attempt.question,
        options=attempt.options,
        safe_default=attempt.safe_default,
        now=now,
    )
    _emit(log, LEDGER_EVENT_TASK_NEEDS_DECISION,
          task_id=str(task_id),
          decision_id=record["decision_id"],
          question=record["question"],
          options=list(record["options"]),
          safe_default=record["safe_default"])

    if unattended:
        applied = auto_apply_safe_default(job, record, now=now)
        if applied is not None:
            _emit(log, LEDGER_EVENT_DECISION_ANSWERED,
                  task_id=str(task_id),
                  decision_id=record["decision_id"],
                  answer=applied["answer"],
                  answer_source=applied["answer_source"])
    return record


def _emit(log: Any, event: str, **meta: Any) -> None:
    """Emit a ledger event when a writer was injected; never raise into the loop."""
    if log is None:
        return
    try:
        log.log(event, **meta)
    except Exception:  # noqa: BLE001 — a ledger write must not break execution
        pass


# ---------------------------------------------------------------------------
# What a failed verify actually means (F052)
# ---------------------------------------------------------------------------


def as_verify_outcome(value: str | VerifyOutcome) -> VerifyOutcome:
    """Normalize whatever a verify step returned.

    Every verify step written before F052 returns a bare VERIFY_* string, and
    they must all keep working untouched — so the richer shape is accepted, not
    required.
    """
    if isinstance(value, VerifyOutcome):
        return value
    return VerifyOutcome(result=str(value))


def cycle_verify_failure_class(verify_result: str) -> str:
    """Classify a non-passing verify through the EXISTING classifier (F010).

    No second vocabulary and no second enum: a failed test is the classifier's
    ``test_failed``, a verify step that could not run at all is its ``config``,
    and anything else is honestly ``unknown``.  A passing or never-run verify has
    no failure class — an empty string, not a guess.
    """
    from packages.orchestration.failure_postmortem import FailureSignals, classify

    if verify_result in (VERIFY_PASSED, VERIFY_NOT_RUN, ""):
        return ""
    if verify_result == VERIFY_FAILED:
        signals = FailureSignals(terminal_status="test_failed")
    elif verify_result == VERIFY_CONFIG_ERROR:
        signals = FailureSignals(error_class="config")
    else:
        signals = FailureSignals(error_text=verify_result)
    return classify(signals).failure_class.value


def render_cycle_summary_line(record: CycleRecord) -> str:
    """One human-readable line per cycle, for status and report renderings.

    A cycle that did not verify says WHY in the same breath: "verify=failed"
    alone sends a reader to the logs, "failure_class=config" sends them to the
    harness instead of to a test they were never going to fix.  A cycle that
    only went green because repair rounds fixed it says THAT too — silent
    healing hides risk (F052).
    """
    line = (f"cycle {record.cycle_index}: verify={record.verify_result} "
            f"tasks={record.tasks_completed}/{record.tasks_attempted}")
    if record.repair_summary:
        line += f" | {record.repair_summary}"
    if record.verify_failure_class:
        line += f" | failure_class={record.verify_failure_class}"
    return line


# ---------------------------------------------------------------------------
# Self-healing test rounds (F052)
# ---------------------------------------------------------------------------


def build_cycle_repair_findings(job: Job, cycle_index: int,
                                outcome: VerifyOutcome,
                                *, executed_task_ids: Collection[str] = (),
                                round_number: int = 1) -> dict[str, Any]:
    """The findings payload ONE repair round is given.

    Built on the EXISTING repair-context builder
    (``repair_context.build_repair_context``), so a repair round receives
    findings in exactly the shape the repair loop already consumes.  F052 adds
    only what a cycle knows and a task-level failure did not: which test ids
    failed, the tail of the failure text, and the files this cycle changed as a
    hint.

    No raw stdout beyond the tail the verify step already bounded — that is the
    repair-context module's rule, and it is kept here.
    """
    from packages.orchestration.repair_context import build_repair_context

    test_event = {"metadata": {"exit_code": 1, "passed": False,
                               "cycle": cycle_index}}
    findings = build_repair_context(job.id, test_event, [])
    findings.update({
        "source": "cycle_verify",
        "cycle_index": cycle_index,
        "repair_round": round_number,
        "failing_test_ids": list(outcome.failing_test_ids),
        "failure_tail": outcome.output,
        "changed_files": list(outcome.changed_files) or list(executed_task_ids),
    })
    return findings


def default_repair_step(job: Job, cycle_index: int, findings: dict[str, Any],
                        *, provider_call: ProviderCall) -> RepairOutcome:
    """ONE repair round, run through the EXISTING bounded repair loop.

    F052 adds no repair mechanism of its own (feature file A6): this hands the
    findings to ``builder_bridge.run_builder_bridge_loop`` — the loop that
    already turns a builder output into a parsed patch, an approved intent, an
    apply and a test — with ``max_cycles=1``, because the ROUND CAP belongs to
    the cycle (``cycles.repair_rounds``) and the cycle re-runs its own verify
    after every round.

    The provider call is the cycle's OWN counted seam, so a repair round is
    counted by the budgets and stopped by the safe points exactly like any other
    provider work.  When the repair loop is not reachable in this deployment the
    round honestly did not run: nothing is counted and nothing is claimed.
    """
    from packages.orchestration.builder_bridge import run_builder_bridge_loop
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.workspace import LocalWorkspaceRuntime

    task = next((t for t in job.tasks if t.status != RunState.COMPLETED),
                job.tasks[0] if job.tasks else None)
    if task is None:
        return RepairOutcome(ran=False, error="repair_no_task")

    def build_fn(repair_context: dict[str, Any] | None) -> BuilderOutput:
        return provider_call(TaskExecutionContext(
            job_id=job.id,
            job_prompt=job.user_prompt,
            task_id=task.id,
            task_type=task.inputs.get("task_type", "unknown"),
            task_description=task.description,
            prior_task_summaries=[json.dumps(repair_context or findings,
                                             sort_keys=True)],
        ))

    try:
        repo_path = LocalWorkspaceRuntime(job_id=job.id).workspace.root
        loop = run_builder_bridge_loop(
            build_fn, repo_path,
            job=job, data_dir=resolve_data_root(), max_cycles=1,
        )
    except Exception as exc:  # noqa: BLE001 — an unreachable repair path is not a crash
        return RepairOutcome(ran=False, error=f"{type(exc).__name__}: {exc}")

    changed: tuple[str, ...] = ()
    parse = getattr(loop.final_result, "parse_result", None)
    if parse is not None:
        changed = tuple(getattr(parse, "target_paths", ()) or ())
    return RepairOutcome(ran=loop.cycles_run > 0, changed_files=changed,
                         stop_reason=loop.stop_reason)


@dataclass(frozen=True)
class RepairPhase:
    """What the whole repair phase of ONE cycle did."""

    outcome: VerifyOutcome
    rounds_used: int = 0
    healed: bool = False
    healed_without_changes: bool = False
    errors: tuple[str, ...] = ()
    #: The stop observed BETWEEN two rounds, if one was.  The cycle still
    #: records everything it already did; the loop then terminates on it.
    stop: Any = None

    @property
    def summary(self) -> str:
        """The one line the evidence and every report carry."""
        if self.rounds_used == 0:
            return ""
        rounds = (f"{self.rounds_used} repair round"
                  + ("" if self.rounds_used == 1 else "s"))
        if self.healed and self.healed_without_changes:
            return f"healed without changes (flaky?) after {rounds}"
        if self.healed:
            return f"healed after {rounds}"
        return f"not healed after {rounds}"


def _run_repair_rounds(job: Job, cycle_index: int, outcome: VerifyOutcome, *,
                       limits: CycleLimits,
                       verify_step: VerifyStep,
                       repair_step: RepairStep,
                       stop_probe: Callable[[], Any],
                       executed_ids: Collection[str] = (),
                       log: Any = None) -> RepairPhase:
    """Up to ``limits.repair_rounds`` bounded repair rounds on a FAILED verify.

    Every rule here comes from the feature file:

    * only a FAILED verify is repaired — a missing command or a bad config is
      classified and left alone (A9);
    * the verify step re-runs after EVERY round, so "healed" always means the
      real verify passed, never that a repair round claimed success;
    * the cap is exact — a round that did not run is not counted, so "exactly
      two rounds" stays provable;
    * a stop request is honored BETWEEN rounds, at the same safe point the cycle
      loop itself uses.  A round already in flight is never interrupted.
    """
    if outcome.result not in _VERIFY_REPAIRABLE or limits.repair_rounds <= 0:
        return RepairPhase(outcome=outcome)

    errors: list[str] = []
    rounds = 0
    while rounds < limits.repair_rounds:
        stop = stop_probe()
        if stop is not None and getattr(stop, "should_stop", False):
            return RepairPhase(outcome=outcome, rounds_used=rounds,
                               errors=tuple(errors), stop=stop)

        findings = build_cycle_repair_findings(
            job, cycle_index, outcome,
            executed_task_ids=executed_ids, round_number=rounds + 1)
        repair = repair_step(job, cycle_index, findings)
        if not repair.ran:
            if repair.error:
                errors.append(f"repair_not_run: {repair.error}")
            break

        rounds += 1
        _emit(log, LEDGER_EVENT_CYCLE_REPAIR_ROUND,
              cycle_index=cycle_index, repair_round=rounds,
              failing_test_ids=list(outcome.failing_test_ids),
              changed_files=list(repair.changed_files),
              stop_reason=repair.stop_reason)

        outcome = as_verify_outcome(
            verify_step(job, cycle_index, limits.verify_command))
        if outcome.result == VERIFY_PASSED:
            phase = RepairPhase(outcome=outcome, rounds_used=rounds, healed=True,
                                healed_without_changes=not repair.changed_files,
                                errors=tuple(errors))
            _emit(log, LEDGER_EVENT_CYCLE_HEALED,
                  cycle_index=cycle_index, repair_rounds_used=rounds,
                  healed_without_changes=phase.healed_without_changes,
                  summary=phase.summary)
            return phase

    return RepairPhase(outcome=outcome, rounds_used=rounds, errors=tuple(errors))


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
    repair: RepairStep | None = None,
    clock: Callable[[], datetime] | None = None,
    save: Callable[[Job], None] | None = None,
    log: Any = None,
    control_root_path: Any = None,
    record_evidence: bool = True,
    record_checkpoint: bool = True,
    first_cycle_index: int | None = None,
    unattended: bool = False,
) -> CycleLoopResult:
    """Run bounded cycles over *job* until a terminal condition.

    One cycle is: safe point -> ready batch -> execute -> verify -> persist.
    The safe point is evaluated BEFORE any work of a cycle begins, so a cycle
    never starts after should_stop says stop.

    Seams (all default to the existing production path):
      task_step  one ready task through run_next_task + verify + finalize
      verify     the per-cycle verify step; the default runs nothing and
                 records ``not_run``
      repair     ONE repair round for a FAILED verify (F052); the default runs
                 the existing bounded repair loop through the counted provider
                 seam
      clock      the only source of "now" — the loop never sleeps
      save       ``storage.save_job``
      log        anything with ``.log(event, **meta)`` (a RunLogWriter); when
                 omitted, no ledger events are emitted

``record_evidence`` writes one summary record per cycle under the job's own
evidence area (N cycles -> exactly N records, monotonically indexed).  An
evidence write that fails is recorded on the job as ``cycle_evidence_error``
and never aborts execution that already happened.

``record_checkpoint`` writes this cycle's F047 checkpoint next to those
records, AFTER the job snapshot is persisted (a checkpoint references that
snapshot).  A checkpoint write that fails is recorded as ``checkpoint_error``
and never aborts the run either — the next cycle retries.

``first_cycle_index`` is the number the first cycle of THIS invocation takes.
It defaults to one past whatever this job already recorded, so a resumed run
continues the job's numbering instead of overwriting the records the previous
process left (F047).  ``max_cycles`` still bounds this invocation only.

    A failed verify spends up to ``limits.repair_rounds`` bounded repair rounds
    before the cycle keeps its failure (F052): every round runs through the
    existing repair loop on the counted provider seam, the verify step re-runs
    after each one, and a heal is recorded loudly instead of being implied by a
    green cycle.  A verify that failed for a non-test reason is classified and
    never repaired.  A task step that fails ends the cycle too — the task runner has already rolled the task back
    to PENDING, so the next cycle (if the budget allows one) retries it.

    ``unattended`` (F051) decides what a safe default is worth.  Attended (the
    default): a task raising ``needs_decision`` always ASKS — the decision is
    enqueued and its branch waits, default or not.  Unattended: a decision that
    carries a safe default is answered from that default immediately, recorded
    as ``answer_source="default"`` in the escalation assumption log, and the
    branch continues in the same cycle.  A decision without a default waits
    either way — Remedy never invents an answer it was not given.
    """
    step = task_step or default_task_step
    verify_step = verify or _no_verify
    now_fn = clock or (lambda: datetime.now(timezone.utc))
    save_fn = save or _save_job

    base_index = (next_cycle_index(str(job.id)) if first_cycle_index is None
                  else int(first_cycle_index))
    loop_started_at = now_fn()
    provider_calls = 0
    cycles: list[CycleRecord] = []
    last_verify = VERIFY_NOT_RUN
    #: F050 in-run blocked tracking.  A task failure rolls the task back to
    #: PENDING (there is no persistent task-level FAILED), so only this loop
    #: knows which attempts it made and lost.  Ids accumulate for the whole
    #: run: a branch that failed stays blocked until a new run retries it.
    blocked_ids: set[UUID] = set()
    #: F051 awaiting tracking.  DERIVED from the job's open escalation records
    #: at every batch boundary, never stored twice: answering a decision removes
    #: the task from this set with no bookkeeping here, which is exactly how an
    #: answered branch gets picked up mid-run.
    awaiting_ids: set[UUID] = set()
    awaiting_checks = 0
    step_takes_target = _step_target_argument(task_step or default_task_step)

    def counted_provider_call(context: TaskExecutionContext) -> BuilderOutput:
        nonlocal provider_calls
        provider_calls += 1
        return provider_call(context)

    #: F052: a repair round IS provider work, so it runs through the same counted
    #: seam — its cost lands on the job's budget with no separate accounting.
    repair_step: RepairStep = repair or (
        lambda j, idx, findings: default_repair_step(
            j, idx, findings, provider_call=counted_provider_call))

    def repair_stop_probe() -> Any:
        """The safe point BETWEEN two repair rounds — the same evaluation the
        cycle loop makes, so a stop is honored identically wherever it lands."""
        at = now_fn()
        return _should_stop(
            str(job.id),
            budgets=limits.budgets,
            counters=_default_counters(
                job, now=at, started_at=loop_started_at,
                provider_calls=provider_calls),
            now=at,
            control_root_path=control_root_path,
        )

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

        # 2. Batch boundary (F051): re-check which branches still await a
        #    decision.  An answered decision has disappeared from the job's open
        #    records, so its branch becomes ready again right here — exactly one
        #    check per boundary, no sleeping and no polling loop anywhere.
        awaiting_checks += 1
        awaiting_ids = awaiting_decision_task_ids(job)

        # 3. Terminal by job shape: green, or nothing ready and not green.
        batch = ready_tasks(job, limits.batch_size, blocked_ids=blocked_ids,
                            awaiting_ids=awaiting_ids)
        if not batch:
            if _is_green(job, last_verify):
                terminal, stop_reason = TERMINAL_ALL_GREEN, ""
            elif awaiting_ids:
                # Nothing has failed — the run needs an answer.  ``blocked``
                # maps to PAUSED, so answering and resuming finishes the rest.
                terminal = TERMINAL_BLOCKED
                stop_reason = (
                    "awaiting_decision; open_decisions="
                    + ",".join(_open_decision_ids(job))
                )
            else:
                terminal = TERMINAL_BLOCKED
                stop_reason = (
                    "no_tasks" if not job.tasks
                    else f"no_ready_tasks; last_verify={last_verify}"
                )
            break

        # 4. Cycle budget.  Not a stop cause — pending work simply remains.
        if len(cycles) >= limits.max_cycles:
            terminal, stop_reason = TERMINAL_MAX_CYCLES_REACHED, ""
            break

        # 5. Run the cycle.
        cycle_index = base_index + len(cycles)
        started_at = now
        attempted = completed = failed = escalated = 0
        errors: list[str] = []
        executed_ids: list[str] = []
        raised_decision_ids: list[str] = []

        # The ready set is recomputed after EVERY task end (F050), so a task
        # that completes mid-cycle can release its dependents immediately and a
        # task that fails withholds its downstream from the rest of this cycle.
        # The batch is a CAP on how many tasks this cycle may run, unchanged.
        for _ in range(limits.batch_size):
            ready_now = ready_tasks(job, limits.batch_size,
                                    blocked_ids=blocked_ids,
                                    awaiting_ids=awaiting_ids)
            if not ready_now:
                break                      # nothing ready any more
            target = ready_now[0]
            attempt = (step(job, counted_provider_call, target)
                       if step_takes_target else step(job, counted_provider_call))
            # F051: a question, not a failure.  One decision is enqueued for
            # this task, its branch pauses, and the loop carries straight on to
            # whatever else is ready — including tasks on disjoint branches of
            # this very cycle.
            if attempt.needs_decision:
                attempted += 1
                escalated += 1
                record = _escalate_task(
                    job, attempt, target,
                    now=now_fn(), unattended=unattended, log=log)
                raised_decision_ids.append(str(record.get("decision_id", "")))
                awaiting_ids = awaiting_decision_task_ids(job)
                continue
            if not attempt.executed and not attempt.error:
                break                      # nothing ready any more; not an attempt
            attempted += 1
            if attempt.executed and attempt.task_id is not None:
                executed_ids.append(str(attempt.task_id))
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
            # F050: this attempt executed and lost, so it blocks its own
            # transitive downstream for the rest of the run — and nothing else.
            blocked_ids.add(attempt.task_id if attempt.task_id is not None
                            else target)
            break

        verify_outcome = as_verify_outcome(
            verify_step(job, cycle_index, limits.verify_command))

        # F052 self-healing.  Only a FAILED verify is repairable; everything else
        # that denies green is classified and kept.  The phase re-runs the verify
        # step itself, so the outcome it returns is always the LAST real one.
        phase = _run_repair_rounds(
            job, cycle_index, verify_outcome,
            limits=limits, verify_step=verify_step, repair_step=repair_step,
            stop_probe=repair_stop_probe,
            executed_ids=executed_ids, log=log)
        verify_outcome = phase.outcome
        last_verify = verify_outcome.result
        if last_verify == VERIFY_FAILED:
            errors.append("verify_failed")
        errors.extend(phase.errors)

        ended_at = now_fn()
        counters = _default_counters(
            job, now=ended_at, started_at=loop_started_at,
            provider_calls=provider_calls)
        record = CycleRecord(
            cycle_index=cycle_index,
            tasks_attempted=attempted,
            tasks_completed=completed,
            tasks_failed=failed,
            tasks_escalated=escalated,
            verify_result=last_verify,
            tokens_so_far=counters.measured_token_total,
            started_at=started_at.isoformat(),
            ended_at=ended_at.isoformat(),
            verify_command=limits.verify_command,
            errors=tuple(errors),
            executed_task_ids=tuple(executed_ids),
            skipped_blocked_task_ids=tuple(
                str(task_id) for task_id in skipped_blocked_tasks(job, blocked_ids)),
            awaiting_task_ids=tuple(
                str(task.id) for task in job.tasks if task.id in awaiting_ids),
            awaiting_downstream_task_ids=tuple(
                str(task_id)
                for task_id in awaiting_downstream_tasks(job, awaiting_ids)),
            open_decision_ids=tuple(raised_decision_ids),
            verify_failure_class=cycle_verify_failure_class(last_verify),
            repair_rounds_used=phase.rounds_used,
            healed_after_repair=phase.healed,
            healed_without_changes=phase.healed_without_changes,
            repair_summary=phase.summary,
        )
        cycles.append(record)

        # 6. Persist the job, then the cycle's own evidence record, then the
        #    checkpoint (F047).  Order matters: a checkpoint references the
        #    persisted snapshot, so the snapshot must already be on disk.
        save_fn(job)
        if record_evidence:
            try:
                write_cycle_record(str(job.id), record)
            except (OSError, ValueError) as exc:
                job.metadata["cycle_evidence_error"] = f"{type(exc).__name__}: {exc}"
        if record_checkpoint:
            _write_cycle_checkpoint(job, record, limits, blocked_ids=blocked_ids,
                                    awaiting_ids=awaiting_ids)
        _emit(log, LEDGER_EVENT_CYCLE_COMPLETED, **record.to_json())

        # F052: a stop observed BETWEEN two repair rounds ends the run — but only
        # after this cycle's evidence is on disk.  The rounds already spent are
        # part of that record, so a returning human can see what the stop cut off.
        if phase.stop is not None:
            terminal = _terminal_from_stop(phase.stop.reason, phase.stop.source)
            stop_reason = phase.stop.reason
            break

    job_status = _apply_terminal(job, terminal, stop_reason)
    save_fn(job)
    open_decisions = _open_decision_ids(job)
    _emit(
        log, LEDGER_EVENT_LOOP_TERMINAL,
        terminal_status=terminal, job_status=job_status,
        stop_reason=stop_reason, cycles_run=len(cycles),
        open_decision_ids=list(open_decisions),
    )
    return CycleLoopResult(
        job=job,
        terminal_status=terminal,
        job_status=job_status,
        stop_reason=stop_reason,
        cycles=tuple(cycles),
        queue_pull=_pull_queue_when_idle(job, terminal, log=log),
        open_decision_ids=open_decisions,
        awaiting_checks=awaiting_checks,
    )
