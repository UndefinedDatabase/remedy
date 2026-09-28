"""F038 T003 — THE END-TO-END PROOF (S3): a question answered with its citations, "stop that
task" as a card, the card confirmed through the write door, and the job stopping with exactly
one accepted audit line.

Modelled on `test_pause_door_live.py`'s `TestJobScopeLiveDoor`, owning its own copies of that
file's helpers — each live test file owns its own copy, the established convention there. A
three-task job runs under `run_job`, in ITS OWN PROCESS, with a `SlowProvider` whose SECOND
build call — task 2's first — writes a `building` file under `tmp_path` and then waits for a
`go` file before it proceeds, so the stop posted through the chat card can never race the job's
end. A real UI server runs IN this test process, in a background thread, over the SAME
REMEDY_DATA_DIR the subprocess runner writes into.
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
from urllib.parse import urlencode

import psutil
import pytest

from packages.orchestration.data_paths import job_record_path

CSRF_HEADER = "X-Remedy-CSRF"

_THREE_TASK_JOB = """\
# Job: Chat E2E Test

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

_RUNNER = """\
import sys, time
from pathlib import Path
sys.path.insert(0, {repo!r})
from packages.orchestration.pingpong_job import parse_job_file, run_job
from packages.orchestration.pingpong_provider import FakeProvider


class SlowProvider(FakeProvider):
    '''A provider whose SECOND build call — task 2's first — writes `building` and waits for
    `go` before it proceeds, so the chat-posted stop can never race the job's end (S3).'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_calls = 0

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        if self.build_calls == 2:
            Path({building!r}).write_text("building")
            deadline = time.monotonic() + 60.0
            while not Path({go!r}).is_file():
                if time.monotonic() > deadline:
                    raise RuntimeError("go never appeared")
                time.sleep(0.02)
        return super().build(prompt, **kwargs)


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
"""


def _test_owned_children(baseline_pids: set[int], tmp_path: Path) -> list[psutil.Process]:
    """Children this TEST is responsible for — nobody else's. Mirrors
    `test_pause_door_live.py`'s own helper of the same name exactly."""
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
    """Start a real UI server for `job_id` in a thread and return `(port, token)`. Mirrors
    `test_pause_door_live.py`'s helper of the same name and purpose."""
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


def _get_chat(port: int, token: str, job_id: str, *, text: str, task: str) -> tuple[int, dict]:
    query = urlencode({"token": token, "text": text, "task": task})
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("GET", f"/api/jobs/{job_id}/chat?{query}")
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read())
    finally:
        conn.close()


def _post(port: int, token: str, command: str, *, job_id: str, nonce: str,
         args: dict | None = None) -> tuple[int, dict]:
    """Mirrors `test_pause_door_live.py`'s own `_post` helper exactly."""
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


def _audit_lines(control_root: Path, job_id: str) -> list[dict]:
    from packages.orchestration.command_audit import AUDIT_FILENAME

    path = control_root / "jobs" / job_id / AUDIT_FILENAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_bytes().splitlines()]


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


@pytest.mark.subprocess
class TestChatE2ELiveDoor:
    def test_an_answer_with_citations_a_stop_card_and_one_accepted_audit_line(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        metafile = tmp_path / "meta.txt"
        building_file = tmp_path / "building"
        go_file = tmp_path / "go"
        script = tmp_path / "runner.py"
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            metafile=str(metafile), building=str(building_file), go=str(go_file)))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        baseline = {c.pid for c in psutil.Process().children(recursive=True)}
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        job_id = ""
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
            task1_id, task2_id = task_ids[0], task_ids[1]

            # Task 2's build call is IN FLIGHT: task 1 is durably applied and the stop
            # posted below can never race the job's end.
            deadline = time.monotonic() + 60.0
            while time.monotonic() < deadline:
                if building_file.is_file():
                    break
                assert proc.poll() is None, "the runner exited before task 2's build call began"
                time.sleep(0.02)
            else:
                pytest.fail("task 2's build call never began within 60s")

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)

                status, body = _get_chat(port, token, job_id,
                                         text="Did the tests pass?", task=task1_id)
                assert status == 200, body
                assert body["available"] is True, body
                assert body["kind"] == "answer", body
                assert body["scope"] == "node", body
                assert body["subject"] == task1_id, body
                assert len(body["evidence"]) >= 1, body
                item_count = len(body["evidence"])
                for sentence in body["sentences"]:
                    if sentence["text"] == "Not in evidence.":
                        assert sentence["citations"] == [], sentence
                    else:
                        assert sentence["citations"], sentence
                        assert all(1 <= c <= item_count for c in sentence["citations"]), sentence

                status, card = _get_chat(port, token, job_id,
                                         text="stop that task", task=task2_id)
                assert status == 200, card
                assert card["available"] is True, card
                assert card["kind"] == "card", card
                assert card["verb"] == "job.stop", card
                assert card["confirmable"] is True, card

                control_root = data_dir / "control"
                assert _audit_lines(control_root, job_id) == []

                status, result = _post(port, token, card["verb"], job_id=job_id,
                                       nonce="chat-e2e-stop", args=card["args"])
                assert status == 200, result
                assert result["outcome"] == "accepted", result
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            go_file.write_text("go")

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:stopped" in out, out
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        data = _job_data(data_dir, job_id)
        assert data["status"] == "stopped"

        assert len(_events(data_dir, job_id, "job_stopped")) == 1

        control_root = data_dir / "control"
        audit = _audit_lines(control_root, job_id)
        assert len(audit) == 1, audit
        assert audit[0]["command"] == "job.stop", audit
        assert audit[0]["outcome"] == "accepted", audit
        assert audit[0]["nonce"] == "chat-e2e-stop", audit

        assert not psutil.pid_exists(proc.pid) or \
            psutil.Process(proc.pid).status() == psutil.STATUS_ZOMBIE
        assert _test_owned_children(baseline, tmp_path) == []
