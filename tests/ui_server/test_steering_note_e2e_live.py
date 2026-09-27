"""F030 R4 T003 — a steering note through the write door, end to end, against a real job run.

A note addressed to the running task while its round 1 build call is held in flight reaches
that task's next round and the stream (SCENARIO A, TAKEN IN); a note whose task passes in the
round it arrived in is never taken in, never reaches another task, and is listed by the job
report and by `remedy chat show` (SCENARIO B, NOT TAKEN IN). DECISION F030 D1 (the address),
D2 (the write door) and D3 (the stream's `note` field) are all exercised through their real
production paths — the write door's `job.steer`, the ping-pong loop's own consumption at the
top of a round, and `events-since`, the same route the cockpit's stream uses.

Structured like `test_pause_e2e_live.py`'s own classes — `@pytest.mark.subprocess`, a real
job run in a subprocess, a real UI server started in a thread, and a real POST through
`HTTPConnection` — and this file keeps its OWN copies of that file's `_RUNNER` shape,
`_start_ui_server_for_job` and `_post`, per that file's own header rule ("each live test file
owns its own copies of that file's helpers... the established convention here"), rather than
importing them. `_all_events_since` is new to this file (the model reads its run log directly;
this file reads the same events through the live write door's own `events-since` route,
because DECISION F030 D3's `note` field is a property of THAT envelope, not of the run log).

The one change to the model's runner: the provider is `HandshakeFakeProvider(FakeProvider)`,
built with the pass round each scenario names. `create_provider` builds a FRESH provider for
every task, so its `build` holds only the FIRST call of the whole runner process — the first
task's round 1 — in flight: it writes `<tmp>/building`, then polls for `<tmp>/go` before
calling `FakeProvider.build`. A module-level flag is what keeps this to one call; a task's own
repair round and every other task's round 1 pass straight through untouched.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.data_paths import job_record_path, run_dir
from packages.orchestration.prompt_segments import SegmentStabilityRank

CSRF_HEADER = "X-Remedy-CSRF"

_TWO_TASK_JOB = """\
# Job: Steering Note E2E Test

## Task 1
Add module one.

Acceptance:
- module exists

## Task 2
Add module two.

Acceptance:
- module exists
"""

#: `create_provider("fake")` builds a fresh provider for every task, so the runner's FIRST
#: build call is the first task's round 1 — the one call this handshake holds in flight.
_RUNNER = """\
import sys, time
from pathlib import Path
sys.path.insert(0, {repo!r})
from packages.orchestration.pingpong_job import parse_job_file, run_job
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration import pingpong_loop

_did_handshake = False


class HandshakeFakeProvider(FakeProvider):
    '''Holds ONLY the runner process's first build call in flight — a module-level flag,
    since `create_provider` mints a fresh provider per task and per call site. It writes
    `<tmp>/building`, then polls every 0.05s for up to 60s until `<tmp>/go` exists, before
    calling `FakeProvider.build`. Every other call (this task's own repair round, or any
    other task's round 1) passes straight through untouched.'''

    def build(self, prompt, **kwargs):
        global _did_handshake
        if not _did_handshake:
            _did_handshake = True
            Path({building!r}).write_text("1")
            deadline = time.monotonic() + 60.0
            while not Path({go!r}).exists() and time.monotonic() < deadline:
                time.sleep(0.05)
        return super().build(prompt, **kwargs)


_real_create_provider = pingpong_loop.create_provider


def _handshake_create_provider(name, **kwargs):
    if name == "fake":
        return HandshakeFakeProvider(pass_on_round={pass_round!r})
    return _real_create_provider(name, **kwargs)


pingpong_loop.create_provider = _handshake_create_provider

job = parse_job_file(Path({job_file!r}).read_text(), {target!r})
with Path({metafile!r}).open("w") as f:
    f.write(job.job_id + chr(10))
    for task in job.tasks:
        f.write(task.task_id + chr(10))

