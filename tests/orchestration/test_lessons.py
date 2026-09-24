"""F265 T001 — the post-task lesson, built from the Run's real diff (DECISION F265 D1).

No network and no model: every test injects the transport seam `teacher_model` defines and
pins the transport's resolution, so each property is observable offline.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.core.models import JobBudgets
from packages.orchestration import lessons, pingpong_job, teacher_model
from packages.orchestration.data_paths import run_dir
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from packages.orchestration.teacher_model import TeacherReply, TeacherTransportUnavailable
from packages.orchestration.teacher_spend import TEACHER_ROLE, TeacherUsage, record_teacher_question
from packages.orchestration.token_ledger import CallRecord, record_call

#: A diff whose ADDED lines use `functools.lru_cache`, and whose REMOVED line uses `os.walk`.
DIFF = """diff --git a/pkg/cache.py b/pkg/cache.py
--- a/pkg/cache.py
+++ b/pkg/cache.py
@@ -1,3 +1,5 @@
-files = list(os.walk(root))
+import functools
+
+@functools.lru_cache(maxsize=128)
+def load(name):
+    return open(name).read()
"""

REPLY = json.dumps({
    "summary": "The change caches file loads so a second read costs nothing.",
    "constructs": [
        {"name": "functools.lru_cache", "what": "memoises a function's results",
         "why_here": "load is called with the same names", "judgement": "sound here"},
        {"name": "os.walk", "what": "walks a tree", "why_here": "it was removed",
         "judgement": "not used"},
        {"name": "asyncio.gather", "what": "runs coroutines", "why_here": "invented",
         "judgement": "not in the diff"},
    ],
})


def _rows(ledger: Path) -> list[dict]:
    conn = sqlite3.connect(ledger)
    try:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute("SELECT * FROM calls ORDER BY call_id")]
    finally:
        conn.close()


def _hash_tree(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


class _Call:
    """A fake transport that records every prompt it is sent."""

    def __init__(self, text: str = REPLY, raises: Exception | None = None):
        self.text, self.raises, self.prompts = text, raises, []

    def __call__(self, prompt: str, *, model: str) -> TeacherReply:
        self.prompts.append((prompt, model))
        if self.raises is not None:
            raise self.raises
        return TeacherReply(text=self.text, usage=TeacherUsage(tokens_in=100, tokens_out=40))


@pytest.fixture
def transport(monkeypatch):
    monkeypatch.setattr(teacher_model, "resolve_teacher_transport",
                        lambda config_file=None: ("ollama", "teacher-model"))


def _run(tmp_path: Path, diff: str | None = DIFF, run_id: str = "run-1") -> Path:
    folder = run_dir(run_id, tmp_path)
    folder.mkdir(parents=True)
    if diff is not None:
        (folder / "result.diff").write_text(diff, encoding="utf-8")
    return folder


def _generate(tmp_path: Path, call: _Call, **kwargs):
    args = {"run_id": "run-1", "job_id": "job-1", "task_id": "T001", "task_title": "cache loads",
            "mission_id": "m-1", "call": call, "ledger_path": tmp_path / "ledger.sqlite3",
            "root": tmp_path}
    args.update(kwargs)
    return lessons.generate_lesson(**args)


def test_the_prompt_carries_the_task_title_and_the_whole_diff():
    prompt = lessons.build_lesson_prompt(DIFF, task_title="cache loads")
    assert "TASK: cache loads" in prompt
    assert prompt.endswith(DIFF)


def test_a_reply_is_read_from_the_json_object_it_holds():
    summary, constructs = lessons.parse_lesson_reply("Here you go:\n```json\n" + REPLY + "\n```")
    assert summary.startswith("The change caches")
    assert [c["name"] for c in constructs] == ["functools.lru_cache", "os.walk", "asyncio.gather"]


@pytest.mark.parametrize("text", [
    "no object at all",
    json.dumps({"constructs": []}),
    json.dumps({"summary": "x", "constructs": [{"name": "a", "what": "b", "why_here": "c"}]}),
    json.dumps({"summary": "x", "constructs": {}}),
    "{" + "x" * lessons.LESSON_MAX_REPLY_CHARS + "}",
])
def test_an_unreadable_reply_is_refused(text):
    with pytest.raises(lessons.LessonError):
        lessons.parse_lesson_reply(text)


def test_only_constructs_on_an_added_line_are_taught():
    _, constructs = lessons.parse_lesson_reply(REPLY)
    kept, dropped = lessons.ground_constructs(constructs, DIFF)
    assert [c["name"] for c in kept] == ["functools.lru_cache"]
    assert dropped == ["os.walk", "asyncio.gather"]


def test_a_completed_run_gets_a_sealed_lesson_billed_to_the_teacher(tmp_path, transport):
    _run(tmp_path)
    call = _Call()
    lesson = _generate(tmp_path, call)

    assert lesson["status"] == lessons.STATUS_READY
    assert [c["name"] for c in lesson["constructs"]] == ["functools.lru_cache"]
    assert lesson["ungrounded"] == ["os.walk", "asyncio.gather"]
    assert lesson["diff_sha256"] == hashlib.sha256(DIFF.encode()).hexdigest()
    assert (lesson["run_id"], lesson["mission_id"], lesson["model"]) == ("run-1", "m-1",
                                                                         "teacher-model")
    assert call.prompts == [(lessons.build_lesson_prompt(DIFF, task_title="cache loads"),
                             "teacher-model")]
    assert lessons.verify_lesson_record(lessons.lesson_path("run-1", tmp_path)) == []
    assert lessons.load_lesson("run-1", tmp_path) == lesson
    rows = _rows(tmp_path / "ledger.sqlite3")
    assert [(r["call_id"], r["role"], r["job_id"], r["tokens_in"]) for r in rows] == [
        ("teacher:lesson:run-1", TEACHER_ROLE, "job-1", 100)]
    assert lesson["call_id"] == "teacher:lesson:run-1" and lesson["billed"] is True


def test_a_stored_lesson_is_read_back_without_a_second_call(tmp_path, transport):
    _run(tmp_path)
    first = _generate(tmp_path, _Call())
    again = _Call(raises=AssertionError("a stored lesson must not call the model"))
    assert _generate(tmp_path, again) == first
    assert again.prompts == []
    assert len(_rows(tmp_path / "ledger.sqlite3")) == 1


def test_reading_a_lesson_writes_nothing(tmp_path, transport):
    _run(tmp_path)
    _generate(tmp_path, _Call())
    before = _hash_tree(tmp_path)
    lessons.load_lesson("run-1", tmp_path)
    _generate(tmp_path, _Call())
    assert _hash_tree(tmp_path) == before


def test_a_spent_pot_is_an_honest_empty_lesson_and_no_call(tmp_path, transport):
    _run(tmp_path)
    ledger = tmp_path / "ledger.sqlite3"
    record_teacher_question(model="teacher-model", job_id="job-1", path=ledger)
    call = _Call()
    lesson = _generate(tmp_path, call, budgets=JobBudgets(max_provider_calls=1))
    assert lesson["status"] == lessons.STATUS_BUDGET_EXHAUSTED
    assert "max_provider_calls" in lesson["reason"]
    assert (lesson["summary"], lesson["constructs"], call.prompts) == ("", [], [])
    assert len(_rows(ledger)) == 1


def test_the_pot_counts_only_this_jobs_teacher_calls(tmp_path, transport):
    _run(tmp_path)
    ledger = tmp_path / "ledger.sqlite3"
    record_teacher_question(model="teacher-model", job_id="job-2", path=ledger)
    record_call(CallRecord(call_id="job-1:T001", job_id="job-1", task_id="T001", role="builder",
                           model="m", ts_utc="2026-09-24T00:00:00+00:00", tokens_in=10**6,
                           tokens_out=10**6), path=ledger)
    lesson = _generate(tmp_path, _Call(),
                       budgets=JobBudgets(max_provider_calls=1, max_total_tokens=1000))
    assert lesson["status"] == lessons.STATUS_READY


def test_the_pot_counts_the_tokens_the_teacher_reported(tmp_path, transport):
    _run(tmp_path)
    ledger = tmp_path / "ledger.sqlite3"
    record_teacher_question(model="teacher-model", job_id="job-1", path=ledger,
                            usage=TeacherUsage(tokens_in=600, tokens_out=500))
    lesson = _generate(tmp_path, _Call(), budgets=JobBudgets(max_total_tokens=1000))
    assert lesson["status"] == lessons.STATUS_BUDGET_EXHAUSTED
    assert "max_total_tokens" in lesson["reason"]


@pytest.mark.parametrize(("diff", "status"), [
    (None, lessons.STATUS_NO_DIFF),
    ("  \n", lessons.STATUS_NO_DIFF),
    ("+" + "x" * lessons.LESSON_MAX_DIFF_CHARS, lessons.STATUS_DIFF_TOO_LARGE),
])
def test_a_run_without_a_teachable_diff_gets_no_call(tmp_path, transport, diff, status):
    _run(tmp_path, diff)
    call = _Call()
    lesson = _generate(tmp_path, call)
    assert (lesson["status"], lesson["summary"], call.prompts) == (status, "", [])
    assert not (tmp_path / "ledger.sqlite3").exists()


def test_a_job_with_no_ledger_gets_no_call(tmp_path, transport):
    _run(tmp_path)
    call = _Call()
    lesson = _generate(tmp_path, call, ledger_path=None)
    assert (lesson["status"], call.prompts) == (lessons.STATUS_NO_LEDGER, [])


def test_an_unreadable_ledger_gets_no_call(tmp_path, transport):
    _run(tmp_path)
    (tmp_path / "ledger.sqlite3").write_bytes(b"this is not a database" * 64)
    call = _Call()
    lesson = _generate(tmp_path, call)
    assert (lesson["status"], call.prompts) == (lessons.STATUS_NO_LEDGER, [])
    assert "could not be read" in lesson["reason"]


def test_an_unusable_transport_is_named_and_never_billed(tmp_path, monkeypatch):
    _run(tmp_path)
    monkeypatch.setattr(teacher_model, "resolve_teacher_transport", lambda config_file=None: None)
    lesson = _generate(tmp_path, _Call())
    assert lesson["status"] == lessons.STATUS_TEACHER_UNAVAILABLE
    assert "ollama" in lesson["reason"]
    assert not (tmp_path / "ledger.sqlite3").exists()


def test_a_failed_call_is_named_and_never_billed(tmp_path, transport):
    _run(tmp_path)
    lesson = _generate(tmp_path, _Call(raises=TeacherTransportUnavailable("connection refused")))
    assert lesson["status"] == lessons.STATUS_TEACHER_UNAVAILABLE
    assert "connection refused" in lesson["reason"]
    assert not (tmp_path / "ledger.sqlite3").exists()


def test_an_unreadable_reply_is_billed_and_teaches_nothing(tmp_path, transport):
    _run(tmp_path)
    lesson = _generate(tmp_path, _Call(text="I would rather not."))
    assert (lesson["status"], lesson["summary"], lesson["billed"]) == (
        lessons.STATUS_UNREADABLE_REPLY, "", True)
    assert len(_rows(tmp_path / "ledger.sqlite3")) == 1


def test_a_tampered_lesson_is_loud(tmp_path, transport):
    _run(tmp_path)
    _generate(tmp_path, _Call())
    path = lessons.lesson_path("run-1", tmp_path)
    body = json.loads(path.read_text(encoding="utf-8"))
    body["summary"] = "something the teacher never said"
    path.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(lessons.LessonError, match="record_sha256"):
        lessons.load_lesson("run-1", tmp_path)


def test_the_configured_teacher_model_reaches_the_transport(tmp_path, monkeypatch):
    _run(tmp_path)
    monkeypatch.setenv("REMEDY_TEACHER_MODEL", "lesson-model")
    from packages.orchestration.config import reset_config

    reset_config()
    call = _Call()
    lesson = _generate(tmp_path, call, config_file=lessons.lesson_role_overrides())
    assert lesson["model"] == "lesson-model"
    assert call.prompts[0][1] == "lesson-model"


def _job_and_task():
    return (SimpleNamespace(job_id="job-1", repo_path=""),
            SimpleNamespace(run_id="run-1", task_id="T001", title="cache loads"))


def test_a_completed_task_gets_no_lesson_while_lessons_are_off(monkeypatch):
    called = []
    monkeypatch.setattr(lessons, "generate_lesson", lambda **kw: called.append(kw))
    pingpong_job._teach_task_lesson(*_job_and_task())
    assert called == []


def test_a_completed_task_gets_its_lesson_when_lessons_are_on(monkeypatch):
    monkeypatch.setenv("REMEDY_TEACHER_LESSONS", "1")
    monkeypatch.setenv("REMEDY_TEACHER_LESSON_MAX_CALLS", "5")
    from packages.orchestration.config import reset_config

    reset_config()
    called = []
    monkeypatch.setattr(lessons, "generate_lesson",
                        lambda **kw: called.append(kw) or {"status": lessons.STATUS_READY})
    pingpong_job._teach_task_lesson(*_job_and_task())
    assert [(kw["run_id"], kw["task_id"], kw["task_title"], kw["mission_id"]) for kw in called] == [
        ("run-1", "T001", "cache loads", "")]
    assert called[0]["budgets"] == JobBudgets(max_provider_calls=5, max_total_tokens=300000)


def test_a_failing_lesson_never_fails_the_task(monkeypatch):
    monkeypatch.setattr(lessons, "lessons_enabled", lambda: True)

    def boom(**_kw):
        raise RuntimeError("teacher exploded")

    monkeypatch.setattr(lessons, "generate_lesson", boom)
    pingpong_job._teach_task_lesson(*_job_and_task())


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, check=True)


class _Provider:
    """A fake builder that writes one file into the job's worktree, and a passing reviewer."""

    def __init__(self, holder: dict):
        self.holder = holder

    def build(self, prompt, **kw):
        (Path(self.holder["path"]) / "greet.txt").write_text("Say hello with greet_all().\n")
        return BuilderOutput(summary="wrote greet.txt", files_changed=["greet.txt"],
                             provider="fake")

    def review(self, prompt, **kw):
        return ReviewerOutput(verdict="pass", confidence="high", summary="ok", provider="fake")


