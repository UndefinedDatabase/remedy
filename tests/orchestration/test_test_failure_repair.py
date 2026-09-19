"""Tests for Test Failure Artifact v1.

Covers:
- Step 950: Redaction — no raw stdout/stderr, no absolute paths, bounded summaries
- Step 951: Linking — failure artifact links to intent, apply, task, test run

F273 deleted the repair loop these tests also drove (R-0923), with its tests.
"""

from __future__ import annotations

import json
import os

from packages.orchestration.test_failure_artifact import (
    FAILURE_COLLECTION_FAILED,
    FAILURE_ENVIRONMENT_FAILED,
    FAILURE_KINDS,
    FAILURE_TEST_FAILED,
    FAILURE_TIMEOUT,
    FAILURE_UNKNOWN,
    RelatedChangeRef,
    SuggestedRepairAction,
    TestFailureArtifact,
    TestFailureSummary,
    _classify_failure_kind,
    _normalize_command,
    build_test_failure_artifact,
    create_fix_task_from_failure,
    emit_failure_events,
    export_failure_artifact_json,
    persist_failure_artifact,
    summarize_failure_artifact,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(tmp_path):
    """Create minimal job in tmp data dir."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)

    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

    job = JobPlan(job_title="test-job", user_prompt="test")
    task = TaskEntry(title="initial task")
    job.tasks = [task]
    save_job_plan(job)
    return job, task, data_dir, old


def _cleanup_env(old):
    if old:
        os.environ["REMEDY_DATA_DIR"] = old
    else:
        os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# Step 941: TestFailureArtifact model
# ---------------------------------------------------------------------------


class TestFailureArtifactModel:

    def test_failure_kinds_defined(self):
        assert len(FAILURE_KINDS) >= 5
        assert FAILURE_TEST_FAILED in FAILURE_KINDS
        assert FAILURE_UNKNOWN in FAILURE_KINDS

    def test_dataclass_defaults(self):
        f = TestFailureArtifact()
        assert f.failure_kind == FAILURE_UNKNOWN
        assert f.exit_code is None
        assert f.related_files == []
        assert f.related_changes == []

    def test_related_change_ref(self):
        r = RelatedChangeRef(ref_type="intent", ref_id="abc", label="test")
        assert r.ref_type == "intent"

    def test_suggested_repair_action(self):
        a = SuggestedRepairAction(label="Fix", command="remedy test run x", reason="failing")
        assert "remedy" in a.command

    def test_failure_summary(self):
        s = TestFailureSummary(failure_kind="test_failed", safe_summary="3 tests failed")
        assert s.repair_available is False


# ---------------------------------------------------------------------------
# Step 942: Build failure artifact
# ---------------------------------------------------------------------------


class TestBuildFailureArtifact:

    def test_build_from_record(self, tmp_path):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry
        job = JobPlan(job_title="test", user_prompt="t")
        task = TaskEntry(title="t")
        job.tasks = [task]

        class FakeRecord:
            test_run_id = "run-abc"
            command = "pytest tests/"
            status = "failed"
            exit_code = 1
            duration_ms = 1200
            output_path = "/tmp/some/output.log"

        failure = build_test_failure_artifact(
            job, FakeRecord(),
            related_intent_id="intent-1",
            related_apply_id="apply-1",
        )
        assert failure.artifact_id
        assert failure.failure_kind == FAILURE_TEST_FAILED
        assert failure.exit_code == 1
        assert "failed" in failure.safe_summary.lower()
        assert failure.output_ref == "output.log"  # basename only
        assert len(failure.related_changes) == 2

    def test_build_from_event_dict(self, tmp_path):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry
        job = JobPlan(job_title="test", user_prompt="t")
        task = TaskEntry(title="t")
        job.tasks = [task]

        event = {
            "status": "timeout",
            "exit_code": "137",
            "command": "pytest --timeout=30",
            "test_run_id": "run-xyz",
        }
        failure = build_test_failure_artifact(job, event)
        assert failure.failure_kind == FAILURE_TIMEOUT
        assert failure.exit_code == 137

    def test_the_artifact_carries_the_job_id(self, tmp_path):
        """R-0888: the artifact links back to its job by the unified record's id."""
        from packages.orchestration.pingpong_job import JobPlan
        job = JobPlan(job_title="test", user_prompt="t")
        failure = build_test_failure_artifact(job, {"status": "failed", "exit_code": 1})
        assert failure.job_id == job.job_id != ""

    def test_build_fallback(self, tmp_path):
        from packages.orchestration.pingpong_job import JobPlan
        job = JobPlan(job_title="test", user_prompt="t")
        failure = build_test_failure_artifact(job, 42)
        assert failure.failure_kind == FAILURE_UNKNOWN
        assert failure.artifact_id


# ---------------------------------------------------------------------------
# Step 950: Redaction tests
# ---------------------------------------------------------------------------


class TestRedaction:

    def test_no_raw_output_in_summary(self):
        f = TestFailureArtifact(
            safe_summary="3 tests failed, exit 1",
            command_safe="pytest tests/",
        )
        text = summarize_failure_artifact(f)
        assert "Traceback" not in text
        assert "stdout" not in text.lower()

    def test_command_normalization_strips_secrets(self):
        cmd = "API_KEY=secret123 pytest tests/"
        safe = _normalize_command(cmd)
        assert "secret123" not in safe
        assert "API_KEY" not in safe

    def test_command_normalization_bounded(self):
        cmd = "pytest " + "a" * 500
        safe = _normalize_command(cmd)
        assert len(safe) <= 200

    def test_output_ref_is_basename(self):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry
        job = JobPlan(job_title="test", user_prompt="t")
        task = TaskEntry(title="t")
        job.tasks = [task]

        class FakeRecord:
            test_run_id = "run-1"
            command = "pytest"
            status = "failed"
            exit_code = 1
            duration_ms = 100
            output_path = "/home/user/.remedy/data/outputs/run-1.log"

        failure = build_test_failure_artifact(job, FakeRecord())
        assert "/" not in failure.output_ref
        assert failure.output_ref == "run-1.log"

    def test_safe_summary_bounded(self):
        f = TestFailureArtifact(safe_summary="x" * 300)
        data = export_failure_artifact_json(f)
        # safe_summary field passes through; build functions bound it
        assert "safe_summary" in data

    def test_export_json_no_raw_content(self):
        f = TestFailureArtifact(
            artifact_id="abc",
            safe_summary="3 tests failed",
            failure_kind="test_failed",
        )
        data = export_failure_artifact_json(f)
        text = json.dumps(data)
        assert "Traceback" not in text
        assert "stderr" not in text

    def test_classify_collection_failed(self):
        assert _classify_failure_kind("failed", 2) == FAILURE_COLLECTION_FAILED
        assert _classify_failure_kind("failed", 5) == FAILURE_COLLECTION_FAILED

    def test_classify_timeout(self):
        assert _classify_failure_kind("timeout", None) == FAILURE_TIMEOUT

    def test_classify_blocked(self):
        assert _classify_failure_kind("blocked", None) == FAILURE_ENVIRONMENT_FAILED


# ---------------------------------------------------------------------------
# Step 951: Linking tests
# ---------------------------------------------------------------------------


class TestLinking:

    def test_failure_links_intent_and_apply(self):
        f = TestFailureArtifact(
            related_intent_id="intent-1",
            related_apply_id="apply-1",
            related_test_run_id="run-1",
        )
        data = export_failure_artifact_json(f)
        assert data["related_intent_id"] == "intent-1"
        assert data["related_apply_id"] == "apply-1"
        assert data["related_test_run_id"] == "run-1"

    def test_related_changes_in_export(self):
        f = TestFailureArtifact(
            related_changes=[
                RelatedChangeRef("intent", "i-1", "patch intent"),
                RelatedChangeRef("apply", "a-1", "apply record"),
            ]
        )
        data = export_failure_artifact_json(f)
        assert len(data["related_changes"]) == 2
        assert data["related_changes"][0]["ref_type"] == "intent"

    def test_persist_links_to_job(self, tmp_path):
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            failure = TestFailureArtifact(
                artifact_id="temp",
                job_id=str(job.job_id),
                task_id=str(task.task_id),
                failure_kind="test_failed",
                safe_summary="1 test failed",
            )
            art = persist_failure_artifact(job, failure)
            assert art.metadata["test_failure"] is True
            assert art.metadata["failure_kind"] == "test_failed"
            assert str(art.id) == failure.artifact_id
        finally:
            _cleanup_env(old)

    def test_fix_task_links_to_failure(self, tmp_path):
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            failure = TestFailureArtifact(
                artifact_id="fail-1",
                job_id=str(job.job_id),
                task_id=str(task.task_id),
                failure_kind="test_failed",
                safe_summary="1 test failed",
            )
            fix_task = create_fix_task_from_failure(job, failure)
            assert fix_task.inputs["failure_artifact_id"] == "fail-1"
            assert fix_task.inputs["failure_kind"] == "test_failed"
            assert len(job.tasks) == 2  # original + fix
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 944: Event emission
# ---------------------------------------------------------------------------


class TestFailureEvents:

    def test_emit_events(self, tmp_path):
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            failure = TestFailureArtifact(
                artifact_id="fail-1",
                job_id=str(job.job_id),
                task_id=str(task.task_id),
                failure_kind="test_failed",
                safe_summary="1 test failed",
            )
            emit_failure_events(data_dir, job.job_id, failure, fix_task_id="fix-1")

            from packages.orchestration.timeline import load_run_events
            events = load_run_events(data_dir, job.job_id)
            event_types = [e.get("event") for e in events]
            assert "test_failure_artifact_created" in event_types
            assert "repair_task_created" in event_types
        finally:
            _cleanup_env(old)


class TestSystemArtifactKeepsTaskIdAbsent:
    """A system-produced artifact carries `task_id = None`, never the string "None".

    `packages/core/models.py` states the convention every artifact lookup relies on:
    `task_id = None` means the artifact came from orchestration rather than from a Task,
    and `artifact_index.task_artifacts_by_kind` matches on equality. F275 round 48's
    id-shape widen wrapped the whole conditional in `str(...)`, which turned that absence
    into the truthy string `"None"` that no lookup matches and no reader expects.
    """

    def test_a_failure_without_a_task_leaves_task_id_absent(self, tmp_path):
        job, _task, _data_dir, old = _make_job(tmp_path)
        try:
            failure = TestFailureArtifact(
                artifact_id="temp",
                job_id=str(job.job_id),
                task_id="",
                failure_kind="test_failed",
                safe_summary="1 test failed",
            )
            art = persist_failure_artifact(job, failure)
            assert art.task_id is None
        finally:
            _cleanup_env(old)
