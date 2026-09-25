"""F026 T001 — the runtime task edit backend: the state gate, the versioned in-place apply,
the spec archive, the approval seal and the failed-to-pending reset (DECISION F026 D1).

The fixture is a job as ``do_sequence`` persists a freshly APPROVED one: a ``task_plan`` body
holding the model's fields plus ``_approval: approved`` and the hash ``consume_plan_approval``
would record, and the task list ``map_task_plan_to_tasks`` derives from it — mirroring
``tests/orchestration/test_plan_editing.py``'s own ``_save_job``, but past the approval gate
this module's edit lives beyond.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import pause_control, safe_points
from packages.orchestration import pingpong_job as ppj
from packages.orchestration import task_edit_runtime as ter
from packages.orchestration.data_paths import job_evidence_export_dir, job_record_path
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    approved_plan_mismatch,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan
from packages.orchestration.plan_editing import (
    EDIT_LOG_EVIDENCE,
    EDIT_LOG_KEY,
    PlanEditRefused,
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


_TASKS = [_task("T1", []), _task("T2", []), _task("T3", []), _task("T4", []), _task("T5", [])]


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
    return data


def _save_job(root: Path, tasks: list[dict], *, state: RunState = RunState.PLANNED,
              approval: str = "approved") -> str:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = approval
    body["_normalization"] = []
    if approval == "approved":
        body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="t", task_plan=body, tasks=mapped, state=state)
    save_job_plan(job, root)
    return job.job_id


def _by_planned(job: JobPlan, planned_id: str) -> tuple[int, ppj.TaskEntry]:
    for i, t in enumerate(job.tasks):
        if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
            return i, t
    raise AssertionError(f"no task for planned id {planned_id!r}")


def _task_id_of(root: Path, job_id: str, planned_id: str) -> str:
    return _by_planned(load_job_plan(job_id, root), planned_id)[1].task_id


def _mutate(root: Path, job_id: str, planned_id: str, **updates) -> None:
    job = load_job_plan(job_id, root)
    _, entry = _by_planned(job, planned_id)
    for k, v in updates.items():
        setattr(entry, k, v)
    save_job_plan(job, root)


def _set_job_state(root: Path, job_id: str, state: RunState) -> None:
    job = load_job_plan(job_id, root)
    job.state = state
    save_job_plan(job, root)


def _edit(root: Path, job_id: str, task_id: str, fields: dict, *, version: int = 1,
          actor: str = "tf:test") -> ter.TaskEditResult:
    return ter.edit_task_at_runtime(
        job_id, task_id, fields, expected_spec_version=version, actor=actor, root=root)


def _evidence_file_names(root: Path, job_id: str) -> list[str]:
    # S2: the export directory's OWN files (`plan_v<n>.md`, the edit-log export) —
    # not `task_specs/`, which `_assert_refused` already compares separately.
    evidence_dir = job_evidence_export_dir(job_id, root)
    if not evidence_dir.exists():
        return []
    return sorted(p.name for p in evidence_dir.iterdir() if p.is_file())


def _assert_refused(root: Path, job_id: str, task_id: str, fields: dict, code: str, *,
                    version: int = 1, says: str = "") -> PlanEditRefused:
    before = job_record_path(job_id, root).read_bytes()
    specs_dir = job_evidence_export_dir(job_id, root) / "task_specs"
    before_specs = sorted(specs_dir.glob("*")) if specs_dir.exists() else []
    before_evidence_names = _evidence_file_names(root, job_id)
    with pytest.raises(PlanEditRefused) as caught:
        _edit(root, job_id, task_id, fields, version=version)
    assert caught.value.code == code, caught.value
    assert says in caught.value.detail
    assert job_record_path(job_id, root).read_bytes() == before
    after_specs = sorted(specs_dir.glob("*")) if specs_dir.exists() else []
    assert after_specs == before_specs
    assert _evidence_file_names(root, job_id) == before_evidence_names
    return caught.value


# ---------------------------------------------------------------------------
# S3 — the state gate, pure
# ---------------------------------------------------------------------------

_ALL_TASK_STATUSES = (
    ppj.TASK_PENDING, ppj.TASK_RUNNING, ppj.TASK_PASSED, ppj.TASK_APPLIED,
    ppj.TASK_BLOCKED, ppj.TASK_FAILED, ppj.TASK_SKIPPED, ppj.TASK_SPLIT,
)


class TestStateGateTaskStatusMatrix:

    def test_pending_not_paused_is_waiting(self):
        assert ter.runtime_edit_state(
            RunState.PLANNED, "approved", ppj.TASK_PENDING, task_paused=False) == "waiting"

    def test_pending_paused_is_paused(self):
        assert ter.runtime_edit_state(
            RunState.PLANNED, "approved", ppj.TASK_PENDING, task_paused=True) == "paused"

    @pytest.mark.parametrize("status", [ppj.TASK_BLOCKED, ppj.TASK_FAILED])
    def test_failed_or_blocked_is_failed(self, status):
        assert ter.runtime_edit_state(
            RunState.PLANNED, "approved", status, task_paused=False) == "failed"

    @pytest.mark.parametrize("status", [
        s for s in _ALL_TASK_STATUSES if s not in (ppj.TASK_PENDING, ppj.TASK_BLOCKED, ppj.TASK_FAILED)
    ])
    def test_every_other_status_refuses_task_not_editable(self, status):
        with pytest.raises(PlanEditRefused) as caught:
            ter.runtime_edit_state(RunState.PLANNED, "approved", status, task_paused=False)
        assert caught.value.code == "task_not_editable"
        assert status in caught.value.detail


class TestStateGateJobStateMatrix:

    @pytest.mark.parametrize("state", [
        RunState.RUNNING, RunState.COMPLETED, RunState.FAILED, RunState.CANCELLED])
    def test_running_and_terminal_states_refuse_job_not_editable(self, state):
        with pytest.raises(PlanEditRefused) as caught:
            ter.runtime_edit_state(state, "approved", ppj.TASK_PENDING, task_paused=False)
        assert caught.value.code == "job_not_editable"
        assert state.value in caught.value.detail

    @pytest.mark.parametrize("state", [
        RunState.PENDING, RunState.PLANNED, RunState.PAUSED, RunState.BLOCKED, RunState.STOPPED])
    def test_every_other_job_state_passes_the_job_check(self, state):
        assert ter.runtime_edit_state(
            state, "approved", ppj.TASK_PENDING, task_paused=False) == "waiting"


class TestStateGateApproval:

    @pytest.mark.parametrize("approval", ["pending", "rejected"])
    def test_open_or_rejected_approval_refuses_plan_not_editable(self, approval):
        with pytest.raises(PlanEditRefused) as caught:
            ter.runtime_edit_state(
                RunState.PLANNED, approval, ppj.TASK_PENDING, task_paused=False)
        assert caught.value.code == "plan_not_editable"
        assert approval in caught.value.detail


# ---------------------------------------------------------------------------
# S4 — accepted through every editable state
# ---------------------------------------------------------------------------

class TestAcceptedThroughEveryEditableState:

    def test_waiting_task_is_edited(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        result = _edit(root, job_id, task_id, {"title": "Renamed", "goal": "new goal"})
        assert result.state == "waiting"
        _, entry = _by_planned(load_job_plan(job_id, root), "T1")
        assert entry.title == "Renamed: new goal"

    def test_paused_by_a_task_pause_file(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        pause_control.request_task_pause(
            job_id, task_id, control_root_path=safe_points.control_root(root))
        result = _edit(root, job_id, task_id, {"title": "Renamed", "goal": "new goal"})
        assert result.state == "paused"

    def test_paused_by_a_paused_job(self, root):
        job_id = _save_job(root, _TASKS)
        _set_job_state(root, job_id, RunState.PAUSED)
        task_id = _task_id_of(root, job_id, "T1")
        result = _edit(root, job_id, task_id, {"title": "Renamed", "goal": "new goal"})
        assert result.state == "paused"

    def test_failed_task_is_edited_and_reset(self, root):
        job_id = _save_job(root, _TASKS)
        _mutate(root, job_id, "T2", status=ppj.TASK_FAILED, error="boom")
        task_id = _task_id_of(root, job_id, "T2")
        result = _edit(root, job_id, task_id, {"title": "Fixed", "goal": "fixed goal"})
        assert result.state == "failed"
        _, entry = _by_planned(load_job_plan(job_id, root), "T2")
        assert entry.status == ppj.TASK_PENDING
        assert entry.error == ""

    def test_blocked_task_is_edited_and_reset(self, root):
        job_id = _save_job(root, _TASKS)
        _mutate(root, job_id, "T2", status=ppj.TASK_BLOCKED, error="blocked")
        task_id = _task_id_of(root, job_id, "T2")
        result = _edit(root, job_id, task_id, {"title": "Fixed", "goal": "fixed goal"})
        assert result.state == "failed"
        _, entry = _by_planned(load_job_plan(job_id, root), "T2")
        assert entry.status == ppj.TASK_PENDING
        assert entry.error == ""


# ---------------------------------------------------------------------------
# Refusals write nothing
# ---------------------------------------------------------------------------

class TestRefusalsWriteNothing:

    @pytest.mark.parametrize("status", [ppj.TASK_RUNNING, ppj.TASK_PASSED, ppj.TASK_APPLIED])
    def test_task_not_editable_status(self, root, status):
        job_id = _save_job(root, _TASKS)
        _mutate(root, job_id, "T1", status=status)
        task_id = _task_id_of(root, job_id, "T1")
        _assert_refused(root, job_id, task_id, {"title": "x", "goal": "y"}, "task_not_editable")

    def test_revalidation_refusal_empty_acceptance(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _assert_refused(root, job_id, task_id, {"acceptance": []}, "invalid_plan")

    def test_unknown_field_refused(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _assert_refused(
            root, job_id, task_id, {"bogus": "x"}, "invalid_args", says="not editable")

    def test_version_conflict_names_the_current_version(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        caught = _assert_refused(
            root, job_id, task_id, {"title": "x", "goal": "y"}, "version_conflict", version=99)
        assert caught.current_version == 1

    def test_unknown_task_id(self, root):
        job_id = _save_job(root, _TASKS)
        _assert_refused(
            root, job_id, "no-such-task-id", {"title": "x", "goal": "y"}, "unknown_task")

    def test_task_without_a_planned_id(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _mutate(root, job_id, "T1", inputs={})
        _assert_refused(root, job_id, task_id, {"title": "x", "goal": "y"}, "not_a_plan_task")


# ---------------------------------------------------------------------------
# S5 — the archive
# ---------------------------------------------------------------------------

class TestArchive:

    def test_archive_path_and_content(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _, before_entry = _by_planned(load_job_plan(job_id, root), "T1")
        before_title, before_acceptance = before_entry.title, before_entry.acceptance

        result = _edit(root, job_id, task_id, {"title": "Renamed", "goal": "new goal"})

        evidence = job_evidence_export_dir(job_id, root)
        archive_path = evidence / "task_specs" / "T1.v1.json"
        assert result.archive_path == archive_path
        payload = json.loads(archive_path.read_text(encoding="utf-8"))
        assert payload["task_id"] == task_id
        assert payload["planned_id"] == "T1"
        assert payload["spec_version"] == 1
        assert payload["state"] == "waiting"
        assert payload["title"] == before_title
        assert payload["acceptance"] == before_acceptance
        assert payload["plan_task"]["title"] == "Build T1"
        assert "archived_at" in payload

    def test_second_edit_writes_v2_and_leaves_v1_byte_identical(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _edit(root, job_id, task_id, {"title": "Renamed", "goal": "new goal"})
        evidence = job_evidence_export_dir(job_id, root)
        v1_path = evidence / "task_specs" / "T1.v1.json"
        v1_bytes = v1_path.read_bytes()

        _edit(root, job_id, task_id, {"title": "Renamed2", "goal": "g2"}, version=2)

        v2_path = evidence / "task_specs" / "T1.v2.json"
        assert v2_path.is_file()
        assert v1_path.read_bytes() == v1_bytes

    def test_equal_archive_crash_case_is_kept_and_the_edit_proceeds(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        job = load_job_plan(job_id, root)
        _, entry = _by_planned(job, "T1")
        body = job.task_plan
        plan = TaskPlan.model_validate({k: v for k, v in body.items() if not k.startswith("_")})
        plan_task = next(t for t in plan.tasks if t.id == "T1").model_dump()
        payload = {
            "plan_task": plan_task,
            "title": entry.title,
            "acceptance": entry.acceptance,
            "task_id": entry.task_id,
            "planned_id": "T1",
            "spec_version": 1,
            "state": "waiting",
            "archived_at": "1999-01-01T00:00:00+00:00",
        }
        evidence = job_evidence_export_dir(job_id, root)
        archive_dir = evidence / "task_specs"
        archive_dir.mkdir(parents=True)
        archive_path = archive_dir / "T1.v1.json"
        archive_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8")

        before_record = job_record_path(job_id, root).read_bytes()
        result = _edit(root, job_id, task_id, {"title": "Renamed", "goal": "new goal"})

        assert result.state == "waiting"
        reread = json.loads(archive_path.read_text(encoding="utf-8"))
        assert reread["archived_at"] == "1999-01-01T00:00:00+00:00"
        assert job_record_path(job_id, root).read_bytes() != before_record

    def test_conflicting_archive_refuses_and_writes_nothing(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        evidence = job_evidence_export_dir(job_id, root)
        archive_dir = evidence / "task_specs"
        archive_dir.mkdir(parents=True)
        archive_path = archive_dir / "T1.v1.json"
        conflicting = {
            "plan_task": {}, "title": "someone else's", "acceptance": "x", "task_id": "other",
            "planned_id": "T1", "spec_version": 1, "state": "waiting",
            "archived_at": "1999-01-01T00:00:00+00:00",
        }
        archive_path.write_text(json.dumps(conflicting, indent=2, sort_keys=True) + "\n",
                                encoding="utf-8")
        before_bytes = archive_path.read_bytes()

        _assert_refused(
            root, job_id, task_id, {"title": "x", "goal": "y"}, "spec_archive_conflict")
        assert archive_path.read_bytes() == before_bytes

    def test_planned_id_with_a_slash_is_archived_under_its_digest(self, root):
        job_id = _save_job(root, [_task("weird/id", [])])
        task_id = _task_id_of(root, job_id, "weird/id")

        result = _edit(root, job_id, task_id, {"title": "x", "goal": "y"})

        digest = hashlib.sha256(b"weird/id").hexdigest()[:32]
        expected = job_evidence_export_dir(job_id, root) / "task_specs" / f"{digest}.v1.json"
        assert result.archive_path == expected
        assert expected.is_file()


# ---------------------------------------------------------------------------
# S6 — the in-place update and its log entry
# ---------------------------------------------------------------------------

class TestInPlaceUpdateAndTheLog:

    def test_keeps_identity_fields_and_updates_the_prompt_fields(self, root):
        job_id = _save_job(root, _TASKS)
        _mutate(root, job_id, "T1", run_id="run-abc", repair_rounds_used=3)
        job = load_job_plan(job_id, root)
        _, entry = _by_planned(job, "T1")
        entry.inputs["foreign"] = "keep-me"
        save_job_plan(job, root)
        task_id = entry.task_id

        result = _edit(root, job_id, task_id, {
            "title": "New Title", "goal": "new goal",
            "acceptance": ["criterion a", "criterion b"],
        })
        assert result.spec_version == 2

        job = load_job_plan(job_id, root)
        _, entry = _by_planned(job, "T1")
        assert entry.task_id == task_id
        assert entry.run_id == "run-abc"
        assert entry.repair_rounds_used == 3
        assert entry.inputs["foreign"] == "keep-me"
        assert entry.title == "New Title: new goal"
        assert entry.acceptance == "criterion a\ncriterion b"
        assert entry.spec_version == 2
        assert job.task_plan["_version"] == 2

        result2 = _edit(root, job_id, task_id, {"title": "Newer", "goal": "newer goal"},
                        version=2)
        assert result2.spec_version == 3
        job = load_job_plan(job_id, root)
        assert job.task_plan["_version"] == 3
        assert _by_planned(job, "T1")[1].spec_version == 3

    def test_runtime_object_carries_every_key(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        result = _edit(root, job_id, task_id, {"title": "x", "goal": "y"})
        runtime = result.entry["runtime"]
        assert set(runtime) == {
            "task_id", "planned_id", "state", "spec_version", "status_before",
            "status_after", "restored", "approved_plan_sha256_before",
            "approved_plan_sha256_after", "archive",
        }
        assert runtime["task_id"] == task_id
        assert runtime["planned_id"] == "T1"
        assert runtime["state"] == "waiting"
        assert runtime["spec_version"] == 2
        assert runtime["status_before"] == ppj.TASK_PENDING
        assert runtime["status_after"] == ppj.TASK_PENDING
        assert runtime["restored"] == []
        assert result.entry["command"] == "plan_edit_task"

    def test_replay_edits_reconstructs_the_stored_plan(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _edit(root, job_id, task_id, {"title": "x1", "goal": "y1"})
        _edit(root, job_id, task_id, {"title": "x2", "goal": "y2"}, version=2)

        job = load_job_plan(job_id, root)
        body = job.task_plan
        original = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": _TASKS})
        rebuilt = replay_edits(original, body[EDIT_LOG_KEY])
        assert [t.model_dump() for t in rebuilt.tasks] == body["tasks"]

    def test_approval_hash_reseals_and_mismatch_reads_none(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        _edit(root, job_id, task_id, {"title": "x", "goal": "y"})
        job = load_job_plan(job_id, root)
        assert approved_plan_mismatch(job) is None


# ---------------------------------------------------------------------------
# S7 — the reset
# ---------------------------------------------------------------------------

class TestReset:

    @pytest.mark.parametrize("failing_status", [ppj.TASK_FAILED, ppj.TASK_BLOCKED])
    def test_reset_restores_skipped_tasks_after_it_not_before(self, root, failing_status):
        job_id = _save_job(root, _TASKS)
        _mutate(root, job_id, "T1", status=ppj.TASK_SKIPPED)                     # before
        _mutate(root, job_id, "T2", status=failing_status, error="boom")         # the edit
        _mutate(root, job_id, "T3", status=ppj.TASK_SKIPPED)                     # after
        _mutate(root, job_id, "T4", status=ppj.TASK_SKIPPED)                     # after
        _mutate(root, job_id, "T5", status=ppj.TASK_PASSED)                      # after, not skipped

        task_id = _task_id_of(root, job_id, "T2")
        result = _edit(root, job_id, task_id, {"title": "Fixed", "goal": "fixed"})
        assert result.state == "failed"

        job = load_job_plan(job_id, root)
        statuses = {pid: _by_planned(job, pid)[1].status
                   for pid in ("T1", "T2", "T3", "T4", "T5")}
        assert statuses["T1"] == ppj.TASK_SKIPPED
        assert statuses["T2"] == ppj.TASK_PENDING
        assert statuses["T3"] == ppj.TASK_PENDING
        assert statuses["T4"] == ppj.TASK_PENDING
        assert statuses["T5"] == ppj.TASK_PASSED
        assert _by_planned(job, "T2")[1].error == ""

        t3_id = _by_planned(job, "T3")[1].task_id
        t4_id = _by_planned(job, "T4")[1].task_id
        assert result.restored == (t3_id, t4_id)


# ---------------------------------------------------------------------------
# S8 — the derived evidence
# ---------------------------------------------------------------------------

class TestEvidenceWritten:

    def test_plan_md_and_edit_log_export_written(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        result = _edit(root, job_id, task_id, {"title": "x", "goal": "y"})

        evidence = job_evidence_export_dir(job_id, root)
        assert (evidence / f"plan_v{result.plan_version}.md").is_file()
        exported = json.loads((evidence / EDIT_LOG_EVIDENCE).read_text(encoding="utf-8"))
        assert exported["version"] == result.plan_version
        job = load_job_plan(job_id, root)
        assert exported["edits"] == job.task_plan[EDIT_LOG_KEY]

    def test_task_spec_versions_ascending(self, root):
        job_id = _save_job(root, _TASKS)
        task_id = _task_id_of(root, job_id, "T1")
        assert ter.task_spec_versions(job_id, "T1", root=root) == ()

        _edit(root, job_id, task_id, {"title": "x1", "goal": "y1"})
        _edit(root, job_id, task_id, {"title": "x2", "goal": "y2"}, version=2)

        versions = ter.task_spec_versions(job_id, "T1", root=root)
        assert [v["spec_version"] for v in versions] == [1, 2]


# ---------------------------------------------------------------------------
# S1 — the field's own round trip
# ---------------------------------------------------------------------------

class TestSpecVersionRoundTrip:

    def test_round_trip_through_save_and_load(self, root):
        job_id = _save_job(root, _TASKS)
        job = load_job_plan(job_id, root)
        _, entry = _by_planned(job, "T1")
        entry.spec_version = 5
        save_job_plan(job, root)

        reloaded = load_job_plan(job_id, root)
        assert _by_planned(reloaded, "T1")[1].spec_version == 5

    def test_record_with_no_spec_version_key_loads_at_one(self, root):
        job_id = _save_job(root, _TASKS)
        record = job_record_path(job_id, root)
        data = json.loads(record.read_text(encoding="utf-8"))
        for t in data["tasks"]:
            t.pop("spec_version", None)
        record.write_text(json.dumps(data), encoding="utf-8")

        reloaded = load_job_plan(job_id, root)
        for t in reloaded.tasks:
            assert t.spec_version == 1
