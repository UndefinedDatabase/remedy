"""What a job's verification really was: the order's test request, its check, and one honest reading.

On 2026-10-17 an order said "Führe den vorhandenen Testbefehl aus". The job's DoD ran `npm test`
and it passed, yet both task records held `test_passed: None`, the client story said "no test
command", and had the tests failed the job would still have ended `completed`, because a `do` job's
DoD checks only report (R-0977). This module closes both gaps with what already exists:

* `require_order_tests` makes the job's `project_tests` check BLOCKING when the order asks for the
  tests to run (and adds that check when the job's DoD has none). A red run then holds the job
  `blocked` through the F061 gate, the one mechanism that already keeps a job from ending green;
  a project that names no test command leaves the check `not run`, which the gate never counts as
  green or red (DECISION F299 D2 (3)). A high-risk change requires the tests the same way, and in
  a repository whose root names no test command (polyglot, several packages) the check runs in the
  package that owns the job's files (`owning_test_packages`), never in an invented one.
* `job_verification` is the one reading every surface shows: the tasks' own test runs and the
  DoD's test checks, each `passed` or `failed`, and a status that never calls an unexecuted test
  passed. Its statuses: `passed`, `failed`, `not_run` (asked for, nothing ran, with the reason),
  `not_required` (not asked for and nothing ran) and `pending` (the job has not ended).

Remedy deliberately does not let an HTTP client name a test command: the command is the project's
own, found where `project_tests` finds it, so no route can make Remedy run an arbitrary argv.
"""
from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

from packages.orchestration.order_scope import order_test_request

#: The job metadata key holding the order's sentence that asks for the tests to run.
ORDER_TEST_REQUEST_KEY = "order_test_request"
#: The id of the check `require_order_tests` adds when the job's DoD has no test check of its own.
ORDER_TESTS_CHECK_ID = "order-tests"
#: The DoD check kinds that run tests; every other kind (a lint, a build, a smoke) is no test run.
_TEST_CHECK_KINDS = frozenset({"project_tests", "pytest"})
#: Job states after which no check of the job runs any more.
_ENDED_STATES = frozenset({"completed", "failed", "blocked", "stopped", "cancelled"})

VERIFICATION_STATUSES = ("passed", "failed", "not_run", "not_required", "pending")


def require_order_tests(job_id: str, order: str) -> str:
    """Make the job's test check blocking when *order* asks for the tests to run; the request or "".

    The sentence is kept on the job (`ORDER_TEST_REQUEST_KEY`), so every later reading knows the
    tests were asked for. A high-risk change (`do_lane.order_risk`: security, persistence,
    deployment) requires them whether or not the order says so. When the repository's root names
    no test command, the job's test checks run in the package that owns its files instead
    (`owning_test_packages`). A DoD that will not parse is left alone: the gate already holds its job.
    """
    from packages.orchestration.dod_gate import dod_path, load_dod, store_dod
    from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    job = load_job_plan(job_id)
    request = order_test_request(order) or (_risk_request(order, job) if job is not None else "")
    packages = owning_test_packages(job) if job is not None else []
    if not request and not packages:
        return ""
    if job is not None and request:
        job.metadata[ORDER_TEST_REQUEST_KEY] = request
        save_job_plan(job)
    dod = load_dod(job_id)
    if dod is None and dod_path(job_id).is_file():
        return request
    checks = list(dod.checks if dod is not None else [])
    if request:
        checks = [c.model_copy(update={"blocking": True}) if c.kind in _TEST_CHECK_KINDS else c
                  for c in checks]
        if not any(c.kind in _TEST_CHECK_KINDS for c in checks):
            checks.append(DoDCheck(id=ORDER_TESTS_CHECK_ID, kind="project_tests", source="standard",
                                   blocking=True, description=request))
    if packages:
        checks = _checks_in_packages(checks, packages)
    if not checks:
        return request
    store_dod(job_id, DoD.model_validate({
        "schema_v": DOD_SCHEMA_V, "checks": [check.model_dump() for check in checks],
        "compiled": dod.compiled if dod is not None else False,
        "origin": dod.origin if dod is not None else "deterministic"}))
    return request


#: At most this many packages get a test check of their own for one job.
MAX_TEST_PACKAGES = 3


def _risk_request(order: str, job: Any) -> str:
    """The sentence requiring the tests of a high-risk change, or "" (`do_lane.order_risk`)."""
    from packages.orchestration.dirty_baseline import job_deliverable_paths
    from packages.orchestration.do_lane import order_risk

    declared, _named = job_deliverable_paths(job)
    risk = order_risk(order, declared)
    return f"The change is high-risk ({risk}), so the project's tests are required." if risk else ""


