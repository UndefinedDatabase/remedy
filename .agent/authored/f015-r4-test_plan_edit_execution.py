"""F015 T003 — an edited plan is the plan that runs: the approval's hash, its check at start, the goldens.

The end-to-end test edits a pending plan three times — a split, a new sequence and an added
criterion — approves it through `consume_plan_approval`, the approval door's own path, and
runs it with the fake provider, then reads which tasks ran and in which order. The goldens
are the three `plan_v<n>.md` revisions those edits render, generated once and then frozen:
there is no regenerate switch, and a change to the rendering is a change to these files in
the same commit (DECISION F015 D4).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_evidence_export_dir
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    approved_plan_mismatch,
    auto_approve_task_plan,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JobPlan,
    load_job_plan,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.plan_editing import consume_plan_approval, edit_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables

GOLDEN_DIR = Path(__file__).parent / "fixtures" / "plan_editing" / "golden"


def _task(tid: str, deps: list[str], acceptance: list[str]) -> dict:
    return {"id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
            "acceptance": acceptance, "depends_on": deps, "est_tokens_band": "S",
            "files_hint": ["docs/README.md"]}


_TASKS = [
    _task("T1", [], ["the parser reads a file"]),
    _task("T2", ["T1"], ["the report lists every row", "the report totals each column"]),
    _task("T3", ["T1"], ["the summary names the file"]),
]

#: The edits, each against the version the one before it produced.
_EDITS = [
    ("plan_split_task", {"task_id": "T2", "partition": [[0], [1]]}),
    ("plan_reorder", {"order": ["T1", "T3", "T2a", "T2b"]}),
    ("plan_edit_acceptance", {"task_id": "T3", "op": "add", "text": "the summary is logged"}),
]


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "README.md").write_text("# Demo\n")
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


def _save_pending(repo: Path) -> str:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
    body = plan.model_dump()
    body["_approval"] = "pending"
    body["_normalization"] = []
    tasks = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(tasks)
    job = JobPlan(job_title="F015 fidelity", repo_path=str(repo), task_plan=body, tasks=tasks,
                  state=RunState.PLANNED)
    save_job_plan(job)
    return str(job.job_id)


def _edit_all(job_id: str) -> None:
    for version, (command, args) in enumerate(_EDITS, start=1):
        edit_plan(job_id, command, args, expected_version=version, actor="cli")


def _approve(job_id: str) -> None:
    consume_plan_approval(load_job_plan(job_id), reason="approve", answers={}, questions=[])


def _run(job_id: str, monkeypatch: pytest.MonkeyPatch) -> tuple[JobPlan, list[str]]:
    """Run the job with the fake provider; return it and the planned ids in the order they ran."""
    import packages.orchestration.pingpong_loop as loop

    by_title = {t.title: t.inputs["plan"]["planned_id"] for t in load_job_plan(job_id).tasks}
    ran: list[str] = []
    real = loop.run_pingpong

    def recording(title, *args, **kwargs):
        ran.append(by_title[title])
        return real(title, *args, **kwargs)

    monkeypatch.setattr(loop, "run_pingpong", recording)
    provider = FakeProvider(pass_on_round=1, fail_on_round=99)
    done = run_job(job_id, builder_provider=provider,
                   reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                   repair_rounds=0)
    return done, ran


class TestTheEditedPlanRuns:

    def test_the_run_executes_the_edited_shape_in_the_edited_sequence(self, root, repo,
                                                                     monkeypatch):
        job_id = _save_pending(repo)
        _edit_all(job_id)
        _approve(job_id)
        done, ran = _run(job_id, monkeypatch)
        assert done.state == JOB_COMPLETED, done.error
        assert ran == ["T1", "T3", "T2a", "T2b"]

    def test_the_approval_records_the_hash_of_exactly_the_plan_it_approved(self, root, repo):
        job_id = _save_pending(repo)
        _edit_all(job_id)
        _approve(job_id)
        body = load_job_plan(job_id).task_plan
        assert body[APPROVED_PLAN_HASH_KEY] == plan_content_hash(body)
        assert body[APPROVED_PLAN_HASH_KEY].startswith("sha256:")
        assert approved_plan_mismatch(load_job_plan(job_id)) is None

    def test_a_rejection_records_no_hash(self, root, repo):
        job_id = _save_pending(repo)
        consume_plan_approval(load_job_plan(job_id), reason="reject", answers={}, questions=[])
        assert APPROVED_PLAN_HASH_KEY not in load_job_plan(job_id).task_plan

    def test_the_unattended_approval_records_the_hash_too(self, root, repo, tmp_path):
        job_id = _save_pending(repo)
        body = auto_approve_task_plan(load_job_plan(job_id).task_plan, tmp_path / "evidence")
        assert body[APPROVED_PLAN_HASH_KEY] == plan_content_hash(body)


class TestTheStartRefusesAnotherPlan:

    def _approved(self, repo: Path) -> str:
        job_id = _save_pending(repo)
        _edit_all(job_id)
        _approve(job_id)
        return job_id

    def test_a_plan_changed_after_its_approval_does_not_start(self, root, repo, monkeypatch):
        job_id = self._approved(repo)
        job = load_job_plan(job_id)
        job.task_plan["tasks"][1]["goal"] = "a goal nobody approved"
        save_job_plan(job)
        done, ran = _run(job_id, monkeypatch)
        assert done.state == JOB_BLOCKED
        assert done.error.startswith("plan_changed_since_approval: the plan hashes to ")
        assert ran == []

    def test_a_task_list_that_is_not_the_approved_plan_does_not_start(self, root, repo,
                                                                     monkeypatch):
        job_id = self._approved(repo)
        job = load_job_plan(job_id)
        job.tasks = [job.tasks[0], job.tasks[2], job.tasks[1], job.tasks[3]]
        save_job_plan(job)
        done, ran = _run(job_id, monkeypatch)
        assert done.state == JOB_BLOCKED
        assert "not as the approved plan's ['T1', 'T3', 'T2a', 'T2b']" in done.error
        assert ran == []

    def test_a_plan_approved_before_the_hash_existed_is_not_refused(self, root, repo):
        job_id = _save_pending(repo)
        job = load_job_plan(job_id)
        job.task_plan["_approval"] = "approved"
        assert approved_plan_mismatch(job) is None

    def test_the_bookkeeping_beside_the_plan_is_not_hashed(self, root, repo):
        job_id = self._approved(repo)
        body = load_job_plan(job_id).task_plan
        recorded = plan_content_hash(body)
        body["_approval_audit"] = {"mode": "human"}
        body["_edits"] = []
        assert plan_content_hash(body) == recorded


class TestThePlanRevisionsAreGolden:

    @pytest.mark.parametrize("name", ["plan_v2.md", "plan_v3.md", "plan_v4.md"])
    def test_each_revision_renders_its_golden(self, root, repo, name):
        job_id = _save_pending(repo)
        _edit_all(job_id)
        rendered = (job_evidence_export_dir(job_id) / name).read_text(encoding="utf-8")
        assert rendered == (GOLDEN_DIR / name).read_text(encoding="utf-8")

    def test_the_golden_directory_holds_exactly_the_three_revisions(self):
        assert sorted(p.name for p in GOLDEN_DIR.iterdir()) == [
            "plan_v2.md", "plan_v3.md", "plan_v4.md"]
