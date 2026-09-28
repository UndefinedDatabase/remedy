"""F038 T003 — `remedy chat ask <job_id> "<text>" [--task <task id>] [--yes] [--json]` runs one
chat turn: a question prints its scope, its checked answer and its numbered evidence; a card
prints its title and lines and is sent through the job's running cockpit only when confirmable
and confirmed (DECISION F038 D10).

Temporary data roots only. No provider call is ever made: `chat.model_written` stays off, so
every question here is answered mechanically.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from apps.cli.grouped import main as grouped_main
from packages.core.models import RunState
from packages.orchestration import steering as ST
from packages.orchestration.command_audit import AUDIT_FILENAME
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.ui_server import start_ui_server
from tests.ui_server.server_start import wait_for_server_info


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _run(argv: list[str]) -> int:
    try:
        grouped_main(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


def _job() -> tuple[JobPlan, str]:
    """A saved RUNNING job of one done, passing task (the block's own fixture shape)."""
    task = TaskEntry(title="Write the README", status="done", test_passed=True)
    job = JobPlan(
        job_title="f038-chat-ask-job", tasks=[task], state=RunState.RUNNING,
        metadata={"target_repo": "/tmp/repo"},
    )
    save_job_plan(job)
    return job, task.task_id


def _audit_path(job_id: str) -> Path:
    return Path(resolve_data_root()) / "control" / "jobs" / job_id / AUDIT_FILENAME


def _audit_lines(job_id: str) -> list[dict]:
    path = _audit_path(job_id)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def _sessions_dir() -> Path:
    d = Path(resolve_data_root()) / "ui" / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _start_live_cockpit(job_id: str, capsys) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a background thread, publishing its info
    file directly INTO the UI session registry — as `remedy ui start` does — so
    `live_ui_session_for_job` finds it and its `pid` is this test process (mirrors
    `tests/orchestration/test_chat_door.py`'s own `_start_ui_server_for_job`).

    The server thread shares this process's stdout with `capsys`, so its own startup
    line is drained here — before the caller's own command runs — rather than leaking
    into the caller's captured output.
    """
    info_file = str(_sessions_dir() / f"{job_id}.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file, json_output=True)
        except (SystemExit, KeyboardInterrupt):
            pass

    t = threading.Thread(target=run, daemon=True)
    t.start()
    info = wait_for_server_info(info_file, t)
    capsys.readouterr()
    return info["port"], token


def _dead_pid() -> int:
    """A PID that has already exited: a child process spawned and reaped."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


# ---------------------------------------------------------------------------
# S5 — a question is answered from its evidence.
# ---------------------------------------------------------------------------


class TestChatAskAnswer:
    def test_a_focused_question_answers_from_the_node_scope(self, capsys):
        job, task_id = _job()
        assert _run(["chat", "ask", job.job_id, "Did the tests pass?", "--task", task_id,
                    "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is True
        assert out["kind"] == "answer"
        assert out["scope"] == "node"
        assert out["subject"] == task_id
        assert out["evidence"]

    def test_an_unfocused_question_says_not_in_evidence(self, capsys):
        job, _task_id = _job()
        assert _run(["chat", "ask", job.job_id, "What is the roadmap position?"]) == 0
        text = capsys.readouterr().out
        assert "Scope: project" in text
        assert "Not in evidence." in text

    def test_a_padded_task_is_answered_in_the_node_scope_with_the_bare_id_as_subject(self, capsys):
        # R-1094: a `--task` naming a real task, padded with spaces, is stripped before it
        # is matched, so the answer still comes back from that task's node scope.
        job, task_id = _job()
        assert _run(["chat", "ask", job.job_id, "Did the tests pass?",
                    "--task", f"  {task_id}  ", "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["scope"] == "node"
        assert out["subject"] == task_id

    def test_a_focused_questions_text_form_names_how_the_answer_was_written(self, capsys):
        # DECISION F038 D13: the text form's line right after `Scope:` says how the
        # answer was written; no model call is ever made here, so it is the mechanical
        # sentence exactly.
        from packages.orchestration.chat_answer import CHAT_GENERATOR_LINE_MECHANICAL

        job, task_id = _job()
        assert _run(["chat", "ask", job.job_id, "Did the tests pass?", "--task", task_id]) == 0
        lines = capsys.readouterr().out.splitlines()
        scope_index = next(i for i, line in enumerate(lines) if line.startswith("Scope:"))
        assert lines[scope_index + 1] == CHAT_GENERATOR_LINE_MECHANICAL

    def test_the_text_forms_evidence_lines_match_the_json_forms_evidence(self, capsys):
        # R-1094: the text form's `[n] kind ref` lines, one per evidence item, must be
        # exactly what the `--json` form's `evidence` list holds — never more, never fewer.
        job, task_id = _job()
        assert _run(["chat", "ask", job.job_id, "Did the tests pass?", "--task", task_id,
                    "--json"]) == 0
        json_out = json.loads(capsys.readouterr().out)
        assert json_out["evidence"]

        assert _run(["chat", "ask", job.job_id, "Did the tests pass?",
                    "--task", task_id]) == 0
        text_out = capsys.readouterr().out
        expected = [f"[{item['number']}] {item['kind']} {item['ref']}"
                    for item in json_out["evidence"]]
        printed = [line for line in text_out.splitlines() if re.match(r"^\[\d+\] ", line)]
        assert printed == expected


# ---------------------------------------------------------------------------
# S6 — a card is printed, and sent only once confirmable and confirmed.
# ---------------------------------------------------------------------------


class TestChatAskCard:
    def test_no_yes_and_no_tty_is_not_sent_and_names_yes(self, capsys):
        job, _task_id = _job()
        assert _run(["chat", "ask", job.job_id, "pause", "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["kind"] == "card"
        assert out["sent"] is False
        assert "--yes" in out["not_sent_reason"]
        assert _audit_lines(job.job_id) == []

    def test_yes_with_no_cockpit_exits_3_and_writes_no_audit(self, capsys):
        job, _task_id = _job()
        assert _run(["chat", "ask", job.job_id, "pause", "--yes"]) == 3
        assert _audit_lines(job.job_id) == []

    def test_yes_with_a_live_cockpit_sends_and_audits(self, capsys):
        job, _task_id = _job()
        _start_live_cockpit(job.job_id, capsys)
        assert _run(["chat", "ask", job.job_id, "pause", "--yes", "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["sent"] is True
        assert out["door"]["command"] == "job.pause"
        lines = _audit_lines(job.job_id)
        assert len(lines) == 1
        assert (lines[0]["command"], lines[0]["outcome"]) == ("job.pause", "accepted")

    def test_a_terminal_prompt_answered_n_is_not_sent(self, capsys, monkeypatch):
        import apps.cli.commands.chat_cmd as chat_cmd_mod

        job, _task_id = _job()
        monkeypatch.setattr(chat_cmd_mod, "_chat_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda *_a, **_k: "n")
        assert _run(["chat", "ask", job.job_id, "pause"]) == 0
        text = capsys.readouterr().out
        assert "Not sent: not confirmed." in text
        assert _audit_lines(job.job_id) == []

    def test_a_terminal_prompt_answered_y_sends(self, capsys, monkeypatch):
        import apps.cli.commands.chat_cmd as chat_cmd_mod

        job, _task_id = _job()
        _start_live_cockpit(job.job_id, capsys)
        monkeypatch.setattr(chat_cmd_mod, "_chat_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda *_a, **_k: "y")
        assert _run(["chat", "ask", job.job_id, "pause"]) == 0
        text = capsys.readouterr().out
        assert "Sent: job.pause." in text
        assert len(_audit_lines(job.job_id)) == 1

    def test_a_live_session_for_another_job_is_not_used(self, capsys):
        job_a, _ = _job()
        job_b, _ = _job()
        _start_live_cockpit(job_a.job_id, capsys)
        assert _run(["chat", "ask", job_b.job_id, "pause", "--yes", "--json"]) == 3
        out = json.loads(capsys.readouterr().out)
        assert out["error"] == "cockpit_not_running"
        assert _audit_lines(job_b.job_id) == []

    def test_a_dead_pid_registration_is_not_used(self, capsys):
        job, _task_id = _job()
        info = {
            "version": 1, "url": "http://127.0.0.1:1/?job=x&token=y", "host": "127.0.0.1",
            "port": 1, "token": "irrelevant", "job_id": job.job_id, "pid": _dead_pid(),
            "started_at": "2020-01-01T00:00:00Z",
        }
        (_sessions_dir() / f"{job.job_id}.json").write_text(json.dumps(info))
        assert _run(["chat", "ask", job.job_id, "pause", "--yes", "--json"]) == 3
        out = json.loads(capsys.readouterr().out)
        assert out["error"] == "cockpit_not_running"

    def test_a_wrong_token_exits_1(self, capsys):
        job, _task_id = _job()
        _port, _token = _start_live_cockpit(job.job_id, capsys)
        session_file = _sessions_dir() / f"{job.job_id}.json"
        info = json.loads(session_file.read_text())
        info["token"] = "not-the-real-token"
        session_file.write_text(json.dumps(info))
        assert _run(["chat", "ask", job.job_id, "pause", "--yes"]) == 1

    def test_an_unrecognized_action_is_not_confirmable(self, capsys):
        job, _task_id = _job()
        assert _run(["chat", "ask", job.job_id, "deploy it", "--yes", "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["sent"] is False
        assert out["confirmable"] is False


# ---------------------------------------------------------------------------
# R-1094: the newest of several live sessions is used, and repeated confirmed
# cards to one running cockpit are each their own audited outcome.
# ---------------------------------------------------------------------------


class TestChatAskLiveSessionAndRepeatSend:
    def test_the_newest_of_two_live_sessions_for_one_job_is_returned(self):
        from apps.cli.commands.ui import live_ui_session_for_job

        job, _task_id = _job()
        pid = os.getpid()
        older = {
            "version": 1, "url": "http://127.0.0.1:1/", "host": "127.0.0.1", "port": 1,
            "token": "older-token", "job_id": job.job_id, "pid": pid,
            "started_at": "2020-01-01T00:00:00Z",
        }
        newer = {
            "version": 1, "url": "http://127.0.0.1:2/", "host": "127.0.0.1", "port": 2,
            "token": "newer-token", "job_id": job.job_id, "pid": pid,
            "started_at": "2020-01-02T00:00:00Z",
        }
        (_sessions_dir() / f"{job.job_id}-a.json").write_text(json.dumps(older))
        (_sessions_dir() / f"{job.job_id}-b.json").write_text(json.dumps(newer))
        session = live_ui_session_for_job(job.job_id)
        assert session["token"] == "newer-token"

    def test_two_cards_confirmed_to_one_cockpit_are_both_audited_accepted(self, capsys):
        job, _task_id = _job()
        _start_live_cockpit(job.job_id, capsys)
        assert _run(["chat", "ask", job.job_id, "pause", "--yes", "--json"]) == 0
        first = json.loads(capsys.readouterr().out)
        assert _run(["chat", "ask", job.job_id, "resume", "--yes", "--json"]) == 0
        second = json.loads(capsys.readouterr().out)
        assert (first["sent"], second["sent"]) == (True, True)
        lines = _audit_lines(job.job_id)
        assert [line["command"] for line in lines] == ["job.pause", "job.unpause"]
        assert all(line["outcome"] == "accepted" for line in lines)


# ---------------------------------------------------------------------------
# The invalid task id, and the bare group form's own contract.
# ---------------------------------------------------------------------------


def test_an_unknown_task_id_exits_2(capsys):
    job, _task_id = _job()
    assert _run(["chat", "ask", job.job_id, "pause", "--task", "0123456789abcdef",
                "--json"]) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["error"] == "invalid_task"


def test_the_bare_group_form_still_records_a_steering_message(capsys):
    job, _task_id = _job()
    assert _run(["chat", job.job_id, "Keep it small."]) == 0
    assert [r["text"] for r in ST.list_steering_messages(job.job_id)] == ["Keep it small."]
