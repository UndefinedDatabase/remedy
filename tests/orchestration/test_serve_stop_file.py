"""F200 acceptance: "A STOP file (F011) stops a run the supervisor started,
exactly as it stops a direct run."

One fixture run — a real multi-task job executed through `run_cycles`, the
same conductor `test_serve_restart_kill.py` and `test_resume_kill.py` drive —
is run TWO ways: as a plain subprocess (DIRECT), and as a run the real
`remedy serve start` supervisor launches (SUPERVISED, through
`post_command(..., {"command": "job.run", ...})`, exactly as DECISION F200 D1
describes). In both modes the fixture's second task writes a marker the
instant it starts and then polls `safe_points.stop_requested` — bounded, no
bare sleep — until a stop is pending, finishes that task, and only then lets
`run_cycles`'s own safe point (checked BEFORE every cycle) see the stop and
end the run. The stop itself is requested the same way an operator would:
the real command line, `python3 -m apps.cli.main job stop <job>`, as its own
subprocess — with `REMEDY_SERVE_DIRECT=1` in DIRECT mode (so it writes the
stop request itself) and without it in SUPERVISED mode (so it is forwarded
through the supervisor's socket in client mode, DECISION F200 D3).

Client mode is told apart from direct mode the same way
`test_serve_client_parity.py` tells them apart: by the door's own audit file,
which only the door writes (a direct run never goes through it).

`run_cycles` records "stopped" in `job.metadata["cycle_job_status"]`, not in
`job.state` (which it leaves `paused` for every non-green terminal —
`TERMINAL_RUN_STATE` in `long_run_executor.py`, proven by that module's own
`TestTerminalStatuses.test_stopped_by_operator`): the coarse `RunState` used
for resumability does not distinguish a stop from a pause, while the cycle
conductor's own status vocabulary does. That is this fixture's (and the
conductor's) existing, tested behaviour, not something this module invents —
so "the job's own record reads `stopped`" is checked where the record
actually says it.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

from packages.orchestration.command_audit import AUDIT_FILENAME
from packages.orchestration.data_paths import normalize_job_id
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan
from packages.orchestration.serve_daemon import post_command, socket_answers
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import read_run_record

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Three tasks: the first completes normally, the second is the one that
#: starts, marks itself, and waits for the stop; the third must still be
#: PENDING when the run ends — proof the stop landed at its very next safe
#: point and not a cycle later.
TOTAL_TASKS = 3
STOP_ON_CYCLE = 2

READY_TIMEOUT_SECONDS = 15.0
MARKER_TIMEOUT_SECONDS = 25.0
END_TIMEOUT_SECONDS = 30.0
POLL_SECONDS = 0.02

_HEX16 = re.compile(r"\b[0-9a-f]{16}\b")

#: The fixture run. Modelled on `test_serve_restart_kill.py`'s
#: FIXTURE_RUN_SOURCE: a real multi-task job executed through `run_cycles`,
#: one task per cycle. Unlike that fixture (which parks forever for a kill),
#: this one's doomed task POLLS `stop_requested` — bounded — and completes
#: once a stop is pending, so the run reaches its NEXT safe point with a stop
#: already requested rather than dying mid-task.
FIXTURE_RUN_SOURCE = '''
import json
import sys
import time
from pathlib import Path

from packages.core.models import RunState
from packages.orchestration.long_run_executor import CycleLimits, TaskAttempt, run_cycles
from packages.orchestration.pingpong_job import require_job_plan, save_job_plan
from packages.orchestration.safe_points import stop_requested

JOB_ID = sys.argv[1]
MARKER = Path(sys.argv[2])
STOP_ON_CYCLE = int(sys.argv[3])
TOTAL_TASKS = int(sys.argv[4])

#: Bounded: the fixture never waits past this for the stop it is told to
#: expect, so a broken test fails loudly instead of hanging the suite.
WAIT_TIMEOUT_SECONDS = 20.0
WAIT_POLL_SECONDS = 0.05

job = require_job_plan(JOB_ID)
if job.state != RunState.RUNNING:
    job.state = RunState.RUNNING
    save_job_plan(job)

_cycle = {"n": 0}


def step(j, _provider):
    pending = [t for t in j.tasks if t.status == RunState.PENDING]
    if not pending:
        return TaskAttempt()
    task = pending[0]
    _cycle["n"] += 1
    if _cycle["n"] == STOP_ON_CYCLE:
        MARKER.write_text(json.dumps({"task_id": task.task_id}), encoding="utf-8")
        deadline = time.monotonic() + WAIT_TIMEOUT_SECONDS
        while stop_requested(JOB_ID) is None:
            if time.monotonic() > deadline:
                raise SystemExit("the stop request never arrived")
            time.sleep(WAIT_POLL_SECONDS)
    task.status = RunState.COMPLETED
    return TaskAttempt(task_id=task.task_id, executed=True, verified=True)


result = run_cycles(job, CycleLimits(max_cycles=TOTAL_TASKS + 2), lambda _ctx: None,
                    task_step=step)
print(json.dumps({"terminal_status": result.terminal_status,
                  "job_status": result.job_status, "job_id": JOB_ID}))
'''

#: Starts one supervisor on an explicit data root, RUN_ARGV built from argv —
#: a real subprocess cannot be handed a Python closure. Modelled on
#: `test_serve_restart_kill.py`'s SUPERVISOR_SOURCE.
SUPERVISOR_SOURCE = '''
import sys
from pathlib import Path

from packages.orchestration.serve_daemon import run_supervisor

root = Path(sys.argv[1])
fixture_run = sys.argv[2]
marker = sys.argv[3]
stop_on_cycle = sys.argv[4]
total_tasks = sys.argv[5]


def run_argv(job_id):
    return [sys.executable, fixture_run, job_id, marker, stop_on_cycle, total_tasks]


run_supervisor(root, run_argv=run_argv)
'''


def _env(root: Path, *, direct: bool) -> dict[str, str]:
    env = dict(os.environ)
    env["REMEDY_DATA_DIR"] = str(root)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUNBUFFERED"] = "1"
    if direct:
        env["REMEDY_SERVE_DIRECT"] = "1"
    else:
        env.pop("REMEDY_SERVE_DIRECT", None)
    return env


def _wait_until(deadline_seconds: float, what: str, check) -> None:
    deadline = time.monotonic() + deadline_seconds
    while time.monotonic() < deadline:
        if check():
            return
        time.sleep(POLL_SECONDS)
    raise AssertionError(f"timed out waiting for {what}")


def _make_job(root: Path) -> JobPlan:
    job = JobPlan(job_title="stop-file-fixture",
                 tasks=[TaskEntry(title=f"t{i}", body="d") for i in range(TOTAL_TASKS)])
    save_job_plan(job, root)
    return job


def _job_record(root: Path, job_id: str) -> dict:
    job = load_job_plan(normalize_job_id(job_id), root)
    assert job is not None, f"job {job_id} vanished from {root}"
    return {
        "cycle_job_status": job.metadata.get("cycle_job_status"),
        "task_statuses": [str(t.status) for t in job.tasks],
    }


def _audit_outcomes(root: Path, job_id: str) -> list[str]:
    path = root / "control" / "jobs" / job_id / AUDIT_FILENAME
    if not path.exists():
        return []
    return [json.loads(line)["outcome"] for line in path.read_bytes().splitlines()]


def _normalise_stop_output(text: str, job_id: str) -> str:
    """JOB_ID and the request id (16 lowercase hex characters, minted fresh
    per episode) are the only things that differ by construction between an
    otherwise identical run in each mode."""
    return _HEX16.sub("<ID>", text.replace(job_id, "<JOB>"))


@dataclass
class FixtureRun:
    """One mode's end state: what the job's own record says, what the run's
    process and the stop command exited with, and what printed."""

    job_id: str
    root: Path
    run_exit_code: int
    stop_exit_code: int
    stop_output: str
    job_record: dict
    audit: list[str]


def _run_direct(tmp_path_factory: pytest.TempPathFactory) -> FixtureRun:
    base = tmp_path_factory.mktemp("stopd")
    root = base / "data"
    root.mkdir()
    job = _make_job(root)
    job_id = str(job.job_id)
    marker = base / "marker.json"
    fixture_script = base / "fixture_run.py"
    fixture_script.write_text(FIXTURE_RUN_SOURCE, encoding="utf-8")

    proc = subprocess.Popen(
        [sys.executable, str(fixture_script), job_id, str(marker),
         str(STOP_ON_CYCLE), str(TOTAL_TASKS)],
        cwd=str(REPO_ROOT), env=_env(root, direct=False),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        _wait_until(MARKER_TIMEOUT_SECONDS, "the direct fixture's marker",
                   lambda: marker.exists() or proc.poll() is not None)
        assert proc.poll() is None, (
            f"the direct fixture exited before writing its marker:\n{proc.stderr.read()}")

        stop = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "stop", job_id,
             "--reason", "proof"],
            cwd=str(REPO_ROOT), env=_env(root, direct=True),
            capture_output=True, text=True, timeout=30)

        out, err = proc.communicate(timeout=END_TIMEOUT_SECONDS)
        assert proc.returncode == 0, f"the direct fixture failed:\n{err}\n{out}"
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=10)

    return FixtureRun(
        job_id=job_id, root=root, run_exit_code=proc.returncode,
        stop_exit_code=stop.returncode,
        stop_output=_normalise_stop_output(stop.stdout, job_id),
        job_record=_job_record(root, job_id), audit=_audit_outcomes(root, job_id))


def _run_supervised(tmp_path_factory: pytest.TempPathFactory) -> FixtureRun:
    base = tmp_path_factory.mktemp("stops")
    root = base / "data"
    root.mkdir()
    job = _make_job(root)
    job_id = str(job.job_id)
    marker = base / "marker.json"
    fixture_script = base / "fixture_run.py"
    fixture_script.write_text(FIXTURE_RUN_SOURCE, encoding="utf-8")
    supervisor_script = base / "run_supervisor_cmd.py"
    supervisor_script.write_text(SUPERVISOR_SOURCE, encoding="utf-8")

    paths = serve_paths(root)
    supervisor = subprocess.Popen(
        [sys.executable, str(supervisor_script), str(root), str(fixture_script),
         str(marker), str(STOP_ON_CYCLE), str(TOTAL_TASKS)],
        cwd=str(REPO_ROOT), env=_env(root, direct=False),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        _wait_until(READY_TIMEOUT_SECONDS, "the supervisor's socket to answer",
                   lambda: socket_answers(paths.socket) or supervisor.poll() is not None)
        assert supervisor.poll() is None, (
            f"the supervisor exited early:\n{supervisor.stderr.read()}")

        status, body = post_command(root, job_id,
                                    {"command": "job.run", "client_nonce": "stop-file-proof"})
        assert status == 200, body

        _wait_until(MARKER_TIMEOUT_SECONDS, "the supervised fixture's marker", marker.exists)

        stop = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "stop", job_id,
             "--reason", "proof"],
            cwd=str(REPO_ROOT), env=_env(root, direct=False),
            capture_output=True, text=True, timeout=30)

        def _run_ended() -> bool:
            record = read_run_record(paths, job_id)
            return record is not None and record.exit_code is not None

        _wait_until(END_TIMEOUT_SECONDS, "the supervised run to record its end", _run_ended)
        record = read_run_record(paths, job_id)
        assert record is not None
    finally:
        if supervisor.poll() is None:
            supervisor.terminate()
            try:
                supervisor.wait(timeout=10)
            except subprocess.TimeoutExpired:
                supervisor.kill()
                supervisor.wait(timeout=10)

    return FixtureRun(
        job_id=job_id, root=root, run_exit_code=record.exit_code,
        stop_exit_code=stop.returncode,
        stop_output=_normalise_stop_output(stop.stdout, job_id),
        job_record=_job_record(root, job_id), audit=_audit_outcomes(root, job_id))


_RUNNERS = {"direct": _run_direct, "supervised": _run_supervised}

#: Door acceptances expected per mode: none direct; `job.run` then `job.stop`
#: supervised — the same count `test_serve_client_parity.py` asserts for each
#: command alone.
_EXPECTED_AUDIT = {"direct": [], "supervised": ["accepted", "accepted"]}


@pytest.fixture(scope="module")
def runs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, FixtureRun]:
    """Both modes, run exactly once each and shared by every assertion below —
    the scenario is expensive (two real subprocesses apiece) and nothing
    after this needs a second run of either mode."""
    return {mode: runner(tmp_path_factory) for mode, runner in _RUNNERS.items()}


@pytest.mark.parametrize("mode", sorted(_RUNNERS))
def test_the_run_reaches_the_same_stopped_end_in_each_mode(mode, runs):
    run = runs[mode]
    assert run.run_exit_code == 0
    assert run.stop_exit_code == 0
    assert run.job_record["cycle_job_status"] == "stopped"
    assert run.job_record["task_statuses"] == ["completed", "completed", "pending"]
    assert run.audit == _EXPECTED_AUDIT[mode]


def test_only_the_supervised_stop_goes_through_the_doors_audit(runs):
    """A direct run never reaches the door; a supervised one is answered by
    it — the one thing that actually tells the two modes apart on disk."""
    assert runs["direct"].audit == []
    assert runs["supervised"].audit == ["accepted", "accepted"]


def test_the_stop_commands_output_and_exit_code_are_equal_between_modes(runs):
    direct, supervised = runs["direct"], runs["supervised"]
    assert (direct.stop_exit_code, direct.stop_output) == (
        supervised.stop_exit_code, supervised.stop_output)


def test_the_runs_process_exit_code_is_equal_between_modes(runs):
    assert runs["direct"].run_exit_code == runs["supervised"].run_exit_code


def test_the_jobs_own_record_is_equal_between_modes(runs):
    assert runs["direct"].job_record == runs["supervised"].job_record
