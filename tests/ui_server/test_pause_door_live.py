"""F025 R4 T2 — job.pause and job.unpause through the REAL write door, live.

Every class below drives a fake-provider job through the real HTTP door
(`packages/orchestration/ui_server.py`'s command channel), the way an operator's
browser would. `TestJobScopeLiveDoor` and `TestTaskScopeLiveDoor` run that job in
ITS OWN PROCESS — the live-runner pattern `tests/orchestration/test_job_stop_integration.py`
established for the kill switch — because only a real, separate process can prove
that a pause taking effect mid-call lets that call finish and starts no next one.
`TestRefusalsLiveDoor` and `TestWithdrawLiveDoor` need no live runner: a refusal
and a withdrawal are both decided before any provider call would begin.

The UI server itself runs IN this test process, in a background thread
(`tests/ui_server/test_command_dispatch.py`'s own pattern) — REMEDY_DATA_DIR is
the same directory the subprocess runner writes into, so both see the same
control files and the same job record.
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import textwrap
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import psutil
import pytest

from packages.orchestration.data_paths import job_record_path

CSRF_HEADER = "X-Remedy-CSRF"

_THREE_TASK_JOB = """\
# Job: Live Pause Door Test

## Task 1
Add module one.

Acceptance:
- module exists

## Task 2
Add module two.

Acceptance:
- module exists

## Task 3
Add module three.

Acceptance:
- module exists
"""

#: How long each of SlowProvider's calls sleeps for — long enough that an HTTP
#: POST issued the instant the metafile appears reliably lands while a call is
#: in flight, short enough that the ten runs G5's mutation tool makes stay fast.
#: The job-scope test does not rely on it: R-1159 holds its call open instead.
_CALL_SLEEP_S = 0.3

_RUNNER = """\
import json, sys, time
from pathlib import Path
sys.path.insert(0, {repo!r})
from packages.orchestration.pause_control import PAUSE_REQUEST_FILENAME
from packages.orchestration.pingpong_job import parse_job_file, run_job
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.safe_points import job_control_dir

#: R-1159: the build call (counted from 1) held open until a job pause request
#: exists on disk; 0 holds none. Holding it makes "the pause lands while that
#: call is in flight" true by construction, not by a race against the sleep.
HOLD_BUILD = {hold_build!r}


class SlowProvider(FakeProvider):
    '''A provider whose calls take real time, like the real ones do. Nothing here
    tells the runner about a pause: the runner has to notice it on its own, exactly
    the way it notices a stop. The held call only WAITS until the request file
    exists, never reads it, and then returns exactly what any other call returns.'''

    build_calls = 0

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        time.sleep({sleep!r})
        if self.build_calls == HOLD_BUILD:
            pause_file = job_control_dir(job.job_id) / PAUSE_REQUEST_FILENAME
            Path({in_flight!r}).write_text("in flight" + chr(10))
            deadline = time.monotonic() + 60.0
            while not pause_file.is_file() and time.monotonic() < deadline:
                time.sleep(0.02)
        return super().build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        time.sleep({sleep!r})
        return super().review(prompt, **kwargs)


job = parse_job_file(Path({job_file!r}).read_text(), {target!r})
with Path({metafile!r}).open("w") as f:
    f.write(job.job_id + chr(10))
    for task in job.tasks:
        f.write(task.task_id + chr(10))


def provider():
    return SlowProvider(pass_on_round=1, fail_on_round=99)


final = run_job(job.job_id, builder_provider=provider(),
                reviewer_provider=provider(), repair_rounds=0)
print("FINAL:" + final.state, flush=True)
# R-1159: why the job ended where it did, so that a red run explains itself.
print("DETAIL:" + json.dumps(dict(
    error=final.error, pause=final.pause,
    tasks=[dict(status=t.status, final_status=t.final_status,
                detail=t.final_status_detail, error=t.error) for t in final.tasks]),
    default=str), flush=True)
