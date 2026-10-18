"""R-1351: a job's required project tests run inside its last task's loop, so a red run gets one repair.

On 2026-10-18 a local model's builder imported `strictEqual` from `node:test`, the reviewer passed
the diff, and the job's DoD then ran the real `npm test`, which failed. The job ended `blocked`, which
was true, but the failing test's own diagnostic never reached a model: the DoD gate runs after every
task has passed, and a `remedy do` job's task loop had no test command at all.

This module closes that gap at the loop's own test phase, which already orders Builder → tests →
Reviewer → repair, counts repair rounds and stops at safe points:

* `final_task_test_command` hands the job's LAST task its BLOCKING DoD test checks as the loop's test
  command (`DoDTestCommand`). They run through `dod_runners.run_check` in the job's worktree, which is
  that task's staging, so the loop runs exactly the command, environment and refusals the DoD gate
  runs afterwards. Earlier tasks get none: a multi-task job's tests may be red until its last task.
  An operator's explicit `--test-command` is kept as it is.
* A check that never started (sandbox refusal, missing tool, executable not allowed, a test command
  the job itself changed, no test command) reads `None` with its reason and is no evidence for a
  repair: the reviewer still runs and the DoD gate still reports it `not run`.
* A red run's diagnostic (the error and assertion lines, then the last lines, with the worktree's
  host path removed) is the round's test summary, so the reviewer reads it and a repair round's
  builder gets it under "Test Result" beside a `test-failure` finding (`with_test_failure_finding`),
  even when the reviewer itself found nothing.
* `review_test_evidence` turns a repair decision into a stop when the run is red with the same
  diagnostic as the round before (an unchanged failure is never fed twice), or when the job's
  remaining budget cannot pay one more round (`repair_round_affordable`).

Remedy deliberately does not start another job to run tests, retry a red run without a repair in
between, or treat a non-blocking red check as a reason to repair: such a check was not asked for and
may be red before the change.
"""
from __future__ import annotations

import hashlib
import re
from collections.abc import Callable, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

#: DoD check kinds that run the project's tests (the same set `order_verification` reads).
TEST_CHECK_KINDS = frozenset({"project_tests", "pytest"})
#: The id of the finding a red run adds to a repair round's findings.
TEST_FAILURE_FINDING_ID = "test-failure"
#: Repair-decision reasons this module writes, beside `pingpong_loop.make_repair_decision`'s own.
REASON_TEST_FAILURE_UNCHANGED = "test_failure_unchanged"
REASON_REPAIR_BUDGET_INSUFFICIENT = "test_failed_repair_budget_insufficient"
#: A repair round is one builder and one reviewer call.
PROVIDER_CALLS_PER_ROUND = 2

#: Lines of a test run's output that name what failed, across node:test, jest, vitest, pytest, go and cargo.
_DIAGNOSTIC_LINE = re.compile(
    r"error|assert|expected|received|actual|traceback|\bfail|not ok|✖|✗|panic|"
    r"cannot find|does not provide|undefined|^\s*E\s{2,}|^\s*>\s", re.IGNORECASE)
#: Volatile text a re-run changes although the failure did not: durations and timestamps.
_VOLATILE = re.compile(r"duration_ms\S*\s*[\d.]+|\d+(?:\.\d+)?\s*(?:ms|s)\b|\d{2}:\d{2}:\d{2}(?:\.\d+)?")
MAX_DIAGNOSTIC_LINES = 30
DIAGNOSTIC_CONTEXT_LINES = 3
MAX_TAIL_LINES = 8
MAX_LINE_CHARS = 300
MAX_DIAGNOSTIC_CHARS = 4000


def red_test_diagnostic(output: str, root: Path | str | None = None) -> str:
    """The lines of *output* a repair needs: the failing ones first, then the last ones.

    The worktree's host path (*root*) is removed, so the text names files as the repository does.
    """
    text = output
    if root:
        for prefix in (f"file://{root}/", f"{root}/"):
            text = text.replace(prefix, "")
    lines = [line.rstrip()[:MAX_LINE_CHARS] for line in text.splitlines() if line.strip()]
    # Each failing line with the three before it: a runner prints the failing location and source line there.
    hits = [i for i, line in enumerate(lines) if _DIAGNOSTIC_LINE.search(line)]
    near = sorted({j for i in hits for j in range(max(i - DIAGNOSTIC_CONTEXT_LINES, 0), i + 1)})
    failing = list(dict.fromkeys(lines[j] for j in near))[:MAX_DIAGNOSTIC_LINES]
    tail = [line for line in lines[-MAX_TAIL_LINES:] if line not in failing]
    parts = failing + (["--- last lines ---", *tail] if tail else [])
    return "\n".join(parts)[:MAX_DIAGNOSTIC_CHARS]


def red_test_fingerprint(summary: str) -> str:
    """A digest of a red run's diagnostic without its durations, so a re-run of one failure matches."""
    head = summary.split("--- last lines ---", 1)[0]
    return hashlib.sha256(_VOLATILE.sub("", head).encode()).hexdigest()[:16]