final = run_job(job.job_id, builder_name="fake", reviewer_name="fake")
print("FINAL:" + final.state, flush=True)
"""


# ---------------------------------------------------------------------------
# Helpers — own copies of test_pause_e2e_live.py's, per that file's header rule
# ---------------------------------------------------------------------------


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`.

    Mirrors `test_pause_e2e_live.py`'s helper of the same name and purpose — each live
    test file owns its own copy, the established convention here.
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


def _job_data(data_dir: Path, job_id: str) -> dict:
    return json.loads(job_record_path(job_id, data_dir).read_text())


# ---------------------------------------------------------------------------
# Helpers new to THIS file — the live write door's own events-since route
# ---------------------------------------------------------------------------


def _all_events_since(port: int, token: str, job_id: str) -> list[dict]:
    """Every event `events-since` will hand back, paged from cursor 0 — mirrors
    `test_task_veto_e2e_live.py`'s own helper exactly. This is the same route the
    cockpit's stream uses, and the one DECISION F030 D3's `note` field belongs to."""
    events: list[dict] = []
    cursor = "0"
    while True:
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("GET", f"/api/jobs/{job_id}/events-since?token={token}&cursor={cursor}")
            resp = conn.getresponse()
            assert resp.status == 200
            body = json.loads(resp.read())
        finally:
            conn.close()
        events.extend(body["events"])
        next_cursor = body["cursor"]
        if next_cursor == cursor or not body["events"]:
            break
        cursor = next_cursor
    return events


def _prompt_trace(data_dir: Path, run_id: str) -> list[dict]:
    """The run's own recorded prompt trace, read from its run directory (F105)."""
    path = run_dir(run_id, data_dir) / "prompt_trace.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _run_two_task_job(repo_root: Path, tmp_path: Path, *, pass_round: int,
                      label: str) -> tuple[subprocess.Popen, Path, Path, Path]:
    """Start the runner subprocess for a fresh two-task job under its own `tmp_path`
    subtree, and return `(proc, data_dir, building_file, go_file)`. The caller owns
    waiting for `building`, posting through the write door, creating `go`, and reaping
    `proc` by its own pid."""
    root = tmp_path / label
    root.mkdir()
    target = root / "repo"
    target.mkdir()
    (target / "README.md").write_text("# demo\n")
    data_dir = root / "remedy_data"
    data_dir.mkdir()

    job_file = root / "job.md"
    job_file.write_text(_TWO_TASK_JOB)
    metafile = root / "meta.txt"
    building = root / "building"
    go = root / "go"
    script = root / "runner.py"
    script.write_text(textwrap.dedent(_RUNNER).format(
        repo=str(repo_root), job_file=str(job_file), target=str(target),
        metafile=str(metafile), building=str(building), go=str(go),
        pass_round=pass_round))

    env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
    proc = subprocess.Popen([sys.executable, str(script)], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc, data_dir, metafile, building, go


def _wait_for_file(path: Path, proc: subprocess.Popen, what: str, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.is_file() and path.read_text().strip():
            return
        assert proc.poll() is None, f"the runner exited before writing {what}"
        time.sleep(0.02)
    pytest.fail(f"the runner never wrote {what} within {timeout}s")


# ---------------------------------------------------------------------------
# SCENARIO A — TAKEN IN
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestSteeringNoteTakenInLive:
    def test_a_note_posted_mid_call_is_taken_in_at_round_two_and_reaches_the_stream(
        self, tmp_path,
    ):
        repo_root = Path(__file__).resolve().parents[2]
        note = "Add a trailing newline before you finish."
        proc, data_dir, metafile, building, go = _run_two_task_job(
            repo_root, tmp_path, pass_round=2, label="a")
        try:
            _wait_for_file(metafile, proc, "the metafile")
            lines = metafile.read_text().splitlines()
            job_id, t1, t2 = lines[0], lines[1], lines[2]

            _wait_for_file(building, proc, "the building marker")

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)
                status, body = _post(port, token, "job.steer", job_id=job_id,
                                     nonce="n-steer-a", args={"task_id": t1, "message": note})
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)
            assert status == 200, body
            assert body["outcome"] == "accepted", body
            assert body["task_id"] == t1, body
            message_id = body["message_id"]

            go.write_text("1")

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:" in out, out
            assert "FINAL:completed" in out, out
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        # --- the prompt trace: round 1 untouched, round 2 carries the note ---
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.orchestration.pingpong_job import load_job_plan
            job = load_job_plan(job_id)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)
        assert job is not None
        t1_run_id = next(t.run_id for t in job.tasks if t.task_id == t1)
        t2_run_id = next(t.run_id for t in job.tasks if t.task_id == t2)

        t1_trace = _prompt_trace(data_dir, t1_run_id)
        t1_builder = sorted((e for e in t1_trace if e["role"] == "builder"),
                            key=lambda e: e["round"])
        assert [e["round"] for e in t1_builder] == [1, 2]
        round1, round2 = t1_builder
        round1_names = [row["name"] for row in round1["segment_manifest"]]
        assert "builder_operator_notes" not in round1_names
        if round1.get("prompt_text_unavailable_reason"):
            pytest.fail(
                "the recorded trace does not record prompt text at all "
                f"({round1['prompt_text_unavailable_reason']}); asserting the manifest "
                "rows alone per the block's fallback clause")
        assert note not in round1["prompt_text_redacted"]

        round2_notes_rows = [r for r in round2["segment_manifest"]
                             if r["name"] == "builder_operator_notes"]
        assert len(round2_notes_rows) == 1, round2["segment_manifest"]
        assert round2_notes_rows[0]["rank"] == int(SegmentStabilityRank.STEERING)
        assert note in round2["prompt_text_redacted"]

        t2_trace = _prompt_trace(data_dir, t2_run_id)
        t2_builder = [e for e in t2_trace if e["role"] == "builder"]
        assert t2_builder
        for entry in t2_builder:
            names = [row["name"] for row in entry["segment_manifest"]]
            assert "builder_operator_notes" not in names
            assert note not in entry.get("prompt_text_redacted", "")

        # --- the consumption marker: names the first task and round 2 ---
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.orchestration import steering as ST
            markers = ST.list_steering_consumptions(job_id, root=data_dir)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)
        [marker] = list(markers.values())
        assert marker["task_id"] == t1
        assert marker["round_number"] == 2

        # --- the stream, through the real events-since route ---
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            events = _all_events_since(port, token, job_id)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        steering_kinds = {"steering_message_received", "steering_message_consumed"}
        received = [e for e in events if e["event"] == "steering_message_received"]
        consumed = [e for e in events if e["event"] == "steering_message_consumed"]
        assert len(received) == 1, received
        assert len(consumed) == 1, consumed
        assert received[0]["note"] == {
            "message_id": message_id, "text": note, "channel": "cockpit", "task_id": t1,
        }
        assert consumed[0]["steering"]["round_number"] == 2
        recv_seq = received[0]["seq"]
        cons_seq = consumed[0]["seq"]
        assert recv_seq < cons_seq

        t1_later_non_steering = [
            e for e in events
            if e.get("task_id") == t1 and e["seq"] > cons_seq and e["event"] not in steering_kinds
        ]
        assert t1_later_non_steering, "no builder action recorded after consumption"

        for event in events:
            if event["event"] not in steering_kinds:
                assert note not in json.dumps(event), event