"""


def _test_owned_children(baseline_pids: set[int], tmp_path: Path) -> list[psutil.Process]:
    """Children this TEST is responsible for — nobody else's. Mirrors
    `test_job_stop_integration.py`'s own helper of the same name exactly."""
    owned: list[psutil.Process] = []
    for child in psutil.Process().children(recursive=True):
        try:
            if child.pid in baseline_pids:
                continue
            if child.status() == psutil.STATUS_ZOMBIE:
                continue
            marker = str(tmp_path)
            cwd = ""
            with contextlib.suppress(psutil.Error):
                cwd = child.cwd() or ""
            cmdline = ""
            with contextlib.suppress(psutil.Error):
                cmdline = " ".join(child.cmdline())
            if marker in cwd or marker in cmdline:
                owned.append(child)
        except psutil.NoSuchProcess:
            continue
    return owned


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`.

    Mirrors `test_command_dispatch.py`'s helper of the same name and purpose —
    each live test file owns its own copy, the established convention here. The
    info file is named UNIQUELY per call: several tests here start a second
    server, in the SAME `tmp_path`, to submit the unpause — a shared filename
    would let the second wait read the first server's stale, already-published
    info before the new thread ever writes its own (R-0734's race, one level up).
    """
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / f"server_info_{secrets.token_hex(4)}.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    from tests.ui_server.server_start import wait_for_server_info

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return wait_for_server_info(info_file, t)["port"], token


def _post(port: int, token: str, command: str, *, job_id: str, nonce: str,
         args: dict | None = None) -> tuple[int, dict]:
    payload: dict = {"command": command, "client_nonce": nonce}
    if args is not None:
        payload["args"] = args
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("POST", f"/api/jobs/{job_id}/commands",
                     body=json.dumps(payload),
                     headers={"Authorization": f"Bearer {token}",
                              CSRF_HEADER: token,
                              "Content-Type": "application/json"})
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read())
    finally:
        conn.close()


def _audit_outcomes(control_root: Path, job_id: str) -> list[str]:
    from packages.orchestration.command_audit import AUDIT_FILENAME

    path = control_root / "jobs" / job_id / AUDIT_FILENAME
    if not path.is_file():
        return []
    return [json.loads(line)["outcome"] for line in path.read_bytes().splitlines()]


def _events(data_root: Path, job_id: str, event: str) -> list[dict]:
    runs = data_root / "job_logs" / job_id
    out: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                raw = json.loads(line)
                if raw.get("event") == event:
                    out.append(raw)
    return out


def _job_data(data_dir: Path, job_id: str) -> dict:
    return json.loads(job_record_path(job_id, data_dir).read_text())


# ---------------------------------------------------------------------------
# L1 — job scope, a real runner process
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestJobScopeLiveDoor:
    def test_pause_parks_the_job_and_unpause_names_the_relaunch(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        metafile = tmp_path / "meta.txt"
        in_flight = tmp_path / "in_flight.txt"
        script = tmp_path / "runner.py"
        # Build call 2 is task 2's build call: task 1 took build call 1.
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            metafile=str(metafile), sleep=_CALL_SLEEP_S, hold_build=2,
            in_flight=str(in_flight)))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        baseline = {c.pid for c in psutil.Process().children(recursive=True)}
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        try:
            deadline = time.monotonic() + 60.0
            while time.monotonic() < deadline:
                if metafile.is_file() and metafile.read_text().strip():
                    break
                assert proc.poll() is None, "the runner exited before writing its metafile"
                time.sleep(0.02)
            else:
                pytest.fail("the runner never wrote its metafile within 60s")
            lines = metafile.read_text().splitlines()
            job_id = lines[0]

            # Wait until task 2's build call is in flight before pausing. R-1159:
            # that call is HELD until the pause request exists, so the pause lands
            # during a call ALREADY IN FLIGHT however slow the server is to start.
            deadline = time.monotonic() + 60.0
            while time.monotonic() < deadline:
                if in_flight.is_file():
                    break
                assert proc.poll() is None, "the runner exited before task 2's build call"
                time.sleep(0.02)
            else:
                pytest.fail("task 2's build call never started within 60s")

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)
                # Job scope: no --task. Task 2's build call is in flight now
                # (SlowProvider sleeps): the call it interrupts finishes, and no
                # reviewer call for task 2 ever starts.
                status, body = _post(port, token, "job.pause", job_id=job_id,
                                     nonce="n-pause")
                assert status == 200, body
                assert body["outcome"] == "requested", body
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            # R-1159: the runner's DETAIL line and standard error ride on every
            # assertion below, so a red run names each task's status and the stop reason.
            why = f"{out}\nstderr:\n{err}"
            assert "FINAL:paused" in out, why
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        data = _job_data(data_dir, job_id)
        assert data["status"] == "paused", why
        assert data["pause"]["scope"] == "job", why
        statuses = [t["status"] for t in data["tasks"]]
        assert statuses[0] == "applied_to_job_workspace", why  # task 1's work is durable
        assert statuses[1] == "pending", why    # task 2's call finished; it never applied
        assert statuses[2] == "pending", why

        assert not psutil.pid_exists(proc.pid) or \
            psutil.Process(proc.pid).status() == psutil.STATUS_ZOMBIE
        assert _test_owned_children(baseline, tmp_path) == []

        # The unpause answers PARKED — this door starts no process of its own.
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.unpause", job_id=job_id,
                                 nonce="n-unpause")
            assert status == 200, body
            assert body["outcome"] == "parked", body
            assert body["next"] == f"remedy job run {job_id}", body

            # "Running that command" — the same run_job() `remedy job run` itself calls.
            from packages.orchestration.pingpong_job import JOB_COMPLETED, run_job
            from packages.orchestration.pingpong_provider import FakeProvider

            resumed = run_job(
                job_id,
                builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                repair_rounds=0)
            assert resumed.state == JOB_COMPLETED
            assert len(_events(data_dir, job_id, "job_resumed")) == 1
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# L2 — task scope, a real runner process
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestTaskScopeLiveDoor:
    def test_pause_withholds_one_task_and_unpause_releases_it(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        metafile = tmp_path / "meta.txt"
        script = tmp_path / "runner.py"
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            metafile=str(metafile), sleep=_CALL_SLEEP_S, hold_build=0,
            in_flight=str(tmp_path / "in_flight.txt")))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        try:
            deadline = time.monotonic() + 60.0
            while time.monotonic() < deadline:
                if metafile.is_file() and len(metafile.read_text().splitlines()) >= 4:
                    break
                assert proc.poll() is None, "the runner exited before writing its metafile"
                time.sleep(0.02)
            else:
                pytest.fail("the runner never wrote its metafile within 60s")
            lines = metafile.read_text().splitlines()
            job_id, task_ids = lines[0], lines[1:4]
            third_task_id = task_ids[2]

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)
                # Naming the third task WHILE the first runs: tasks 1 and 2 are not
                # in this pause's withheld set (LINEAR: only the paused task and
                # what follows it in plan order are withheld).
                status, body = _post(port, token, "job.pause", job_id=job_id,
                                     nonce="n-pause-task", args={"task": third_task_id})
                assert status == 200, body
                assert (body["outcome"], body["task_id"]) == ("paused", third_task_id), body
                assert len(_events(data_dir, job_id, "task_paused")) == 1
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:paused" in out, f"{out}\nstderr:\n{err}"
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        data = _job_data(data_dir, job_id)
        assert data["status"] == "paused"
        assert data["pause"]["scope"] == "task"
        statuses = [t["status"] for t in data["tasks"]]
        assert statuses[0] == "applied_to_job_workspace"
        assert statuses[1] == "applied_to_job_workspace"
        assert statuses[2] == "pending"                     # withheld, never dispatched

        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.unpause", job_id=job_id,
                                 nonce="n-unpause-task", args={"task": third_task_id})
            assert status == 200, body
            assert (body["outcome"], body["task_id"]) == ("released", third_task_id), body
            assert len(_events(data_dir, job_id, "task_resumed")) == 1

            from packages.orchestration.pingpong_job import JOB_COMPLETED, run_job
            from packages.orchestration.pingpong_provider import FakeProvider

            resumed = run_job(
                job_id,
                builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                repair_rounds=0)
            assert resumed.state == JOB_COMPLETED
            assert all(t.status == "applied_to_job_workspace" for t in resumed.tasks)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# L3 — refusals; no live runner needed, the effect declines before any call
# ---------------------------------------------------------------------------


class TestRefusalsLiveDoor:
    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

        self.job = JobPlan(job_title="live-refusals-job",
                           user_prompt="Test prompt for the pause door refusals",
                           tasks=[TaskEntry(title="Write a README")])
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"

    def test_an_unknown_task_is_409_and_audited_rejected_state(self):
        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = _post(port, token, "job.pause", job_id=self.job_id,
                             nonce="n-unknown-task", args={"task": "not-a-real-task"})
        assert status == 409, body
        assert "not-a-real-task" not in json.dumps(body), body
        assert _audit_outcomes(self.control, self.job_id) == ["rejected_state"]

    def test_a_completed_job_is_409_and_audited_rejected_state(self):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import save_job_plan

        self.job.state = RunState.COMPLETED
        save_job_plan(self.job)

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = _post(port, token, "job.pause", job_id=self.job_id,
                             nonce="n-completed")
        assert status == 409, body
        assert _audit_outcomes(self.control, self.job_id) == ["rejected_state"]

    def test_a_completed_job_refuses_unpause_too(self):
        from packages.core.models import RunState
        from packages.orchestration.pingpong_job import save_job_plan

        self.job.state = RunState.COMPLETED
        save_job_plan(self.job)

        port, token = _start_ui_server_for_job(self.job_id, self.tmp_path)
        status, body = _post(port, token, "job.unpause", job_id=self.job_id,
                             nonce="n-completed-unpause")
        assert status == 409, body
        assert _audit_outcomes(self.control, self.job_id) == ["rejected_state"]


# ---------------------------------------------------------------------------
# L4 — withdraw a pause the job never reached; no live runner needed
# ---------------------------------------------------------------------------


class TestWithdrawLiveDoor:
    def test_a_withdrawn_pause_never_parks_the_relaunch(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import (
            JOB_COMPLETED,
            JobPlan,
            TaskEntry,
            run_job,
            save_job_plan,
        )
        from packages.orchestration.pingpong_provider import FakeProvider

        # R-1072: a target of its own — without it the runner builds a git
        # worktree of the whole live checkout, which fails under load.
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")

        job = JobPlan(job_title="live-withdraw-job",
                     user_prompt="Test prompt for the pause door withdraw",
                     tasks=[TaskEntry(title="Write a README")],
                     repo_path=str(target))
        save_job_plan(job)
        job_id = str(job.job_id)

        port, token = _start_ui_server_for_job(job_id, tmp_path)
        status, body = _post(port, token, "job.pause", job_id=job_id, nonce="n-request")
        assert status == 200, body
        assert body["outcome"] == "requested", body

        status, body = _post(port, token, "job.unpause", job_id=job_id, nonce="n-withdraw")
        assert status == 200, body
        assert body["outcome"] == "withdrawn", body

        final = run_job(job_id,
                        builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                        reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                        repair_rounds=0)
        assert final.state == JOB_COMPLETED
        assert all(t.status == "applied_to_job_workspace" for t in final.tasks)
