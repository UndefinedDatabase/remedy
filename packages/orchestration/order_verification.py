"""What a job's verification really was: the order's test request, its check, and one honest reading.

On 2026-10-17 an order said "Führe den vorhandenen Testbefehl aus". The job's DoD ran `npm test`
and it passed, yet both task records held `test_passed: None`, the client story said "no test
command", and had the tests failed the job would still have ended `completed`, because a `do` job's
DoD checks only report (R-0977). This module closes both gaps with what already exists:

* `require_order_tests` makes the job's `project_tests` check BLOCKING when the order asks for the
  tests to run (and adds that check when the job's DoD has none). A red run then holds the job
  `blocked` through the F061 gate, the one mechanism that already keeps a job from ending green;
  a project that names no test command leaves the check `not run`, which the gate never counts as
  green or red (DECISION F299 D2 (3)).
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
    tests were asked for. A DoD that will not parse is left alone: the gate already holds its job.
    """
    request = order_test_request(order)
    if not request:
        return ""
    from packages.orchestration.dod_gate import dod_path, load_dod, store_dod
    from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck
    from packages.orchestration.pingpong_job import load_job_plan, save_job_plan

    job = load_job_plan(job_id)
    if job is not None:
        job.metadata[ORDER_TEST_REQUEST_KEY] = request
        save_job_plan(job)
    dod = load_dod(job_id)
    if dod is None and dod_path(job_id).is_file():
        return request
    checks = [c.model_copy(update={"blocking": True}) if c.kind in _TEST_CHECK_KINDS else c
              for c in (dod.checks if dod is not None else [])]
    if not any(c.kind in _TEST_CHECK_KINDS for c in checks):
        checks.append(DoDCheck(id=ORDER_TESTS_CHECK_ID, kind="project_tests", source="standard",
                               blocking=True, description=request))
    store_dod(job_id, DoD.model_validate({
        "schema_v": DOD_SCHEMA_V, "checks": [check.model_dump() for check in checks],
        "compiled": dod.compiled if dod is not None else False,
        "origin": dod.origin if dod is not None else "deterministic"}))
    return request


def _command_words(command: str) -> str:
    """The command a check ran, without a host path: `/home/x/.venv/bin/python -m pytest` → `python -m pytest`."""
    return " ".join(PurePosixPath(word).name if word.startswith("/") else word for word in command.split())


def job_verification(job: Any) -> dict[str, Any]:
    """The job's verification as `{status, required, request, runs, reason}`; see the module text."""
    from packages.orchestration.dod_gate import load_gate_result

    request = str((getattr(job, "metadata", None) or {}).get(ORDER_TEST_REQUEST_KEY) or "")
    runs: list[dict[str, Any]] = [
        {"source": "task", "task_id": str(task.task_id), "status": "passed" if task.test_passed else "failed"}
        for task in job.tasks if task.test_passed is not None]
    not_run_reason = ""
    gate = load_gate_result(str(job.job_id)) or {}
    for check in gate.get("checks") or []:
        if not isinstance(check, dict) or check.get("kind") not in _TEST_CHECK_KINDS:
            continue
        if check.get("reason") == "no_test_command":
            from packages.orchestration.project_tests import NO_CHECK_RAN_WORDS
            not_run_reason = NO_CHECK_RAN_WORDS
            continue
        runs.append({"source": "dod", "check_id": str(check.get("check_id") or ""),
                     "status": "passed" if check.get("status") == "passed" else "failed",
                     "command": _command_words(str(check.get("command") or "")),
                     "blocking": bool(check.get("blocking"))})
    state = getattr(job.state, "value", str(job.state))
    if any(run["status"] == "failed" for run in runs):
        status = "failed"
    elif runs:
        status = "passed"
    elif state not in _ENDED_STATES:
        status = "pending"
    elif request:
        status = "not_run"
        not_run_reason = not_run_reason or f"the job ended {state} before its checks ran"
    else:
        status = "not_required"
    return {"status": status, "required": bool(request), "request": request, "runs": runs,
            "reason": not_run_reason if status in ("not_run", "not_required") else ""}
