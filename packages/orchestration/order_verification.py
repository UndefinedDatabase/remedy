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
    request = order_test_request(order) or (
        (_risk_request(order, job) or _project_tests_request(job)) if job is not None else "")
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
        # amend1027 B2: tests the order did not ask for make only the project's own command
        # blocking, never a compiled pytest check that may not fit the project.
        flip = _TEST_CHECK_KINDS if request != PROJECT_TESTS_REQUEST else frozenset({"project_tests"})
        checks = [c.model_copy(update={"blocking": True}) if c.kind in flip else c for c in checks]
        if not any(c.kind == "project_tests" for c in checks) and (
                _project_tests_request(job) or not any(c.kind in _TEST_CHECK_KINDS for c in checks)):
            checks.append(DoDCheck(id=ORDER_TESTS_CHECK_ID, kind="project_tests", source="standard",
                                   blocking=True, description=request))
        timeout = project_tests_timeout(job)
        checks = [c.model_copy(update={"spec": {**c.spec, "timeout_sec": timeout}})
                  if c.kind == "project_tests" and timeout and "timeout_sec" not in c.spec else c
                  for c in checks]
    if packages:
        checks = _checks_in_packages(checks, packages)
    if not checks:
        return request
    store_dod(job_id, DoD.model_validate({
        "schema_v": DOD_SCHEMA_V, "checks": [check.model_dump() for check in checks],
        "compiled": dod.compiled if dod is not None else False,
        "origin": dod.origin if dod is not None else "deterministic"}))
    return request


#: amend1027 B2: the sentence a job carries when the project's own tests run because it has them.
PROJECT_TESTS_REQUEST = "The project names a test command, so its own tests run before a result is offered."


def _project_tests_request(job: Any) -> str:
    """`PROJECT_TESTS_REQUEST` when the job's repository names a test command that can run, else ""
    (operator amendment amend1027-green-builds B2: the DoD runs the project's tests itself)."""
    from pathlib import Path

    from packages.orchestration.project_tests import ProjectTestConfigError, find_project_test_command

    raw = str(getattr(job, "repo_path", "") or "")
    if not raw or not Path(raw).is_dir():
        return ""
    try:
        found = find_project_test_command(Path(raw), "python3")
    except ProjectTestConfigError:
        return ""
    return PROJECT_TESTS_REQUEST if found is not None and not found.unrunnable else ""


def project_tests_timeout(job: Any) -> int:
    """The project tests' time limit from the order: half its wall-clock cap, from the DoD's
    default to an hour; 0 (the default applies) when the job sets no cap."""
    from packages.orchestration.dod_runners import CHECK_TIMEOUT_DEFAULT_SEC

    minutes = ((getattr(job, "budgets", None) or {}) if job is not None else {}).get("max_wall_clock_minutes")
    if not isinstance(minutes, int) or isinstance(minutes, bool) or minutes <= 0:
        return 0
    return max(CHECK_TIMEOUT_DEFAULT_SEC, min(3600, minutes * 30))


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
#: with no exit code is a refusal before exec (`dod_runners._refused`). A run cut at its time limit
#: judged nothing either (amend1027 B3: "Zeitlimit" is a reason no test ran).
_RAN_REASONS = frozenset({"", "nonzero_exit"})
#: amend1027 B3: a refused DoD check's reason as the key of `builder_test_runs.NOT_RUN_REASONS`.
_REFUSAL_KEYS = {"tool_unavailable": "command_not_found", "executable_not_allowed": "permission_denied",
                 "timeout": "timeout", "sandbox_unavailable": "sandbox_unavailable",
                 "no_test_command": "no_test_command"}
#: amend1027 B2: how much of a red run's output the reading carries.
MAX_VERIFICATION_OUTPUT_CHARS = 4000


def _refused_before_running(check: dict[str, Any]) -> bool:
    return (check.get("status") != "passed" and check.get("exit_code") is None
            and str(check.get("reason") or "") not in _RAN_REASONS)


def _without_host_paths(text: str, job: Any) -> str:
    """TEXT with the job's workspace path and the home folder taken out, cut to its last 4,000 characters."""
    import os

    for prefix in (str(getattr(job, "job_workspace_path", "") or ""), os.path.expanduser("~")):
        if prefix and prefix != "/":
            text = text.replace(prefix.rstrip("/") + "/", "").replace(prefix, "~")
    return text[-MAX_VERIFICATION_OUTPUT_CHARS:]


def _builder_readings(job: Any) -> dict[str, dict[str, Any]]:
    """The builder's last test reading of each task run, keyed by its run id (amend1027 B1)."""
    from packages.orchestration.builder_test_runs import load_builder_test_runs

    last: dict[str, dict[str, Any]] = {}
    for row in load_builder_test_runs(str(job.job_id)):
        if row.get("passed") is not None or str(row.get("run_id") or "") not in last:
            last[str(row.get("run_id") or "")] = row
    return last


