"""R-1351: the units of `packages/orchestration/verified_repair.py`.

The walk through a real `remedy do` with a real `npm test` is `tests/cli/test_do_verified_repair.py`;
these pin the pieces it is made of: the diagnostic, the fingerprint, the budget arithmetic, the
finding a red run adds, the decision it may turn into a stop, and which task gets the checks.
"""
from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.pingpong_loop import PingPongRound, RepairDecision, make_repair_decision
from packages.orchestration.pingpong_provider import ReviewFinding
from packages.orchestration.verified_repair import (
    REASON_REPAIR_BUDGET_INSUFFICIENT,
    REASON_TEST_FAILURE_UNCHANGED,
    TEST_FAILURE_FINDING_ID,
    DoDTestCommand,
    final_task_test_command,
    red_test_diagnostic,
    red_test_fingerprint,
    repair_round_affordable,
    review_test_evidence,
    with_test_failure_finding,
)

NODE_OUTPUT = """> test
> node --test

TAP version 13
ok 1 - baseline
  duration_ms: 0.761056
# file:///work/.remedy-wt/job-1/test/calc.test.js:1
# import { test, strictEqual } from "node:test";
#                ^^^^^^^^^^^
# SyntaxError: The requested module 'node:test' does not provide an export named 'strictEqual'
#     at ModuleJob._instantiate (node:internal/modules/esm/module_job:226:21)
not ok 2 - test/calc.test.js
  duration_ms: 74.573
# tests 2
# pass 1
# fail 1
# duration_ms 124.411767
"""
PYTEST_OUTPUT = """tests/test_add.py F                                                      [100%]
    def test_add():
>       assert add(1, 1) == 2
E       assert 0 == 2
FAILED tests/test_add.py::test_add - assert 0 == 2
1 failed in 0.03s
"""


def test_the_diagnostic_keeps_the_failing_lines_and_the_offending_source_line_without_host_paths():
    text = red_test_diagnostic(NODE_OUTPUT, "/work/.remedy-wt/job-1")

    assert "does not provide an export named 'strictEqual'" in text
    assert 'import { test, strictEqual } from "node:test";' in text     # the line before the error
    assert "not ok 2 - test/calc.test.js" in text
    assert "/work/.remedy-wt" not in text and "# test/calc.test.js:1" in text
    assert text.index("SyntaxError") < text.index("--- last lines ---")


def test_the_diagnostic_reads_a_pytest_assertion():
    text = red_test_diagnostic(PYTEST_OUTPUT)

    assert ">       assert add(1, 1) == 2" in text and "E       assert 0 == 2" in text


def test_a_rerun_of_the_same_failure_has_the_same_fingerprint_and_another_failure_does_not():
    again = NODE_OUTPUT.replace("74.573", "81.002").replace("124.411767", "131.5").replace("0.761056", "0.9")
    other = NODE_OUTPUT.replace("strictEqual", "deepEqual")

    first = red_test_fingerprint(red_test_diagnostic(NODE_OUTPUT))
    assert red_test_fingerprint(red_test_diagnostic(again)) == first
    assert red_test_fingerprint(red_test_diagnostic(other)) != first


def _counters(calls: int = 0, tokens: int = 0, seconds: float = 0.0) -> BudgetCounters:
    return BudgetCounters(provider_calls=calls, measured_token_total=tokens, measured_call_count=calls,
                          elapsed_seconds=seconds, actual_sources=("pingpong_live",) if calls else ())


@pytest.mark.parametrize(("budgets", "now", "affordable"), [
    ({}, _counters(50, 10**6, 9999), True),                                     # no limit never refuses
    ({"max_provider_calls": 4}, _counters(2), True),                            # two calls left: one round
    ({"max_provider_calls": 3}, _counters(2), False),                           # one call left: no round
    ({"max_total_tokens": 30_000}, _counters(2, 18_000), True),                 # 12,000 left, a round cost 9,000
    ({"max_total_tokens": 25_000}, _counters(2, 18_000), False),                # 7,000 left
    ({"max_wall_clock_minutes": 2}, _counters(2, 0, 60.0), True),               # 60 s left, a round took 30 s
    ({"max_wall_clock_minutes": 1}, _counters(2, 0, 50.0), False),              # 10 s left, a round took 25 s
], ids=["no-limits", "calls-enough", "calls-short", "tokens-enough", "tokens-short", "time-enough", "time-short"])
def test_a_repair_round_must_fit_the_remaining_budget(budgets, now, affordable):
    assert repair_round_affordable(JobBudgets(**budgets), _counters(), now, rounds=2) is affordable