class DoDTestCommand(str):
    """The loop's test command when it is the job's blocking DoD test checks.

    A `str` whose value names the checks, so every reader of a run's `test_command` (the record, the
    report) keeps working; `pingpong_loop._run_test_command` runs it through `run_in`.
    """

    checks: tuple[Any, ...]
    budget_probe: Callable[[int], bool] | None

    def __new__(cls, checks: Sequence[Any], budget_probe: Callable[[int], bool] | None = None) -> DoDTestCommand:
        value = "the job's required project tests (" + ", ".join(c.id for c in checks) + ")"
        made = super().__new__(cls, value)
        made.checks = tuple(checks)
        made.budget_probe = budget_probe
        return made

    # A copy is the same command; it must never degrade to a plain string a shell would split and run.
    def __copy__(self) -> DoDTestCommand:
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> DoDTestCommand:
        return self

    def __reduce__(self) -> tuple[Any, ...]:
        raise TypeError("a DoDTestCommand runs checks of this process's job; it is not pickled")

    def run_in(self, staging: Path) -> tuple[bool | None, str, str]:
        """(passed, summary, tripped): True all green, False one ran red, None one never started."""
        from packages.orchestration.dod_runners import REASON_NONZERO_EXIT, run_check

        red: list[str] = []
        for check in self.checks:
            ev = run_check(check, staging)
            if ev.green:
                continue
            if ev.reason != REASON_NONZERO_EXIT or ev.exit_code in (None, 126, 127):
                # Nothing was judged: the reviewer runs on, and the DoD gate reports it not run.
                detail = red_test_diagnostic(ev.output_tail, staging.resolve())[-600:]
                return None, f"tests_not_run: {ev.reason or f'exit {ev.exit_code}'}: {detail}", ""
            red.append(f"{ev.command or check.id} exited {ev.exit_code}:\n"
                       f"{red_test_diagnostic(ev.output_tail, staging.resolve())}")
        if red:
            return False, "\n\n".join(red), ""
        return True, "passed: " + ", ".join(c.id for c in self.checks), ""


def final_task_test_command(job: Any, task: Any, test_command: str | None,
                            counters_fn: Callable[[], Any] | None = None) -> str | None:
    """The test command *task*'s loop runs: the operator's, else the job's blocking DoD test checks
    when *task* is the job's last one, else none (see the module text)."""
    if test_command:
        return test_command
    from packages.orchestration.dod_gate import load_dod
    from packages.orchestration.pingpong_job import TASK_PENDING, TASK_RUNNING

    if any(t is not task and t.status in (TASK_PENDING, TASK_RUNNING) for t in job.tasks):
        return test_command
    dod = load_dod(str(job.job_id))
    checks = [c for c in (dod.checks if dod is not None else []) if c.blocking and c.kind in TEST_CHECK_KINDS]
    if not checks:
        return test_command
    probe = None
    if counters_fn is not None and getattr(job, "budgets", None):
        from packages.core.models import JobBudgets

        probe = _budget_probe(JobBudgets.model_validate(job.budgets), counters_fn)
    return DoDTestCommand(checks, probe)


def _budget_probe(budgets: Any, counters_fn: Callable[[], Any]) -> Callable[[int], bool]:
    """A probe answering whether one more round fits the job's remaining budget, after *rounds* rounds."""
    start = counters_fn()

    def affordable(rounds: int) -> bool:
        return repair_round_affordable(budgets, start, counters_fn(), rounds)
    return affordable


def repair_round_affordable(budgets: Any, start: Any, now: Any, rounds: int,
                            *, at: datetime | None = None) -> bool:
    """Whether the job's remaining budget pays one more round of this loop.

    A round costs two provider calls, and as many tokens and seconds as this loop's rounds have
    cost on average so far (from *start*, the counters when the loop began, to *now*). A limit
    the job does not set never refuses.
    """
    rounds = max(rounds, 1)
    if budgets.max_provider_calls is not None:
        if budgets.max_provider_calls - now.provider_calls < PROVIDER_CALLS_PER_ROUND:
            return False
    if budgets.max_total_tokens is not None:
        per_round = (now.measured_token_total - start.measured_token_total) / rounds
        if budgets.max_total_tokens - now.measured_token_total < per_round:
            return False
    per_round_s = (now.elapsed_seconds - start.elapsed_seconds) / rounds
    if budgets.max_wall_clock_minutes is not None:
        if budgets.max_wall_clock_minutes * 60 - now.elapsed_seconds < per_round_s:
            return False
    if budgets.deadline is not None:
        left = (budgets.deadline - (at or datetime.now(timezone.utc))).total_seconds()
        if left < per_round_s:
            return False
    return True


def with_test_failure_finding(findings: list[Any], rd: Any) -> list[Any]:
    """*findings*, plus one naming the red test run when the round's tests ran and failed.

    A repair round's builder reads the run's diagnostic under "Test Result" only beside a finding,
    so a reviewer that passed a diff whose tests are red would otherwise send it a repair round
    holding no evidence at all.
    """
    if rd.test_passed is not False or any(f.id == TEST_FAILURE_FINDING_ID for f in findings):
        return findings
    from packages.orchestration.pingpong_provider import ReviewFinding

    return [*findings, ReviewFinding(
        id=TEST_FAILURE_FINDING_ID, severity="high",
        summary="The project's tests fail on this change; the test result below shows the failure.",
        required_fix="Change the code or the test the failure names so the project's tests pass. "
                     "Do not delete or weaken a test to make it pass.")]


def review_test_evidence(decision: Any, rd: Any, rounds: Sequence[Any], test_command: str) -> Any:
    """*decision*, turned into a stop when a repair from red tests would be pointless or unpaid."""
    if decision.repair_decision != "repair" or rd.test_passed is not False:
        return decision
    earlier = [r for r in rounds if r is not rd]
    if earlier and earlier[-1].test_passed is False and (
            red_test_fingerprint(earlier[-1].test_summary) == red_test_fingerprint(rd.test_summary)):
        decision.repair_decision, decision.reason = "stop_exhausted", REASON_TEST_FAILURE_UNCHANGED
    elif getattr(test_command, "budget_probe", None) is not None and not test_command.budget_probe(len(rounds)):
        decision.repair_decision, decision.reason = "stop_exhausted", REASON_REPAIR_BUDGET_INSUFFICIENT
    return decision
