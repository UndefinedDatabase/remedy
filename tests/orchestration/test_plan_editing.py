"""F015 T001 — the plan-editing backend: every edit kind, its revalidation and its atomicity.

The fixture is a job as ``do_sequence`` persists a freshly planned one: a ``task_plan`` body
holding the model's fields plus ``_approval: pending`` and ``_normalization``, and the task
list ``map_task_plan_to_tasks`` derives from it. Every refusal is checked to leave the job
record byte-identical and to write no derived file.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import plan_editing
from packages.orchestration.data_paths import job_evidence_export_dir, job_record_path
from packages.orchestration.job_plan import map_task_plan_to_tasks
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan
from packages.orchestration.plan_editing import (
    EDIT_LOG_EVIDENCE,
    PLAN_EDIT_COMMANDS,
    PlanEditRefused,
    consume_plan_approval,
    edit_plan,
    plan_edit_lock,
    replay_edits,
)
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables


def _task(tid: str, deps: list[str], acceptance: list[str] | None = None) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": acceptance or [f"{tid} works"], "depends_on": deps,
        "est_tokens_band": "S", "files_hint": [f"src/{tid.lower()}.py"],
    }


# T1 <- T2 <- T3, and T4 waits for both T2 and T1: deleting T2 must hand T3 and T4 its T1.
_TASKS = [
    _task("T1", []),
    _task("T2", ["T1"], ["parser reads a file", "parser reports errors", "parser is fast"]),
    _task("T3", ["T2"]),
    _task("T4", ["T2", "T1"]),
]


def _save_job(root: Path, tasks: list[dict], *, approval: str = "pending",
              state: RunState = RunState.PLANNED) -> str:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = approval
    body["_normalization"] = []
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="t", task_plan=body, tasks=mapped, state=state)
    save_job_plan(job, root)
    return job.job_id


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


def _edit(root: Path, job_id: str, command: str, args: dict, version: int = 1):
    return edit_plan(job_id, command, args, expected_version=version, actor="tf:test", root=root)


def _ids_and_deps(root: Path, job_id: str) -> list[tuple[str, list[str]]]:
    body = load_job_plan(job_id, root).task_plan
    return [(t["id"], t["depends_on"]) for t in body["tasks"]]


def _assert_refused_unchanged(root: Path, job_id: str, command: str, args: dict, code: str,
                              *, version: int = 1, says: str = "") -> PlanEditRefused:
    record = job_record_path(job_id, root)
    before = record.read_bytes()
    with pytest.raises(PlanEditRefused) as caught:
        _edit(root, job_id, command, args, version)
    assert caught.value.code == code, caught.value
    assert says in caught.value.detail
    assert record.read_bytes() == before
    evidence = job_evidence_export_dir(job_id, root)
    assert not (evidence / EDIT_LOG_EVIDENCE).exists()
    assert not list(evidence.glob("plan_v*.md")) if evidence.exists() else True
    return caught.value


class TestEachEditRoundTrips:

    def test_edit_task_persists_the_plan_its_version_log_tasks_and_derived_files(self, root):
        job_id = _save_job(root, _TASKS)
        result = _edit(root, job_id, "plan_edit_task",
                       {"task_id": "T3", "fields": {"title": "Wire T3", "est_tokens_band": "L"}})
        assert result.version == 2
        job = load_job_plan(job_id, root)
        t3 = job.task_plan["tasks"][2]
        assert (t3["title"], t3["est_tokens_band"]) == ("Wire T3", "L")
        assert job.task_plan["_version"] == 2 and job.task_plan["_approval"] == "pending"
        assert job.task_plan["_normalization"] == []
        # The task list the executor reads is regenerated from the edited plan.
        assert job.tasks[2].title == "Wire T3: goal of T3"
        assert job.tasks[2].inputs["plan"]["est_tokens_band"] == "L"
        [entry] = job.task_plan["_edits"]
        assert (entry["version"], entry["actor"], entry["command"]) == (2, "tf:test", "plan_edit_task")
        assert entry["before"][2]["title"] == "Build T3" and entry["after"][2]["title"] == "Wire T3"
        evidence = job_evidence_export_dir(job_id, root)
        assert result.plan_md == evidence / "plan_v2.md"
        assert "### 3. T3 — Wire T3" in result.plan_md.read_text(encoding="utf-8")
        exported = json.loads((evidence / EDIT_LOG_EVIDENCE).read_text(encoding="utf-8"))
        assert exported["version"] == 2 and exported["edits"] == job.task_plan["_edits"]

    def test_delete_hands_dependents_the_deleted_tasks_own_dependencies(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_delete_task", {"task_id": "T2"})
        assert _ids_and_deps(root, job_id) == [("T1", []), ("T3", ["T1"]), ("T4", ["T1"])]

    def test_delete_of_a_root_leaves_its_dependents_with_their_other_dependencies(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_delete_task", {"task_id": "T1"})
        assert _ids_and_deps(root, job_id) == [("T2", []), ("T3", ["T2"]), ("T4", ["T2"])]

    def test_reorder_persists_the_explicit_order(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_reorder", {"order": ["T1", "T2", "T4", "T3"]})
        assert [t for t, _ in _ids_and_deps(root, job_id)] == ["T1", "T2", "T4", "T3"]
        assert [t.inputs["plan"]["planned_id"] for t in load_job_plan(job_id, root).tasks] == [
            "T1", "T2", "T4", "T3"]

    def test_merge_fuses_the_named_tasks_and_rewires_their_dependents(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_merge_tasks", {"task_ids": ["T3", "T2"]})
        body = load_job_plan(job_id, root).task_plan
        assert _ids_and_deps(root, job_id) == [("T1", []), ("T2", ["T1"]), ("T4", ["T2", "T1"])]
        merged = body["tasks"][1]
        assert merged["acceptance"] == [
            "parser reads a file", "parser reports errors", "parser is fast", "T3 works"]
        assert merged["title"] == "Build T2 + Build T3" and merged["est_tokens_band"] == "M"

    def test_merge_points_a_dropped_members_dependents_at_the_surviving_task(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_merge_tasks", {"task_ids": ["T1", "T2"]})
        assert _ids_and_deps(root, job_id) == [("T1", []), ("T3", ["T1"]), ("T4", ["T1"])]

    def test_split_partitions_acceptance_into_a_chain_its_dependents_wait_for(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_split_task", {"task_id": "T2", "partition": [[0, 2], [1]]})
        body = load_job_plan(job_id, root).task_plan
        assert _ids_and_deps(root, job_id) == [
            ("T1", []), ("T2a", ["T1"]), ("T2b", ["T2a"]), ("T3", ["T2b"]), ("T4", ["T2b", "T1"])]
        assert body["tasks"][1]["acceptance"] == ["parser reads a file", "parser is fast"]
        assert body["tasks"][2]["acceptance"] == ["parser reports errors"]

    def test_edit_acceptance_adds_edits_and_removes_one_criterion_at_a_time(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_edit_acceptance", {"task_id": "T2", "op": "add", "text": "docs"})
        _edit(root, job_id, "plan_edit_acceptance",
              {"task_id": "T2", "op": "edit", "index": 0, "text": "parser reads two files"}, 2)
        _edit(root, job_id, "plan_edit_acceptance", {"task_id": "T2", "op": "remove", "index": 2}, 3)
        body = load_job_plan(job_id, root).task_plan
        assert body["tasks"][1]["acceptance"] == [
            "parser reads two files", "parser reports errors", "docs"]
        assert body["_version"] == 4 and len(body["_edits"]) == 3
        assert (job_evidence_export_dir(job_id, root) / "plan_v4.md").is_file()


class TestInvalidEditsChangeNothing:

    @pytest.mark.parametrize(("command", "args", "code", "says"), [
        ("plan_edit_task", {"task_id": "T1", "fields": {"id": "X"}}, "invalid_args", "not editable"),
        ("plan_edit_task", {"task_id": "T1", "fields": {"clarifications_resolved": []}},
         "invalid_args", "immutable"),
        ("plan_edit_task", {"task_id": "T1", "fields": {"est_tokens_band": "XXL"}},
         "invalid_plan", "'S', 'M', 'L' or 'XL'"),
        ("plan_edit_task", {"task_id": "T1", "fields": {"title": "Inspect the code"}},
         "invalid_plan", "inspection"),
        ("plan_edit_task", {"task_id": "T9", "fields": {"title": "x"}}, "unknown_task", "T9"),
        ("plan_edit_task", {"task_id": "T1", "fields": {"title": "Build T1"}},
         "invalid_args", "changes nothing"),
        ("plan_reorder", {"order": ["T1", "T2", "T3"]}, "invalid_args", "missing: ['T4']"),
        ("plan_reorder", {"order": ["T1", "T2", "T3", "T3"]}, "invalid_args", "exactly once"),
        # DECISION F015 D4: a job runs its tasks in plan order, so none may precede its own.
        ("plan_reorder", {"order": ["T2", "T1", "T3", "T4"]}, "invalid_plan",
         "task 'T2' comes before 'T1', which it waits for"),
        ("plan_merge_tasks", {"task_ids": ["T1"]}, "invalid_args", "at least two"),
        ("plan_merge_tasks", {"task_ids": ["T1", "T3"]}, "invalid_plan", "cycle"),
        ("plan_split_task", {"task_id": "T2", "partition": [[0, 1, 2]]}, "invalid_args", "two"),
        ("plan_split_task", {"task_id": "T2", "partition": [[0, 1], [1]]}, "invalid_args",
         "exactly one group"),
        ("plan_edit_acceptance", {"task_id": "T1", "op": "remove", "index": 0},
         "invalid_plan", "at least 1 item"),
        ("plan_edit_acceptance", {"task_id": "T1", "op": "edit", "index": 3, "text": "x"},
         "invalid_args", "0 to 0"),
        ("plan_edit_acceptance", {"task_id": "T1", "op": "edit", "index": 0, "text": " "},
         "invalid_plan", "must not be empty"),
        ("plan_edit_acceptance", {"task_id": "T1", "op": "rename"}, "invalid_args", "op must"),
        ("plan_delete_everything", {}, "unknown_command", "plan_edit_task"),
    ])
    def test_refused_edit_names_the_violation_and_writes_nothing(self, root, command, args, code,
                                                                 says):
        job_id = _save_job(root, _TASKS)
        refused = _assert_refused_unchanged(root, job_id, command, args, code, says=says)
        assert refused.current_version == 1

    def test_deleting_the_last_task_is_refused_by_the_schema(self, root):
        job_id = _save_job(root, [_task("T1", [])])
        _assert_refused_unchanged(root, job_id, "plan_delete_task", {"task_id": "T1"},
                                  "invalid_plan", says="at least 1 item")

    def test_a_job_without_a_task_plan_is_refused(self, root):
        job = JobPlan(job_title="t")
        save_job_plan(job, root)
        _assert_refused_unchanged(root, job.job_id, "plan_delete_task", {"task_id": "T1"},
                                  "no_task_plan")


class TestTheEditWindow:

    @pytest.mark.parametrize(("approval", "state", "says"), [
        ("approved", RunState.PLANNED, "the plan is approved"),
        ("rejected", RunState.PLANNED, "the plan is rejected"),
        ("pending", RunState.RUNNING, "the job is running"),
        ("pending", RunState.COMPLETED, "the job is completed"),
    ])
    def test_an_approved_rejected_or_started_plan_refuses_with_its_state(self, root, approval,
                                                                         state, says):
        job_id = _save_job(root, _TASKS, approval=approval, state=state)
        _assert_refused_unchanged(root, job_id, "plan_delete_task", {"task_id": "T4"},
                                  "plan_not_editable", says=says)

    def test_a_stale_version_gets_a_conflict_naming_the_current_one(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_delete_task", {"task_id": "T4"})
        record = job_record_path(job_id, root)
        before = record.read_bytes()
        with pytest.raises(PlanEditRefused) as caught:
            _edit(root, job_id, "plan_delete_task", {"task_id": "T3"}, version=1)
        assert (caught.value.code, caught.value.current_version) == ("version_conflict", 2)
        assert record.read_bytes() == before

    def test_an_edit_waits_for_the_plan_lock_and_gives_up_cleanly(self, root, monkeypatch):
        monkeypatch.setattr(plan_editing, "_LOCK_TIMEOUT_SEC", 0.2)
        job_id = _save_job(root, _TASKS)
        with plan_edit_lock(job_id, root):
            _assert_refused_unchanged(root, job_id, "plan_delete_task", {"task_id": "T4"},
                                      "lock_timeout")


class TestTheLogReconstructsThePlan:

    def test_replaying_the_log_from_the_original_reaches_the_stored_plan(self, root):
        job_id = _save_job(root, _TASKS)
        original = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
        steps = [
            ("plan_split_task", {"task_id": "T2", "partition": [[0], [1, 2]]}),
            ("plan_edit_task", {"task_id": "T3", "fields": {"goal": "a sharper goal"}}),
            ("plan_reorder", {"order": ["T1", "T2a", "T2b", "T4", "T3"]}),
            ("plan_delete_task", {"task_id": "T2a"}),
            ("plan_edit_acceptance", {"task_id": "T4", "op": "add", "index": 0, "text": "first"}),
        ]
        for version, (command, args) in enumerate(steps, start=1):
            _edit(root, job_id, command, args, version)
        body = load_job_plan(job_id, root).task_plan
        replayed = replay_edits(original, body["_edits"])
        assert [t.model_dump() for t in replayed.tasks] == body["tasks"]
        assert [e["version"] for e in body["_edits"]] == [2, 3, 4, 5, 6]

    def test_a_log_that_does_not_reconstruct_the_plan_is_named(self, root):
        job_id = _save_job(root, _TASKS)
        _edit(root, job_id, "plan_delete_task", {"task_id": "T4"})
        _edit(root, job_id, "plan_delete_task", {"task_id": "T3"}, 2)
        edits = load_job_plan(job_id, root).task_plan["_edits"]
        edits[1]["args"]["task_id"] = "T2"
        original = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
        with pytest.raises(ValueError, match="edit 1 .version 3. does not replay"):
            replay_edits(original, edits)


def test_the_six_commands_are_the_feature_files_six():
    assert PLAN_EDIT_COMMANDS == (
        "plan_edit_task", "plan_delete_task", "plan_reorder", "plan_merge_tasks",
        "plan_split_task", "plan_edit_acceptance")


class TestTheApprovalClosesTheWindow:
    """DECISION F015 D2: the approval is consumed under the plan-edit lock against the record."""

    def _approve(self, job, root):
        return consume_plan_approval(job, reason="approve", answers={}, questions=[], root=root)

    def test_an_edit_accepted_after_the_door_loaded_the_job_is_approved_not_lost(self, root):
        job_id = _save_job(root, _TASKS)
        stale = load_job_plan(job_id, root)
        _edit(root, job_id, "plan_delete_task", {"task_id": "T4"})
        self._approve(stale, root)
        stored = load_job_plan(job_id, root)
        assert stored.task_plan["_approval"] == "approved"
        assert [t["id"] for t in stored.task_plan["tasks"]] == ["T1", "T2", "T3"]
        assert stored.task_plan["_version"] == 2 and len(stored.task_plan["_edits"]) == 1
        assert [t.inputs["plan"]["planned_id"] for t in stored.tasks] == ["T1", "T2", "T3"]

    def test_a_second_approval_finds_the_approval_closed_and_writes_nothing(self, root):
        job_id = _save_job(root, _TASKS)
        self._approve(load_job_plan(job_id, root), root)
        record = job_record_path(job_id, root)
        before = record.read_bytes()
        with pytest.raises(PlanEditRefused) as caught:
            self._approve(load_job_plan(job_id, root), root)
        assert caught.value.code == "approval_closed"
        assert "the plan is approved" in caught.value.detail
        assert record.read_bytes() == before

    def test_an_edit_after_the_approval_is_refused_with_the_state(self, root):
        job_id = _save_job(root, _TASKS)
        self._approve(load_job_plan(job_id, root), root)
        _assert_refused_unchanged(root, job_id, "plan_delete_task", {"task_id": "T4"},
                                  "plan_not_editable", says="the plan is approved")

    def test_the_approval_waits_for_an_edit_in_progress(self, root, monkeypatch):
        monkeypatch.setattr(plan_editing, "_LOCK_TIMEOUT_SEC", 0.2)
        job_id = _save_job(root, _TASKS)
        record = job_record_path(job_id, root)
        before = record.read_bytes()
        with plan_edit_lock(job_id, root), pytest.raises(PlanEditRefused) as caught:
            self._approve(load_job_plan(job_id, root), root)
        assert caught.value.code == "lock_timeout"
        assert record.read_bytes() == before
