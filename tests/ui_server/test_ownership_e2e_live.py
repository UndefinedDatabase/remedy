"""F035 R7 T003, DECISION F035 D7 — the ownership ledger end to end: one real job, acted on
through both doors, whose ledger file, `remedy job ownership`, the browser's `ownership` route
and the job report all agree entry for entry, sentence for sentence and task for task.

A three-task job runs in a subprocess with a fake provider held at its FIRST build call
(`HandshakeFakeProvider`, mirroring `test_steering_note_e2e_live.py`'s own one — a module-level
flag, since `create_provider` mints a fresh provider per task and per call site). While that
call is held, five actions land in this order: through the door, with one real token,
`job.veto-task` of the THIRD task with a reason, then `chat.send` with a job-wide message; on
the real command line, `remedy job steer` addressing a note to the SECOND task, then `remedy
job pause --task` and `remedy job unpause --task` of the same task. The run is then released and
completes normally — the pause and its immediate release both land before the second task is
ever dispatched, so nothing parks and no relaunch is needed (`pause_control.pause_job_command`
and `unpause_job_command` are pure control-file writes, never a waiting process).

Structured like `test_steering_note_e2e_live.py` and `test_pause_e2e_live.py` — `@pytest.mark.
subprocess`, its own runner, server starter and door helper — and this file keeps its OWN
copies of those files' `_start_ui_server_for_job` and `_post`, per their shared header rule
("each live test file owns its own copies of that file's helpers... the established convention
here"), and its own `_get_json`, mirroring `test_task_veto_e2e_live.py`'s.

DEVIATION FROM DECISION F035 D7's PROSE (declared in the round 7 handback): the decision's own
words group "the veto and the message" together under one phrase, `You (browser, token #1)`.
Measured at this branch's HEAD, `_dispatch_chat_send` in `packages/orchestration/ui_server.py`
hardcodes `channel="cockpit"` for `chat.send` rather than the token fingerprint
`_dispatch_job_veto_task` passes — only `ownership_actor` calls carrying a `tf:`-prefixed
`recorded_as` earn a token number (`build_ownership_ledger`'s own numbering rule), so the
job-wide message's own sentence reads `You (browser)`, with no number, while the veto alone
reads `You (browser, token #1)`. This file asserts the MEASURED sentence, not the decision's
prose, per the F035 R4 precedent (DECISION F035 D5) for a block's own prose outrun by the code
it describes.
"""
from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import textwrap
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.data_paths import job_evidence_export_dir, job_record_path

CSRF_HEADER = "X-Remedy-CSRF"

_THREE_TASK_JOB = """\
# Job: Ownership E2E Test

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

VETO_REASON = "duplicates the work task one already does"
CHAT_MESSAGE = "Keep every diff small."
STEER_NOTE = "Double-check the acceptance wording before you finish."
PAUSE_REASON = "waiting on a design review"

#: `create_provider("fake")` builds a fresh provider for every task, so the runner's FIRST
#: build call is the first task's round 1 — the one call this handshake holds in flight,
#: exactly as `test_steering_note_e2e_live.py`'s own `HandshakeFakeProvider` does. No
#: `pass_on_round` override: `FakeProvider`'s own defaults (round 1 fails review, round 2
#: repairs and passes) give the first task a second round — the safe point that consumes the
#: job-wide message this test sends while round 1 is held.
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
    calling `FakeProvider.build`. Every other call passes straight through untouched.'''

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
        return HandshakeFakeProvider()
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
# Helpers — own copies of the sibling live test files', per their own header rule
# ---------------------------------------------------------------------------


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`."""
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