def job_verification(job: Any) -> dict[str, Any]:
    """The job's verification as `{status, required, request, runs, reason, reason_key, tested_by,
    output}`; see the module text. `tested_by` names `builder` when a task's reading was its
    builder's own test run and `final_check` when Remedy ran the tests itself (amend1027 B)."""
    from packages.orchestration.builder_test_runs import NOT_RUN_REASONS
    from packages.orchestration.dod_gate import load_gate_result

    request = str((getattr(job, "metadata", None) or {}).get(ORDER_TEST_REQUEST_KEY) or "")
    builder = _builder_readings(job)
    runs: list[dict[str, Any]] = []
    for task in job.tasks:
        reading = builder.get(str(getattr(task, "run_id", "") or ""))
        if task.test_passed is not None:
            mine = reading is not None and reading.get("passed") is task.test_passed
            runs.append({"source": "builder" if mine else "task", "task_id": str(task.task_id),
                         "status": "passed" if task.test_passed else "failed",
                         **({"command": _command_words(str(reading["command"]))} if mine else {})})
    # R-1343: a task test command the sandbox refused ran nothing, so it is neither a run nor absent.
    refused_task = next((task for task in job.tasks
                         if task.test_passed is None and task.tripped_limit == "sandbox_unavailable"), None)
    refused = refused_task is not None
    not_run_reason = (f"the test command of task {refused_task.task_id} was refused: the tool sandbox is "
                      "unavailable, so no test ran" if refused_task is not None else "")
    reason_key = "sandbox_unavailable" if refused else ""
    output = ""
    gate = load_gate_result(str(job.job_id)) or {}
    for check in gate.get("checks") or []:
        if not isinstance(check, dict) or check.get("kind") not in _TEST_CHECK_KINDS:
            continue
        if check.get("reason") == "no_test_command":
            from packages.orchestration.project_tests import NO_CHECK_RAN_WORDS
            not_run_reason, reason_key = NO_CHECK_RAN_WORDS, "no_test_command"
            continue
        if _refused_before_running(check):
            # A check refused before exec (an executable outside the allowed set, a test command
            # the job itself changed, no tool sandbox, its time limit) ran nothing: never a failed
            # test, never a pass.
            not_run_reason = not_run_reason or f"the test check was refused before it ran ({check.get('reason')})"
            reason_key = reason_key or _REFUSAL_KEYS.get(str(check.get("reason") or ""), "not_attempted")
            refused = True
            continue
        if check.get("status") != "passed" and not output:
            output = _without_host_paths(str(check.get("output_tail") or ""), job)
        runs.append({"source": "dod", "check_id": str(check.get("check_id") or ""),
                     "status": "passed" if check.get("status") == "passed" else "failed",
                     "command": _command_words(str(check.get("command") or "")),
                     "blocking": bool(check.get("blocking"))})
    tested_by = sorted({"builder" if run["source"] == "builder" else "final_check" for run in runs}
                       | ({"builder"} if any(r.get("passed") is not None for r in builder.values()) else set()))
    if any(run["source"] == "dod" for run in runs):
        # R-1351: with no test command of its own, a task's run WAS the DoD's checks, run again by the
        # gate after the last task; the gate's run is the reading, so one suite never counts twice.
        # amend1027 B2: the gate's run decides over a builder's own run as well.
        own = str(getattr(getattr(job, "execution_config", None), "test_command", "") or "")
        runs = [run for run in runs if run["source"] == "dod" or (own and run["source"] == "task")]
    if not output and any(run["status"] == "failed" for run in runs):
        red = [row for row in builder.values() if row.get("passed") is False]
        output = _without_host_paths(str(red[-1].get("output_tail") or ""), job) if red else ""
    state = getattr(job.state, "value", str(job.state))
    if any(run["status"] == "failed" for run in runs):
        status = "failed"
    elif runs and not refused:    # one test that could not run leaves the verification incomplete
        status = "passed"
    elif state not in _ENDED_STATES:
        status = "pending"
    elif request or refused:      # a test check that was there and could not run is not "not required"
        status = "not_run"
        if not not_run_reason:
            told = [row for row in builder.values() if row.get("reason_key")]
            reason_key = str(told[-1]["reason_key"]) if told else ""
            not_run_reason = (NOT_RUN_REASONS.get(reason_key, "") if told else "") or (
                f"the job ended {state} before its checks ran")
    else:
        status = "not_required"
    return {"status": status, "required": bool(request), "request": request, "runs": runs,
            "reason": not_run_reason if status in ("not_run", "not_required") else "",
            "reason_key": (reason_key or "not_attempted") if status == "not_run" else "",
            "tested_by": tested_by, "output": output if status == "failed" else ""}