# ---------------------------------------------------------------------------
# SCENARIO B — NOT TAKEN IN
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestSteeringNoteNotTakenInLive:
    def test_a_note_whose_task_passes_in_round_one_is_never_taken_in(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        note = "Keep the diff under ten lines."
        proc, data_dir, metafile, building, go = _run_two_task_job(
            repo_root, tmp_path, pass_round=1, label="b")
        try:
            _wait_for_file(metafile, proc, "the metafile")
            lines = metafile.read_text().splitlines()
            job_id, t1, t2 = lines[0], lines[1], lines[2]

            _wait_for_file(building, proc, "the building marker")

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)
                status, body = _post(port, token, "job.steer", job_id=job_id,
                                     nonce="n-steer-b", args={"task_id": t1, "message": note})
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)
            assert status == 200, body
            assert body["outcome"] == "accepted", body
            message_id = body["message_id"]

            go.write_text("1")

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:completed" in out, out
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.orchestration import steering as ST
            markers = ST.list_steering_consumptions(job_id, root=data_dir)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)
        assert markers == {}

        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.orchestration.pingpong_job import load_job_plan
            job = load_job_plan(job_id)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)
        assert job is not None
        t1_run_id = next(t.run_id for t in job.tasks if t.task_id == t1)
        t2_run_id = next(t.run_id for t in job.tasks if t.task_id == t2)

        for run_id in (t1_run_id, t2_run_id):
            for entry in _prompt_trace(data_dir, run_id):
                if entry["role"] != "builder":
                    continue
                names = [row["name"] for row in entry["segment_manifest"]]
                assert "builder_operator_notes" not in names
                assert note not in entry.get("prompt_text_redacted", "")

        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.orchestration.pingpong_job import export_job_report, format_job_report_text
            report = export_job_report(job)
            report_text = format_job_report_text(job)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        by_task = {t["task_id"]: t for t in report["tasks"]}
        assert by_task[t1]["steering_not_consumed"] == [
            {"message_id": message_id, "text": note,
             "received_at": by_task[t1]["steering_not_consumed"][0]["received_at"]}
        ]
        assert "steering_not_consumed" not in by_task[t2]
        assert f"      Steering not consumed: “{note}”" in report_text

        show_env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        show_proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "chat", "show", job_id, "--json"],
            cwd=str(repo_root), env=show_env, capture_output=True, text=True, timeout=60)
        assert show_proc.returncode == 0, (
            f"chat show exited {show_proc.returncode}: {show_proc.stderr}")
        show_body = json.loads(show_proc.stdout)
        [row] = [m for m in show_body["messages"] if m["message_id"] == message_id]
        assert row["status"] == "not_taken_in", row
        assert row["addressed_to"] == t1, row