def _get_json(port: int, token: str, job_id: str, endpoint: str) -> dict:
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("GET", f"/api/jobs/{job_id}/{endpoint}?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        return json.loads(resp.read())
    finally:
        conn.close()


def _job_data(data_dir: Path, job_id: str) -> dict:
    return json.loads(job_record_path(job_id, data_dir).read_text())


def _wait_for_file(path: Path, proc: subprocess.Popen, what: str, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if path.is_file() and path.read_text().strip():
            return
        assert proc.poll() is None, f"the runner exited before writing {what}"
        time.sleep(0.02)
    pytest.fail(f"the runner never wrote {what} within {timeout}s")


# ---------------------------------------------------------------------------
# Helper new to THIS file — `ownershipEntriesForTask`'s own rule, in Python (S3 (e))
# ---------------------------------------------------------------------------


def _entries_for_task(entries: list[dict], task_id: str) -> list[dict]:
    """`ownershipEntriesForTask` in `apps/ui/src/api/ownership.ts`, ported: an entry belongs
    to a task when it names the task directly or names it in its consequence's task ids; ""
    names no task at all."""
    if task_id == "":
        return []
    return [e for e in entries
            if e["task_id"] == task_id or task_id in e["consequence"]["task_ids"]]


@pytest.mark.subprocess
class TestOwnershipE2ELive:
    def test_one_job_through_both_doors_agrees_entry_for_entry(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        metafile = tmp_path / "meta.txt"
        building = tmp_path / "building"
        go = tmp_path / "go"
        script = tmp_path / "runner.py"
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            metafile=str(metafile), building=str(building), go=str(go)))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            _wait_for_file(metafile, proc, "the metafile")
            lines = metafile.read_text().splitlines()
            job_id, t1, t2, t3 = lines[0], lines[1], lines[2], lines[3]

            _wait_for_file(building, proc, "the building marker")

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)

                # --- through the door, one real token: veto the THIRD task -----------
                status, body = _post(port, token, "job.veto-task", job_id=job_id,
                                     nonce="n-veto",
                                     args={"task_id": t3, "reason": VETO_REASON})
                assert status == 200, body
                assert body["outcome"] == "vetoed", body

                # --- through the SAME door: a job-wide steering message ---------------
                status, body = _post(port, token, "chat.send", job_id=job_id,
                                     nonce="n-chat", args={"message": CHAT_MESSAGE})
                assert status == 200, body
                assert body["outcome"] == "accepted", body
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            # --- on the real command line: a note addressed to the SECOND task --------
            steer = subprocess.run(
                [sys.executable, "-m", "apps.cli.main", "job", "steer", job_id, STEER_NOTE,
                 "--task", t2],
                cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=60)
            assert steer.returncode == 0, f"job steer exited {steer.returncode}: {steer.stderr}"

            # --- on the real command line: pause, then release, the SECOND task -------
            pause = subprocess.run(
                [sys.executable, "-m", "apps.cli.main", "job", "pause", job_id,
                 "--task", t2, "--reason", PAUSE_REASON],
                cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=60)
            assert pause.returncode == 0, f"job pause exited {pause.returncode}: {pause.stderr}"

            unpause = subprocess.run(
                [sys.executable, "-m", "apps.cli.main", "job", "unpause", job_id,
                 "--task", t2],
                cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=60)
            assert unpause.returncode == 0, (
                f"job unpause exited {unpause.returncode}: {unpause.stderr}")

            # --- release the held build call; the run finishes on its own -------------
            go.write_text("1")

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            # The run ends with exit 0 (S3's own words) but not necessarily
            # "completed": the veto of the third task is never answered by a
            # `decision.resolve` in this run (S3 orders no such step), and
            # `pingpong_job.py`'s own veto-terminal check blocks a job whose
            # vetoed task carries no settled answer — measured, not assumed,
            # since the block's own text never claims a final state.
            assert "FINAL:" in out, out
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        data = _job_data(data_dir, job_id)
        assert data["status"] == "blocked"
        assert data["error"] == f"all_remaining_work_vetoed: vetoed {t3}; unreachable none"

        # ------------------------------------------------------------------------
        # (a) the evidence export's ownership.json equals build_ownership_ledger of
        #     the finished job
        # ------------------------------------------------------------------------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.orchestration.ownership import build_ownership_ledger
            from packages.orchestration.ownership_phrases import ownership_view
            from packages.orchestration.pingpong_job import (
                format_job_report_text,
                load_job_plan,
            )
            job = load_job_plan(job_id)
            assert job is not None
            rebuilt = build_ownership_ledger(job)
            view = ownership_view(job)
            report_text = format_job_report_text(job)
            from packages.orchestration import steering as ST
            markers = ST.list_steering_consumptions(job_id, root=data_dir)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        assert view["error"] == ""
        exported = json.loads(
            (job_evidence_export_dir(job_id, data_dir) / "ownership.json").read_text())
        assert exported == rebuilt

        entries = view["entries"]
        titles = {t.task_id: t.title for t in job.tasks}

        # ------------------------------------------------------------------------
        # (c) the actions, in the ledger's order, are exactly the five this run made
        # ------------------------------------------------------------------------
        assert [e["action"] for e in entries] == [
            "task_vetoed", "steering_sent", "note_sent", "task_paused", "task_resumed",
        ]
        veto_entry, chat_entry, note_entry, pause_entry, resume_entry = entries

        # ------------------------------------------------------------------------
        # (b) `remedy job ownership --json` and the browser's route answer the same
        #     entries, each the file's entry plus its sentence
        # ------------------------------------------------------------------------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            route_body = _get_json(port, token, job_id, "ownership")
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)
        assert route_body["error"] == ""
        assert route_body["entries"] == entries

        ownership_cmd = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "ownership", job_id, "--json"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=60)
        assert ownership_cmd.returncode == 0, (
            f"job ownership exited {ownership_cmd.returncode}: {ownership_cmd.stderr}")
        cli_body = json.loads(ownership_cmd.stdout)
        assert cli_body["entries"] == entries
        assert cli_body["entries"] == route_body["entries"]

        # ------------------------------------------------------------------------
        # each sentence equals a literal this test writes out, whose consumption
        # clauses name the task and round the run's OWN markers record (S3 (c))
        # ------------------------------------------------------------------------
        chat_message_id = chat_entry["record_ref"].split(":", 1)[1]
        note_message_id = note_entry["record_ref"].split(":", 1)[1]
        chat_marker = markers.get(chat_message_id)
        note_marker = markers.get(note_message_id)

        def _title(task_id: str) -> str:
            return titles.get(task_id, task_id)

        expected_veto = (
            f"You (browser, token #1) vetoed task {t3} ({_title(t3)}) — reason: "
            f"“{VETO_REASON}”."
        )
        if chat_marker is not None:
            consumer_task = chat_marker["task_id"]
            expected_chat = (
                f"You (browser) sent a steering message: “{CHAT_MESSAGE}”. "
                f"Task {consumer_task} ({_title(consumer_task)}) took it in at "
                f"round {chat_marker['round_number']}."
            )
        else:
            expected_chat = (
                f"You (browser) sent a steering message: “{CHAT_MESSAGE}”. "
                "No task has taken it in yet."
            )
        assert note_marker is not None, "the note to the second task was never taken in"
        expected_note = (
            f"You (command line) sent a note to task {t2} ({_title(t2)}): "
            f"“{STEER_NOTE}”. It was taken in at round {note_marker['round_number']}."
        )
        expected_pause = (
            f"You (command line) paused task {t2} ({_title(t2)}) — reason: "
            f"“{PAUSE_REASON}”."
        )
        expected_resume = f"You resumed task {t2} ({_title(t2)})."

        assert veto_entry["sentence"] == expected_veto
        assert chat_entry["sentence"] == expected_chat
        assert note_entry["sentence"] == expected_note
        assert pause_entry["sentence"] == expected_pause
        assert resume_entry["sentence"] == expected_resume

        # ------------------------------------------------------------------------
        # (d) `format_job_report_text` holds "Ownership:" and the five sentences,
        #     in that order
        # ------------------------------------------------------------------------
        expected_block = ["Ownership:"] + [
            f"  - {s}" for s in
            [expected_veto, expected_chat, expected_note, expected_pause, expected_resume]
        ]
        report_lines = report_text.splitlines()
        assert "Ownership:" in report_lines
        idx = report_lines.index("Ownership:")
        assert report_lines[idx:idx + len(expected_block)] == expected_block

        # ------------------------------------------------------------------------
        # (e) the entries per task, by `ownershipEntriesForTask`'s own rule: the
        #     veto for the third task, the note/pause/resume for the second, and
        #     for the first only the job-wide message if its round took it in
        # ------------------------------------------------------------------------
        assert _entries_for_task(entries, t3) == [veto_entry]
        assert _entries_for_task(entries, t2) == [note_entry, pause_entry, resume_entry]
        expected_t1 = [chat_entry] if t1 in chat_entry["consequence"]["task_ids"] else []
        assert _entries_for_task(entries, t1) == expected_t1