def owning_test_packages(job: Any) -> list[str]:
    """The folders whose own test command covers the job's files, when the repository's root names none.

    A polyglot or multi-package repository (`web/package.json`, `py/tests/`) has no command at its
    root, so its project test check found nothing and read `not run`. Each file the job declares or
    names is walked up to the nearest folder where `project_tests.find_project_test_command` finds a
    command (the same three sources, the same order); [] when the root has one, when no folder has
    one, or when the root's configuration cannot be read (its check then says why).
    """
    from pathlib import Path

    from packages.orchestration.dirty_baseline import job_deliverable_paths
    from packages.orchestration.project_tests import ProjectTestConfigError, find_project_test_command

    root = Path(str(getattr(job, "repo_path", "") or ""))
    if not str(root) or not root.is_dir():
        return []
    try:
        if find_project_test_command(root, "python3") is not None:
            return []
        declared, named = job_deliverable_paths(job)
        found: list[str] = []
        for rel in dict.fromkeys([*declared, *named]):
            folder = PurePosixPath(rel).parent
            while str(folder) not in (".", "") and ".." not in folder.parts:
                if (root / folder).is_dir() and find_project_test_command(root / folder, "python3"):
                    found.append(str(folder))
                    break
                folder = folder.parent
    except ProjectTestConfigError:
        return []
    return list(dict.fromkeys(found))[:MAX_TEST_PACKAGES]


def _checks_in_packages(checks: list[Any], packages: list[str]) -> list[Any]:
    """Each `project_tests` check that names no folder runs in the first package, and once more,
    under its id with a suffix, in each further one."""
    placed: list[Any] = []
    for check in checks:
        if check.kind != "project_tests" or str(check.spec.get("cwd") or ""):
            placed.append(check)
            continue
        for number, folder in enumerate(packages):
            placed.append(check.model_copy(update={
                "id": check.id if number == 0 else f"{check.id}-{number + 1}",
                "spec": {**check.spec, "cwd": folder}}))
    return placed


def _command_words(command: str) -> str:
    """The command a check ran, without a host path: `/home/x/.venv/bin/python -m pytest` → `python -m pytest`."""
    return " ".join(PurePosixPath(word).name if word.startswith("/") else word for word in command.split())


#: Reasons of a check that ran its command and judged the result; any other non-passed reason
#: with no exit code is a refusal before exec (`dod_runners._refused`).
_RAN_REASONS = frozenset({"", "nonzero_exit", "timeout"})


def _refused_before_running(check: dict[str, Any]) -> bool:
    return (check.get("status") != "passed" and check.get("exit_code") is None
            and str(check.get("reason") or "") not in _RAN_REASONS)


def job_verification(job: Any) -> dict[str, Any]:
    """The job's verification as `{status, required, request, runs, reason}`; see the module text."""
    from packages.orchestration.dod_gate import load_gate_result

    request = str((getattr(job, "metadata", None) or {}).get(ORDER_TEST_REQUEST_KEY) or "")
    runs: list[dict[str, Any]] = [
        {"source": "task", "task_id": str(task.task_id), "status": "passed" if task.test_passed else "failed"}
        for task in job.tasks if task.test_passed is not None]
    # R-1343: a task test command the sandbox refused ran nothing, so it is neither a run nor absent.
    refused_task = next((task for task in job.tasks
                         if task.test_passed is None and task.tripped_limit == "sandbox_unavailable"), None)
    refused = refused_task is not None
    not_run_reason = (f"the test command of task {refused_task.task_id} was refused: the tool sandbox is "
                      "unavailable, so no test ran" if refused_task is not None else "")
    gate = load_gate_result(str(job.job_id)) or {}
    for check in gate.get("checks") or []:
        if not isinstance(check, dict) or check.get("kind") not in _TEST_CHECK_KINDS:
            continue
        if check.get("reason") == "no_test_command":
            from packages.orchestration.project_tests import NO_CHECK_RAN_WORDS
            not_run_reason = NO_CHECK_RAN_WORDS
            continue
        if _refused_before_running(check):
            # A check refused before exec (an executable outside the allowed set, a test command
            # the job itself changed, no tool sandbox) ran nothing: never a failed test, never a pass.
            not_run_reason = not_run_reason or f"the test check was refused before it ran ({check.get('reason')})"
            refused = True
            continue
        runs.append({"source": "dod", "check_id": str(check.get("check_id") or ""),
                     "status": "passed" if check.get("status") == "passed" else "failed",
                     "command": _command_words(str(check.get("command") or "")),
                     "blocking": bool(check.get("blocking"))})
    state = getattr(job.state, "value", str(job.state))
    if any(run["status"] == "failed" for run in runs):
        status = "failed"
    elif runs and not refused:    # one test that could not run leaves the verification incomplete
        status = "passed"
    elif state not in _ENDED_STATES:
        status = "pending"
    elif request or refused:      # a test check that was there and could not run is not "not required"
        status = "not_run"
        not_run_reason = not_run_reason or f"the job ended {state} before its checks ran"
    else:
        status = "not_required"
    return {"status": status, "required": bool(request), "request": request, "runs": runs,
            "reason": not_run_reason if status in ("not_run", "not_required") else ""}
