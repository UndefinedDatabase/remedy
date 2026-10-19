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


@pytest.mark.parametrize(("reason", "exit_code", "expected"), [
    ("executable_not_allowed", None, "not_run"),     # refused before exec: nothing ran
    ("test_command_changed", None, "not_run"),
    ("tool_unavailable", None, "not_run"),
    ("sandbox_unavailable", None, "not_run"),        # exec-1017c: the guard spawned nothing
    ("nonzero_exit", 1, "failed"),                   # it ran and was red
    ("timeout", None, "failed"),                     # it ran out of time: a run, and not green
])
def test_a_check_refused_before_it_ran_is_not_run_never_failed_or_passed(data_root, reason, exit_code, expected):
    job = _job("blocked")
    job.metadata[OV.ORDER_TEST_REQUEST_KEY] = "Run the tests."
    _gate(job, {"check_id": "order-tests", "kind": "project_tests", "status": "failed",
                "reason": reason, "exit_code": exit_code, "command": "cargo test"})

    found = OV.job_verification(job)

    assert found["status"] == expected
    if expected == "not_run":
        assert (found["runs"], found["required"]) == ([], True)
        assert reason in found["reason"]



@pytest.mark.parametrize("request_", ["Run the tests.", ""])
def test_a_task_test_command_the_sandbox_refused_is_not_run_even_beside_a_passing_one(data_root, request_):
    """R-1343: a refused command ran no test; it leaves the job unverified, asked for or not, and one
    passing test of another task never turns the job's verification into a pass."""
    job = _job("blocked", [TaskEntry(title="ran", test_passed=True),
                           TaskEntry(title="refused", test_passed=None, tripped_limit="sandbox_unavailable")])
    job.metadata[OV.ORDER_TEST_REQUEST_KEY] = request_

    found = OV.job_verification(job)

    assert found["status"] == "not_run"
    assert "tool sandbox is unavailable" in found["reason"]
    assert [run["status"] for run in found["runs"]] == ["passed"]


def test_a_refused_check_without_a_request_is_not_run_never_not_required(data_root):
    job = _job("blocked")
    _gate(job, {"check_id": "project-tests", "kind": "project_tests", "status": "failed",
                "reason": "sandbox_unavailable", "exit_code": None, "command": "npm test"})

    assert OV.job_verification(job)["status"] == "not_run"

def _polyglot(tmp_path):
    repo = tmp_path / "repo"
    for rel, text in {"web/package.json": '{"scripts": {"test": "node --test"}}',
                      "web/src/index.js": "export const f = () => 1;\n",
                      "py/pkg/app.py": "x = 1\n", "py/tests/test_app.py": "def test_x():\n    pass\n",
                      "go/calc.go": "package calc\n", "README.md": "# r\n"}.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    return repo


@pytest.mark.parametrize(("files", "packages"), [
    (["web/src/index.js"], ["web"]),                      # the nearest package.json with a test script
    (["py/pkg/app.py"], ["py"]),                          # the nearest folder with a tests folder
    (["web/src/index.js", "py/pkg/app.py"], ["web", "py"]),
    (["go/calc.go"], []),                                 # no command Remedy knows: honestly none
    (["README.md"], []),
])
def test_a_polyglot_repository_tests_the_package_that_owns_the_jobs_files(data_root, tmp_path, files, packages):
    repo = _polyglot(tmp_path)
    job = JobPlan(job_title="t", mission="m", repo_path=str(repo),
                  tasks=[TaskEntry(title=f"Deliver {f}", inputs={"deliverable": f}) for f in files])

    assert OV.owning_test_packages(job) == packages


def test_a_root_test_command_keeps_the_check_at_the_root(data_root, tmp_path):
    repo = _polyglot(tmp_path)
    (repo / "package.json").write_text('{"scripts": {"test": "npm run test --workspaces"}}')
    job = JobPlan(job_title="t", mission="m", repo_path=str(repo),
                  tasks=[TaskEntry(title="x", inputs={"deliverable": "web/src/index.js"})])

    assert OV.owning_test_packages(job) == []


def test_a_requested_run_in_a_polyglot_repository_runs_in_each_owning_package(data_root, tmp_path):
    repo = _polyglot(tmp_path)
    job = JobPlan(job_title="t", mission="m", repo_path=str(repo),
                  tasks=[TaskEntry(title="x", inputs={"deliverable": "web/src/index.js"},
                                   files_hint=["web/src/index.js", "py/pkg/app.py"])])
    save_job_plan(job)
    store_dod(str(job.job_id), DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic", checks=[
        DoDCheck(id="ctr-C001", kind="project_tests", source="plan_acceptance", blocking=False)]))

    OV.require_order_tests(str(job.job_id), "Fix web/src/index.js and py/pkg/app.py. Run the tests.")

    checks = load_dod(str(job.job_id)).checks
    assert [(c.id, c.spec.get("cwd"), c.blocking) for c in checks] == [
        ("ctr-C001", "web", True), ("ctr-C001-2", "py", True)]


def test_a_high_risk_change_requires_the_tests_though_the_order_does_not_ask(data_root, tmp_path):
    job = JobPlan(job_title="t", mission="m", repo_path=str(tmp_path),
                  tasks=[TaskEntry(title="x", inputs={"deliverable": "src/auth/session.py"})])
    save_job_plan(job)

    request = OV.require_order_tests(str(job.job_id), "Change the session expiry in src/auth/session.py.")

    assert "high-risk" in request
    [check] = load_dod(str(job.job_id)).checks
    assert (check.kind, check.blocking) == ("project_tests", True)
    assert load_job_plan(str(job.job_id)).metadata[OV.ORDER_TEST_REQUEST_KEY] == request


@pytest.mark.parametrize(("own_command", "sources"), [("", ["dod"]), ("make check", ["task", "dod"])],
                         ids=["dod-checks-in-the-task", "operator-command"])
def test_a_tasks_run_of_the_dods_own_checks_is_not_counted_beside_the_gates(data_root, own_command, sources):
    """R-1351: with no test command of its own, the last task ran the DoD's checks before review, and
    the gate ran them again; one suite is one run. An operator's own command is a run of its own."""
    job = _job(tasks=[TaskEntry(title="Deliver README.md", test_passed=True)])
    if own_command:
        from packages.orchestration.execution_config import ExecutionConfig
        job.execution_config = ExecutionConfig(test_command=own_command)
    _gate(job, {"check_id": "ctr-C001", "kind": "project_tests", "status": "passed", "blocking": True,
                "command": "npm test"})

    found = OV.job_verification(job)

    assert found["status"] == "passed" and [run["source"] for run in found["runs"]] == sources


def test_a_task_whose_red_run_held_the_job_before_the_gate_is_its_only_evidence(data_root):
    job = _job("blocked", tasks=[TaskEntry(title="Deliver README.md", test_passed=False)])

    found = OV.job_verification(job)

    assert found["status"] == "failed" and [run["source"] for run in found["runs"]] == ["task"]
