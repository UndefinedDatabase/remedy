"""F332: a job task an earlier task of its job already did ends done with a plain record, never blocked.

The shape is job 6c4564622e87457e's (operator order beweis): task 2 changed NetHeader.tsx and its call
site KnowledgeNet.tsx, so task 3 (deliverable KnowledgeNet.tsx) staged nothing, and task 4 only runs the
tests. Fakes only; no model call, no real job.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration import job_task_already_done as A
from packages.orchestration.client_story import _task_rows
from packages.orchestration.client_story_words import story_problems
from packages.orchestration.empty_diff_gate import reject_verdict_on_empty_diff
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    TASK_APPLIED,
    TASK_BLOCKED,
    ApplyManifest,
    TaskEntry,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import ReviewerOutput, ReviewFinding
from packages.orchestration.pingpong_provider_fake import FakeProvider

_KNOWLEDGE_NET = "src/screens/KnowledgeNet.tsx"
_NET_HEADER = "src/screens/net/NetHeader.tsx"


def _task(task_id: str, title: str, *, status: str = "pending", applied: list[str] | None = None,
          deliverable: str = "", hints: list[str] | None = None, acceptance: str = "") -> TaskEntry:
    task = TaskEntry(task_id=task_id, title=title, status=status, acceptance=acceptance)
    task.inputs = {"deliverable": deliverable, "plan": {"files_hint": list(hints or [])}}
    if applied is not None:
        task.apply_manifest = ApplyManifest(task_id=task_id, applied_files=list(applied), status="applied")
    return task


class _Job:
    def __init__(self, tasks: list[TaskEntry]) -> None:
        self.tasks = tasks


def _the_job() -> _Job:
    """Job 6c4564622e87457e's four tasks at the moment task 3 staged no change."""
    return _Job([
        _task("150976f7", "Replace ad-hoc info button in Memory.tsx with InfoButton", status=TASK_APPLIED,
              applied=["src/screens/Memory.tsx"], deliverable="src/screens/Memory.tsx"),
        _task("15be7564", "Refactor NetHeader to accept ComponentChildren instead of onInfo callback",
              status=TASK_APPLIED, applied=[_NET_HEADER, _KNOWLEDGE_NET, "src/styles/knowledge-net.css"],
              deliverable=_NET_HEADER),
        _task("001c113a", "Update KnowledgeNet to pass rendered InfoButton to NetHeader", deliverable=_KNOWLEDGE_NET,
              hints=[_KNOWLEDGE_NET], acceptance="KnowledgeNet passes a rendered <InfoButton> as children"),
        _task("e94a6632", "Run the test command and confirm it exits green",
              deliverable="Test command exits with code 0", acceptance="Test command exits with code 0"),
    ])


def test_the_task_whose_file_an_earlier_task_changed_is_already_done_by_that_task() -> None:
    job = _the_job()
    work = A.earlier_work(job, job.tasks[2])
    assert work is not None and not work.test_run
    assert (work.task_number, work.task_id, work.file_names()) == (2, "15be7564", [_KNOWLEDGE_NET])
    assert work.evidence() == f"already done by task 2 (15be7564): {_KNOWLEDGE_NET} (task 2)"


def test_a_task_naming_a_file_no_earlier_task_touched_is_not_already_done() -> None:
    job = _the_job()
    job.tasks[2] = _task("001c113a", "Update src/screens/Other.tsx", deliverable="src/screens/Other.tsx")
    assert A.earlier_work(job, job.tasks[2]) is None
    assert A.earlier_work(job, job.tasks[0]) is None          # the first task has no earlier task


def test_a_task_that_only_runs_the_tests_checks_every_file_the_earlier_tasks_changed() -> None:
    job = _the_job()
    job.tasks[2].status = TASK_APPLIED                         # task 3 ended done, applying nothing
    work = A.earlier_work(job, job.tasks[3])
    assert work is not None and work.test_run and work.task_number == 2
    assert set(work.file_names()) == {"src/screens/Memory.tsx", _NET_HEADER, _KNOWLEDGE_NET,
                                      "src/styles/knowledge-net.css"}
    assert work.evidence().startswith("checked the work of task 2 (15be7564): ")
    assert not A.is_test_run_task(_task("x", "Run the migration that renames the column"))


def test_the_gate_lifts_no_file_changed_only_as_its_one_reason_and_records_the_evidence() -> None:
    job = _the_job()
    task = job.tasks[2]

    class _Result:
        staged_files: list[str] = []

    assert A.settle_already_done(job, task, _Result(), (False, ["no_file_changed", "reviewer_verdict=needs_repair"])) \
        == (False, ["no_file_changed", "reviewer_verdict=needs_repair"])
    assert A.ALREADY_DONE_KEY not in task.inputs
    assert A.settle_already_done(job, task, _Result(), (False, ["no_file_changed"])) == (True, [])
    assert task.inputs[A.ALREADY_DONE_KEY] == {
        "task": 2, "task_id": "15be7564", "files": [_KNOWLEDGE_NET],
        "evidence": f"already done by task 2 (15be7564): {_KNOWLEDGE_NET} (task 2)"}


