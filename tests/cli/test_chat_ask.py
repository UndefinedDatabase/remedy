"""F038 T003 — `remedy chat ask <job_id> "<text>" [--task <task id>] [--yes] [--json]` runs one
chat turn: a question prints its scope, its checked answer and its numbered evidence; a card
prints its title and lines and is sent through the serve supervisor's write door only when
confirmable and confirmed (DECISION F038 D10, DECISION amend1015f D20).

Temporary data roots only. No provider call is ever made: `chat.model_written` stays off, so
every question here is answered mechanically.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from apps.cli.grouped import main as grouped_main
from packages.core.models import RunState
from packages.orchestration import steering as ST
from packages.orchestration.command_audit import AUDIT_FILENAME
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.serve_paths import serve_paths
from tests.serve_http_handler.door_host import SupervisorThread


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path_factory, monkeypatch):
    """A short data root, so a supervisor's socket path stays below its length limit."""
    root = tmp_path_factory.mktemp("ca")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def supervisor(isolate_data_root):
    """A real `remedy serve start` supervisor for the test's data root (amend1015f D20)."""
    running = SupervisorThread(isolate_data_root)
    yield running
    running.close()


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

    def test_yes_with_no_supervisor_exits_3_and_writes_no_audit(self, capsys):
        job, _task_id = _job()
        assert _run(["chat", "ask", job.job_id, "pause", "--yes", "--json"]) == 3
        out = json.loads(capsys.readouterr().out)
        assert out["error"] == "serve_not_running"
        assert "remedy serve start" in out["message"]
        assert _audit_lines(job.job_id) == []

    def test_yes_with_a_running_supervisor_sends_and_audits(self, capsys, supervisor):
        job, _task_id = _job()
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

    def test_a_terminal_prompt_answered_y_sends(self, capsys, monkeypatch, supervisor):
        import apps.cli.commands.chat_cmd as chat_cmd_mod

        job, _task_id = _job()
        monkeypatch.setattr(chat_cmd_mod, "_chat_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda *_a, **_k: "y")
        assert _run(["chat", "ask", job.job_id, "pause"]) == 0
        text = capsys.readouterr().out
        assert "Sent: job.pause." in text
        assert len(_audit_lines(job.job_id)) == 1

    def test_a_wrong_token_exits_1(self, capsys, supervisor, isolate_data_root):
        job, _task_id = _job()
        serve_paths(isolate_data_root).token_file.write_text("not-the-real-token",
                                                             encoding="utf-8")
        assert _run(["chat", "ask", job.job_id, "pause", "--yes", "--json"]) == 1
        out = json.loads(capsys.readouterr().out)
        assert out["error"] == "door_refused"
        assert _audit_lines(job.job_id) == []

    def test_an_unrecognized_action_is_not_confirmable(self, capsys):
        job, _task_id = _job()
        assert _run(["chat", "ask", job.job_id, "deploy it", "--yes", "--json"]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["sent"] is False
        assert out["confirmable"] is False


# ---------------------------------------------------------------------------
# R-1094: repeated confirmed cards to one running supervisor are each their own
# audited outcome.
# ---------------------------------------------------------------------------


class TestChatAskRepeatSend:
    def test_two_cards_confirmed_to_one_supervisor_are_both_audited_accepted(
            self, capsys, supervisor):
        job, _task_id = _job()
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
