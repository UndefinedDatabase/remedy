"""F265: the job's lessons route and the stream's lesson announcement (DECISION F265 D2).

The route is read with `do_GET` on a handler built without a socket, the way
`tests/ui_server/test_handler_table_walk.py` reads every endpoint, over a job saved to a
temporary data root. No model is called: the one stored lesson is written through the
generator with an injected transport.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from packages.orchestration import lessons, teacher_model
from packages.orchestration.data_paths import resolve_data_root, run_dir
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.teacher_model import TeacherReply
from packages.orchestration.teacher_spend import TeacherUsage
from packages.orchestration.ui_server import _RemedyHandler, _safe_event_summary

DIFF = "--- a/x.py\n+++ b/x.py\n@@ -0,0 +1 @@\n+print(sorted(names))\n"
REPLY = json.dumps({"summary": "Prints the names in order.", "constructs": [
    {"name": "sorted", "what": "orders", "why_here": "stable output", "judgement": "fine"}]})


@pytest.fixture
def job(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(teacher_model, "resolve_teacher_transport",
                        lambda config_file=None: ("ollama", "teacher-model"))
    plan = JobPlan(job_title="lessons route", tasks=[
        TaskEntry(task_id="T001", title="print the names", run_id="run-a"),
        TaskEntry(task_id="T002", title="ran without a lesson", run_id="run-b"),
        TaskEntry(task_id="T003", title="not run yet"),
    ])
    save_job_plan(plan)
    folder = run_dir("run-a")
    folder.mkdir(parents=True)
    (folder / "result.diff").write_text(DIFF, encoding="utf-8")
    lessons.generate_lesson(
        run_id="run-a", job_id=str(plan.job_id), task_id="T001", task_title="print the names",
        call=lambda prompt, *, model: TeacherReply(text=REPLY, usage=TeacherUsage()),
        ledger_path=tmp_path / "ledger.sqlite3")
    run_dir("run-b").mkdir(parents=True)
    return str(plan.job_id)


def _get(job_id: str) -> tuple[int, dict]:
    handler = _RemedyHandler.__new__(_RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = job_id
    handler.app_html = ""
    captured: dict = {}
    handler._send_json = lambda code, data: captured.update(code=code, data=data)  # type: ignore[method-assign]
    handler.path = f"/api/jobs/{job_id}/lessons?token=tok"
    handler.do_GET()
    return captured["code"], captured["data"]


def _hash_tree(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def test_every_task_is_listed_with_its_lesson_or_the_reason_it_has_none(job):
    code, data = _get(job)
    assert code == 200
    assert (data["job_id"], data["lessons_enabled"]) == (job, False)
    rows = data["lessons"]
    assert [(r["task_id"], r["run_id"], r["status"]) for r in rows] == [
        ("T001", "run-a", lessons.STATUS_READY), ("T002", "run-b", lessons.STATUS_NONE),
        ("T003", "", lessons.STATUS_NONE)]
    assert rows[0]["summary"] == "Prints the names in order."
    assert [c["name"] for c in rows[0]["constructs"]] == ["sorted"]
    assert rows[0]["lesson_id"] == "lesson-run-a"
    assert "switched off" in rows[1]["reason"]
    assert rows[2]["reason"] == "this task has not run yet"


def test_with_lessons_on_a_run_without_one_says_none_was_stored(job, monkeypatch):
    from packages.orchestration.config import reset_config

    monkeypatch.setenv("REMEDY_TEACHER_LESSONS", "1")
    reset_config()
    _, data = _get(job)
    assert data["lessons_enabled"] is True
    assert data["lessons"][1]["reason"] == "no lesson was stored for this run"


def test_a_tampered_lesson_is_named_and_its_text_withheld(job):
    path = lessons.lesson_path("run-a")
    body = json.loads(path.read_text(encoding="utf-8"))
    body["summary"] = "words the teacher never wrote"
    path.write_text(json.dumps(body), encoding="utf-8")
    code, data = _get(job)
    assert code == 200
    row = data["lessons"][0]
    assert row["status"] == lessons.STATUS_NOT_INTACT
    assert "summary" not in row and "constructs" not in row


def test_reading_the_route_writes_nothing(job):
    root = resolve_data_root()
    before = _hash_tree(root)
    _get(job)
    _get(job)
    assert _hash_tree(root) == before


def test_the_stream_names_the_run_and_status_of_a_stored_lesson_and_nothing_else():
    summary = _safe_event_summary(7, {"event": "task_lesson_written", "task_id": "T001",
                                      "metadata": {"run_id": "run-a", "lesson_status": "ready",
                                                   "summary": "not for the stream"}})
    assert set(summary) == {"seq", "event", "timestamp", "outcome", "task_id", "lesson"}
    assert summary["lesson"] == {"run_id": "run-a", "status": "ready"}
    odd = _safe_event_summary(8, {"event": "task_lesson_written",
                                  "metadata": {"run_id": "run-a", "lesson_status": "made-up"}})
    assert odd["lesson"] == {"run_id": "run-a", "status": ""}
    other = _safe_event_summary(9, {"event": "task_run_completed", "task_id": "T001",
                                    "metadata": {"run_id": "run-a", "lesson_status": "ready"}})
    assert "lesson" not in other