def test_a_real_job_teaches_its_completed_task_from_the_runs_own_diff(tmp_path, monkeypatch):
    from packages.orchestration import job_evidence
    from packages.orchestration import worktrees as W
    from packages.orchestration.config import reset_config
    from packages.orchestration.pingpong_job import JOB_COMPLETED, parse_job_file, run_job
    from packages.orchestration.token_ledger import query_cost

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("REMEDY_TEACHER_LESSONS", "1")
    reset_config()
    monkeypatch.setattr(job_evidence, "_resolve_job_ledger_project_id", lambda job: "proj-1")
    monkeypatch.setattr(teacher_model, "resolve_teacher_transport",
                        lambda config_file=None: ("ollama", "teacher-model"))
    call = _Call(text=json.dumps({"summary": "Adds a greeting.", "constructs": [
        {"name": "greet_all()", "what": "greets", "why_here": "asked", "judgement": "fine"}]}))
    monkeypatch.setattr(teacher_model, "ollama_teacher_call", call)
    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (("init", "-q"), ("config", "user.email", "t@e.com"), ("config", "user.name", "T"),
                 ("config", "commit.gpgsign", "false")):
        _git(repo, *args)
    (repo / "base.txt").write_text("base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")
    holder: dict = {}
    real_create = W.create

    def spy(job_id, r):
        handle = real_create(job_id, r)
        holder["path"] = handle.path
        return handle

    monkeypatch.setattr(W, "create", spy)
    job = parse_job_file("# One\n\n## Task 1 — greet\n\nWrite greet.txt.\n", str(repo))
    provider = _Provider(holder)
    done = run_job(job.job_id, builder_provider=provider, reviewer_provider=provider,
                   builder_name="fake", reviewer_name="fake", max_rounds=1)

    assert done.state == JOB_COMPLETED, (done.error, [t.error for t in done.tasks])
    run_id = done.tasks[0].run_id
    lesson = lessons.load_lesson(run_id)
    diff = (run_dir(run_id) / "result.diff").read_text(encoding="utf-8")
    assert lesson["status"] == lessons.STATUS_READY
    assert lesson["diff_sha256"] == hashlib.sha256(diff.encode("utf-8")).hexdigest()
    assert [c["name"] for c in lesson["constructs"]] == ["greet_all()"]
    assert call.prompts[0][0].endswith(diff)
    report = query_cost(project_id="proj-1", job_id=str(job.job_id), by="role")
    assert [(row.bucket, row.calls) for row in report.rows] == [(TEACHER_ROLE, 1)]


