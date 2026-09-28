"""F038 T003, DECISION F038 D11 — the cockpit's chat route: `GET
/api/jobs/<job_id>/chat?text=<line>&task=<task id>` runs one chat turn and answers it in the
same wire shape `chat_turn_view` gives, which `remedy chat ask --json` emits too. The route is
read with `do_GET` on a handler built without a socket, the way
`tests/ui_server/test_lessons_route.py` reads every endpoint, over a saved RUNNING job of one
task in a temporary data root. The route sends nothing: every assertion below either reads its
body or hashes the data root before and after.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import quote

import pytest

from apps.cli.grouped import main as grouped_main
from packages.core.models import RunState
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.ui_server import _RemedyHandler


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _job() -> tuple[JobPlan, str]:
    """A saved RUNNING job of one done, passing task (the block's own fixture shape)."""
    task = TaskEntry(title="Write the README", status="done", test_passed=True)
    job = JobPlan(
        job_title="f038-chat-route-job", tasks=[task], state=RunState.RUNNING,
        metadata={"target_repo": "/tmp/repo"},
    )
    save_job_plan(job)
    return job, task.task_id


def _get(job_id: str, *, text: str | None = None, task: str | None = None) -> tuple[int, dict]:
    handler = _RemedyHandler.__new__(_RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = job_id
    handler.app_html = ""
    captured: dict = {}
    handler._send_json = lambda code, data: captured.update(code=code, data=data)  # type: ignore[method-assign]
    query = "token=tok"
    if text is not None:
        query += f"&text={quote(text)}"
    if task is not None:
        query += f"&task={quote(task)}"
    handler.path = f"/api/jobs/{job_id}/chat?{query}"
    handler.do_GET()
    return captured["code"], captured["data"]


def _run_cli(argv: list[str]) -> int:
    try:
        grouped_main(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


def _hash_tree(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def test_a_focused_question_answers_200_with_numbered_evidence():
    job, task_id = _job()
    code, data = _get(job.job_id, text="Did the tests pass?", task=task_id)
    assert code == 200
    assert data["available"] is True
    assert data["kind"] == "answer"
    assert data["scope"] == "node"
    assert data["subject"] == task_id
    assert [item["number"] for item in data["evidence"]] == list(
        range(1, len(data["evidence"]) + 1))


def test_the_routes_body_matches_remedy_chat_asks_json_for_a_question_and_for_pause(capsys):
    job, task_id = _job()

    code, route_answer = _get(job.job_id, text="Did the tests pass?", task=task_id)
    assert code == 200
    assert _run_cli(["chat", "ask", job.job_id, "Did the tests pass?", "--task", task_id,
                     "--json"]) == 0
    cli_answer = json.loads(capsys.readouterr().out)
    for key in set(route_answer) - {"available"}:
        assert cli_answer[key] == route_answer[key], key

    code, route_card = _get(job.job_id, text="pause")
    assert code == 200
    assert _run_cli(["chat", "ask", job.job_id, "pause", "--json"]) == 0
    cli_card = json.loads(capsys.readouterr().out)
    for key in set(route_card) - {"available"}:
        assert cli_card[key] == route_card[key], key


def test_an_unfocused_question_answers_project_scope_with_no_evidence():
    job, _task_id = _job()
    code, data = _get(job.job_id, text="What is the roadmap position?")
    assert code == 200
    assert data["available"] is True
    assert data["scope"] == "project"
    assert data["evidence"] == []
    assert [sentence["text"] for sentence in data["sentences"]] == ["Not in evidence."]


def test_pause_answers_a_confirmable_card_and_writes_nothing():
    job, _task_id = _job()
    root = Path(resolve_data_root())
    before = _hash_tree(root)
    code, data = _get(job.job_id, text="pause")
    assert code == 200
    assert data["available"] is True
    assert data["kind"] == "card"
    assert data["verb"] == "job.pause"
    assert data["confirmable"] is True
    assert _hash_tree(root) == before


def test_a_focused_note_answers_job_steer_with_exact_args():
    job, task_id = _job()
    code, data = _get(job.job_id, text="note: use tabs", task=task_id)
    assert code == 200
    assert data["verb"] == "job.steer"
    assert data["args"] == {"task_id": task_id, "message": "use tabs"}
    assert data["missing"] == []


def test_no_text_and_a_blank_text_each_answer_empty_text():
    job, _task_id = _job()
    code, data = _get(job.job_id)
    assert code == 200
    assert data == {"available": False, "reason": "empty_text"}
    code, data = _get(job.job_id, text="   ")
    assert code == 200
    assert data == {"available": False, "reason": "empty_text"}


def test_an_unknown_task_answers_unknown_task():
    job, _task_id = _job()
    code, data = _get(job.job_id, text="pause", task="0123456789abcdef")
    assert code == 200
    assert data == {"available": False, "reason": "unknown_task"}


def test_a_padded_task_is_answered_in_the_node_scope():
    job, task_id = _job()
    code, data = _get(job.job_id, text="Did the tests pass?", task=f"  {task_id}  ")
    assert code == 200
    assert data["available"] is True
    assert data["scope"] == "node"
    assert data["subject"] == task_id


def test_two_questions_leave_the_data_root_hashing_identically():
    job, task_id = _job()
    root = Path(resolve_data_root())
    before = _hash_tree(root)
    _get(job.job_id, text="Did the tests pass?", task=task_id)
    _get(job.job_id, text="What is the roadmap position?")
    assert _hash_tree(root) == before