def test_a_deadline_closer_than_one_round_refuses_it():
    at = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
    budgets = JobBudgets(deadline=at + timedelta(seconds=10))

    assert repair_round_affordable(budgets, _counters(), _counters(2, 0, 40.0), 1, at=at) is False
    assert repair_round_affordable(budgets, _counters(), _counters(2, 0, 4.0), 1, at=at) is True


def _round(passed: bool | None, summary: str = "") -> PingPongRound:
    return PingPongRound(round_number=1, test_passed=passed, test_summary=summary)


def test_a_red_run_adds_one_test_failure_finding_and_nothing_else_does():
    reviewer_finding = ReviewFinding(id="F1", summary="naming")

    added = with_test_failure_finding([reviewer_finding], _round(False, "x"))
    assert [f.id for f in added] == ["F1", TEST_FAILURE_FINDING_ID]
    assert with_test_failure_finding(added, _round(False, "x")) == added           # never twice
    assert with_test_failure_finding([], _round(None, "tests_not_run: x")) == []   # nothing ran
    assert with_test_failure_finding([], _round(True)) == []


def _repair(passed: bool | None) -> RepairDecision:
    return make_repair_decision(round_num=1, reviewer_verdict="pass", tests_passed=passed, finding_count=0,
                                repair_rounds_allowed=2, repair_rounds_used=0, is_repair=False,
                                coherence_error=None)


def test_an_unchanged_failure_turns_the_repair_into_a_stop_and_a_changed_one_does_not():
    diag = red_test_diagnostic(NODE_OUTPUT)
    first, same = _round(False, diag), _round(False, diag.replace("74.573", "99.1"))
    changed = _round(False, red_test_diagnostic(PYTEST_OUTPUT))

    assert review_test_evidence(_repair(False), first, [first], "npm test").repair_decision == "repair"
    stopped = review_test_evidence(_repair(False), same, [first, same], "npm test")
    assert (stopped.repair_decision, stopped.reason) == ("stop_exhausted", REASON_TEST_FAILURE_UNCHANGED)
    assert review_test_evidence(_repair(False), changed, [first, changed], "npm test").repair_decision == "repair"


def test_a_budget_probe_that_says_no_turns_the_repair_into_a_stop():
    command = DoDTestCommand([SimpleNamespace(id="C1")], budget_probe=lambda rounds: False)
    rd = _round(False, "boom")

    decision = review_test_evidence(_repair(False), rd, [rd], command)
    assert (decision.repair_decision, decision.reason) == ("stop_exhausted", REASON_REPAIR_BUDGET_INSUFFICIENT)
    # A decision that was no test repair is never touched.
    assert review_test_evidence(_repair(True), _round(True), [], command).repair_decision == "pass_no_repair"


def test_the_command_is_its_checks_and_a_copy_is_the_same_command():
    command = DoDTestCommand([SimpleNamespace(id="ctr-C001")])

    assert str(command) == "the job's required project tests (ctr-C001)"
    assert copy.deepcopy(command) is command and copy.copy(command) is command
    with pytest.raises(TypeError):
        import pickle
        pickle.dumps(command)


def _job(tmp_path: Path, monkeypatch, statuses: list[str], checks: list[dict]) -> SimpleNamespace:
    from packages.orchestration.dod_gate import store_dod
    from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    job = SimpleNamespace(job_id="j1", budgets=None,
                          tasks=[SimpleNamespace(task_id=f"T{i}", status=s) for i, s in enumerate(statuses)])
    store_dod("j1", DoD.model_validate({"schema_v": DOD_SCHEMA_V, "checks": checks, "compiled": False,
                                        "origin": "deterministic"}))
    return job


TESTS_BLOCKING = {"id": "C1", "kind": "project_tests", "source": "standard", "blocking": True}


def test_only_the_last_task_gets_the_blocking_test_checks(tmp_path, monkeypatch):
    job = _job(tmp_path, monkeypatch, ["passed", "running", "pending"], [TESTS_BLOCKING])

    assert final_task_test_command(job, job.tasks[1], None) is None        # a later task is pending
    job.tasks[2].status = "passed"
    command = final_task_test_command(job, job.tasks[1], None)
    assert isinstance(command, DoDTestCommand) and [c.id for c in command.checks] == ["C1"]
    assert final_task_test_command(job, job.tasks[1], "make check") == "make check"   # the operator's wins


def test_a_non_blocking_test_check_is_no_reason_to_test_in_the_loop(tmp_path, monkeypatch):
    job = _job(tmp_path, monkeypatch, ["running"], [{**TESTS_BLOCKING, "blocking": False}])

    assert final_task_test_command(job, job.tasks[0], "") == ""