def test_the_empty_diff_keeps_a_pass_only_for_a_task_already_done() -> None:
    def review(*findings: ReviewFinding) -> ReviewerOutput:
        return ReviewerOutput(verdict="pass", findings=list(findings), summary="holds")

    low = ReviewFinding(id="L1", severity="low", summary="a note")
    medium = ReviewFinding(id="M1", severity="medium", summary="half done")
    assert reject_verdict_on_empty_diff(review(), staged_files=[], is_fake=False, already_done=True).verdict == "pass"
    assert reject_verdict_on_empty_diff(review(low), staged_files=[], is_fake=False,
                                        already_done=True).verdict == "pass"
    assert reject_verdict_on_empty_diff(review(medium), staged_files=[], is_fake=False,
                                        already_done=True).verdict == "needs_repair"
    held = reject_verdict_on_empty_diff(review(), staged_files=[], is_fake=False)
    assert held.verdict == "needs_repair" and held.findings[0].id == "EMPTY-change"


def test_the_reviewer_is_asked_whether_the_acceptance_already_holds(monkeypatch: pytest.MonkeyPatch) -> None:
    job = _the_job()
    monkeypatch.setattr("packages.orchestration.pingpong_job.load_job_plan", lambda job_id: job)
    asked = A.no_change_diff_summary("6c4564622e87457e", "001c113a")
    assert asked.startswith(A.NO_CHANGE_LINE + "\n")
    assert f"The job's earlier tasks changed these files: {_KNOWLEDGE_NET} (task 2)." in asked
    assert "Judge whether this task's acceptance already holds in the workspace" in asked
    assert A.no_change_diff_summary("6c4564622e87457e", "150976f7") == A.NO_CHANGE_LINE
    assert A.no_change_diff_summary("", "") == A.NO_CHANGE_LINE


def test_the_story_names_the_task_already_done_with_its_closed_word() -> None:
    job = _the_job()
    A.settle_already_done(job, job.tasks[2], type("R", (), {"staged_files": []})(), (False, ["no_file_changed"]))
    rows = _task_rows(job, {})
    assert rows[2]["phrase"] == {"key": "already_done", "args": {"task": 2, "n": 1}}
    assert rows[0]["phrase"] is None
    steps = [{"id": i, "status": "waiting", "phrase": None, "tasks": rows if i == "building" else []}
             for i in ("reading", "planning", "building", "checking", "finished")]
    story = {"state": "working", "next": {"action": "none"}, "steps": steps}
    assert story_problems(story) == []
    rows[2]["phrase"] = {"key": "already_done", "args": {"task": 2}}
    assert story_problems(story) == ["task phrase already_done carries args ['task']"]


_ALREADY_DONE_JOB = """\
# Job: One file, two tasks

## Task 1
Rewrite the heading of docs/README.md.

Files:
- docs/README.md

Acceptance:
- the heading is rewritten

## Task 2
Make docs/README.md name the project.

Files:
- {second}

Acceptance:
- the heading names the project
"""


class _FirstCallOnlyBuilder(FakeProvider):
    """Changes docs/README.md on its first call and nothing after: task 1 did task 2's work."""

    def build(self, prompt, **kwargs):
        out = super().build(prompt, **kwargs)
        if self._build_count > 1:
            out.files_changed = []
        return out


@pytest.fixture
def _repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "src").mkdir()
    (repo / "docs" / "README.md").write_text("# Docs\n")
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    return repo


def _run(repo: Path, second: str):
    job = parse_job_file(_ALREADY_DONE_JOB.format(second=second), str(repo))
    return run_job(job.job_id, builder_provider=_FirstCallOnlyBuilder(pass_on_round=1, fail_on_round=99),
                   reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99), repair_rounds=0)


def test_a_job_whose_second_task_was_done_by_the_first_ends_without_a_block(_repo: Path) -> None:
    result = _run(_repo, "docs/README.md")
    first, second = result.tasks
    assert first.status == TASK_APPLIED and second.status == TASK_APPLIED
    assert result.state != JOB_BLOCKED and not result.error
    assert second.inputs[A.ALREADY_DONE_KEY]["evidence"] == \
        f"already done by task 1 ({first.task_id}): docs/README.md (task 1)"


def test_a_no_change_task_naming_a_file_no_earlier_task_touched_still_blocks(_repo: Path) -> None:
    result = _run(_repo, "src/main.py")
    second = result.tasks[1]
    assert second.status == TASK_BLOCKED
    assert second.error == "completion_gate_failed: no_file_changed"
    assert result.state == JOB_BLOCKED and A.ALREADY_DONE_KEY not in second.inputs
