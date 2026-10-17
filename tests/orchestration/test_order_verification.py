"""`order_verification`: the order's test request becomes a blocking check, and one honest reading."""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from packages.orchestration import order_verification as OV
from packages.orchestration.dod_gate import load_dod, result_path, store_dod
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck
from packages.orchestration.order_scope import order_test_request
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    return tmp_path / "data"


def _job(state: str = "completed", tasks: list[TaskEntry] | None = None) -> JobPlan:
    job = JobPlan(job_title="t", mission="m", tasks=tasks or [TaskEntry(title="Deliver README.md")])
    job.state = SimpleNamespace(value=state)  # a reading only looks at the state's word
    return job


@pytest.mark.parametrize(("order", "request_"), [
    ("Fix README.md. Führe den vorhandenen Testbefehl aus.", "Führe den vorhandenen Testbefehl aus."),
    ("Fix README.md. Run the test command.", "Run the test command."),
    ("Fix the bug in src/a.py and make sure the tests pass.", "Fix the bug in src/a.py and make sure the tests pass."),
    ("Fix the bug in src/a.py and add a regression test.", ""),        # a test to WRITE is no run
    ("Fix the typo in README.md.", ""),
])
def test_the_order_test_request_is_the_sentence_that_asks_for_a_run(order, request_):
    assert order_test_request(order) == request_


def test_a_requested_run_makes_the_jobs_test_check_blocking_and_is_kept_on_the_job(data_root):
    job = JobPlan(job_title="t", mission="m", tasks=[TaskEntry(title="x")])
    save_job_plan(job)
    store_dod(str(job.job_id), DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic", checks=[
        DoDCheck(id="ctr-C001", kind="project_tests", source="plan_acceptance", blocking=False)]))

    request = OV.require_order_tests(str(job.job_id), "Fix README.md. Run npm test.")

    assert request == "Run npm test."
    [check] = load_dod(str(job.job_id)).checks
    assert (check.id, check.blocking) == ("ctr-C001", True)
    assert load_job_plan(str(job.job_id)).metadata[OV.ORDER_TEST_REQUEST_KEY] == "Run npm test."


def test_a_requested_run_adds_a_test_check_to_a_job_without_one(data_root):
    job = JobPlan(job_title="t", mission="m", tasks=[TaskEntry(title="x")])
    save_job_plan(job)

    OV.require_order_tests(str(job.job_id), "Fix README.md. Run the tests.")

    [check] = load_dod(str(job.job_id)).checks
    assert (check.id, check.kind, check.blocking) == (OV.ORDER_TESTS_CHECK_ID, "project_tests", True)


def test_an_order_without_a_run_changes_nothing(data_root):
    job = JobPlan(job_title="t", mission="m", tasks=[TaskEntry(title="x")])
    save_job_plan(job)

    assert OV.require_order_tests(str(job.job_id), "Fix the typo in README.md.") == ""
    assert load_dod(str(job.job_id)) is None


def _gate(job: JobPlan, *checks: dict) -> None:
    path = result_path(str(job.job_id))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"released": True, "checks": list(checks)}))


def test_the_reading_counts_the_dods_test_run_and_hides_host_paths(data_root):
    job = _job()
    job.metadata[OV.ORDER_TEST_REQUEST_KEY] = "Run the tests."
    _gate(job, {"check_id": "ctr-C001", "kind": "project_tests", "status": "passed", "blocking": True,
                "command": "/home/someone/.venv/bin/python -m pytest tests"},
          {"check_id": "lint", "kind": "lint", "status": "failed"})

    found = OV.job_verification(job)

    assert (found["status"], found["required"]) == ("passed", True)
    [run] = found["runs"]                                  # a lint is no test run
    assert run["command"] == "python -m pytest tests"


@pytest.mark.parametrize(("state", "request_", "checks", "tasks_passed", "expected"), [
    ("completed", "", [], [None], "not_required"),
    ("completed", "Run npm test.", [], [None], "not_run"),
    ("running", "Run npm test.", [], [None], "pending"),
    ("blocked", "Run npm test.", [{"kind": "project_tests", "status": "failed"}], [None], "failed"),
    ("completed", "", [], [True, None], "passed"),
    ("completed", "", [], [True, False], "failed"),
])
def test_unexecuted_tests_are_never_passed(data_root, state, request_, checks, tasks_passed, expected):
    job = _job(state, [TaskEntry(title=f"t{n}", test_passed=passed) for n, passed in enumerate(tasks_passed)])
    job.metadata[OV.ORDER_TEST_REQUEST_KEY] = request_
    if checks:
        _gate(job, *checks)

    assert OV.job_verification(job)["status"] == expected


def test_a_project_without_a_test_command_says_so_when_tests_were_asked_for(data_root):
    from packages.orchestration.project_tests import NO_CHECK_RAN_WORDS

    job = _job()
    job.metadata[OV.ORDER_TEST_REQUEST_KEY] = "Run the tests."
    _gate(job, {"check_id": "order-tests", "kind": "project_tests", "status": "failed",
                "reason": "no_test_command"})

    found = OV.job_verification(job)

    assert (found["status"], found["reason"], found["runs"]) == ("not_run", NO_CHECK_RAN_WORDS, [])