def test_the_lesson_keys_default_to_off_and_to_a_bounded_pot():
    from packages.orchestration.config import get_config

    config = get_config()
    assert config.get("teacher.lessons") is False
    assert lessons.lesson_budgets() == JobBudgets(max_provider_calls=30, max_total_tokens=300000)


def _lessons_on(monkeypatch, tmp_path):
    from packages.orchestration.config import reset_config

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("REMEDY_TEACHER_LESSONS", "1")
    reset_config()


def test_a_stored_lesson_is_announced_once_on_the_jobs_run_log(tmp_path, monkeypatch, transport):
    from packages.orchestration import job_evidence
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events

    _lessons_on(monkeypatch, tmp_path)
    monkeypatch.setattr(job_evidence, "_resolve_job_ledger_project_id", lambda job: "proj-1")
    monkeypatch.setattr(teacher_model, "ollama_teacher_call", _Call())
    _run(resolve_data_root())
    job = SimpleNamespace(job_id="0a1b2c3d4e5f6a7b", repo_path="")
    task = SimpleNamespace(run_id="run-1", task_id="T001", title="cache loads")
    pingpong_job._teach_task_lesson(job, task)
    pingpong_job._teach_task_lesson(job, task)
    written = [e for e in load_run_events(resolve_data_root(), job.job_id)
               if e.get("event") == "task_lesson_written"]
    assert [(e.get("task_id"), e["metadata"]) for e in written] == [
        ("T001", {"run_id": "run-1", "lesson_status": lessons.STATUS_READY})]


def test_a_mission_jobs_lesson_names_its_mission(tmp_path, monkeypatch):
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.mission_state import (
        MISSION_ROLE_INITIAL,
        create_mission,
        link_job_to_mission,
    )

    _lessons_on(monkeypatch, tmp_path)
    mission = create_mission("p-f265", "Teach the change", root=resolve_data_root())
    link_job_to_mission("p-f265", mission.id, "0a1b2c3d4e5f6a7b", MISSION_ROLE_INITIAL,
                        root=resolve_data_root())
    called = []
    monkeypatch.setattr(lessons, "generate_lesson",
                        lambda **kw: called.append(kw) or {"status": lessons.STATUS_READY})
    job = SimpleNamespace(job_id="0a1b2c3d4e5f6a7b", repo_path="")
    pingpong_job._teach_task_lesson(job, SimpleNamespace(run_id="run-1", task_id="T001",
                                                         title="cache loads"))
    assert [kw["mission_id"] for kw in called] == [mission.id]
