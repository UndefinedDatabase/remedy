"""Tests for Test Failure Artifact v1 + Repair Loop v0.

Covers:
- Step 950: Redaction — no raw stdout/stderr, no absolute paths, bounded summaries
- Step 951: Linking — failure artifact links to intent, apply, task, test run
- Step 952: Repair loop v0 — phased result, stop reasons, next safe actions
- Step 953: Runtime CLI — repair.start and repair.failure-show in catalog
- Step 949: Integration — failure_summary field in DoRunResult
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

    from packages.core.models import Job, Task
    from packages.orchestration.storage import save_job

    job = Job(name="test-job", user_prompt="test")
    task = Task(description="initial task")
    job.tasks = [task]
    save_job(job)
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
        from packages.core.models import Job, Task
        job = Job(name="test", user_prompt="t")
        task = Task(description="t")
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
        from packages.core.models import Job, Task
        job = Job(name="test", user_prompt="t")
        task = Task(description="t")
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

    def test_build_fallback(self, tmp_path):
        from packages.core.models import Job
        job = Job(name="test", user_prompt="t")
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
        from packages.core.models import Job, Task
        job = Job(name="test", user_prompt="t")
        task = Task(description="t")
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
                job_id=str(job.id),
                task_id=str(task.id),
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
                job_id=str(job.id),
                task_id=str(task.id),
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
                job_id=str(job.id),
                task_id=str(task.id),
                failure_kind="test_failed",
                safe_summary="1 test failed",
            )
            emit_failure_events(data_dir, job.id, failure, fix_task_id="fix-1")

            from packages.orchestration.timeline import load_run_events
            events = load_run_events(data_dir, job.id)
            event_types = [e.get("event") for e in events]
            assert "test_failure_artifact_created" in event_types
            assert "repair_task_created" in event_types
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 952: Repair loop v0 tests
# ---------------------------------------------------------------------------


class TestRepairLoopV0:

    def _setup_failure(self, tmp_path):
        """Create job with persisted failure artifact."""
        job, task, data_dir, old = _make_job(tmp_path)
        failure = TestFailureArtifact(
            artifact_id="temp",
            job_id=str(job.id),
            task_id=str(task.id),
            failure_kind="test_failed",
            safe_summary="3 tests failed",
        )
        art = persist_failure_artifact(job, failure)
        return job, str(art.id), data_dir, old

    def test_repair_loop_creates_fix_task(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id)
            assert result.fix_task_id
            assert result.stop_reason == "fix_task_created"
        finally:
            _cleanup_env(old)

    def test_repair_loop_phases(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id)
            phase_names = [p["phase"] for p in result.phases]
            assert "load" in phase_names
            assert "validate" in phase_names
            assert "fix_task" in phase_names
            assert "stop" in phase_names
        finally:
            _cleanup_env(old)

    def test_repair_loop_next_safe_action(self, tmp_path):
        from packages.orchestration.do_run import validate_next_safe_action_command
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id)
            assert result.next_safe_action is not None
            assert validate_next_safe_action_command(result.next_safe_action.command)
        finally:
            _cleanup_env(old)

    def test_repair_loop_with_patch_intent(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            assert result.repair_artifact_id
            assert result.repair_patch_intent_id
            assert result.stop_reason == "approval_required"
        finally:
            _cleanup_env(old)

    def test_repair_loop_idempotent_fix_task(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            r1 = start_repair_loop_v0(str(job.id), fail_art_id)
            r2 = start_repair_loop_v0(str(job.id), fail_art_id)
            assert r1.fix_task_id == r2.fix_task_id
        finally:
            _cleanup_env(old)

    def test_repair_loop_job_not_found(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            result = start_repair_loop_v0("00000000-0000-0000-0000-000000000000", "fake")
            assert result.stop_reason == "job_not_found"
            assert result.error
        finally:
            _cleanup_env(old)

    def test_repair_loop_failure_not_found(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), "nonexistent-id")
            assert result.stop_reason == "failure_artifact_not_found"
        finally:
            _cleanup_env(old)

    def test_export_json(self, tmp_path):
        from packages.orchestration.repair_loop import (
            export_repair_loop_json,
            start_repair_loop_v0,
        )
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id)
            data = export_repair_loop_json(result)
            assert data["version"] == 1
            assert data["job_id"] == str(job.id)
            assert data["fix_task_id"]
            assert data["next_safe_action"] is not None
            text = json.dumps(data)
            assert "Traceback" not in text
        finally:
            _cleanup_env(old)

    def test_summarize(self, tmp_path):
        from packages.orchestration.repair_loop import (
            start_repair_loop_v0,
            summarize_repair_loop,
        )
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id)
            text = summarize_repair_loop(result)
            assert "Repair Loop" in text
            assert "Fix task" in text
            assert "Stop:" in text
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 953: Runtime CLI catalog tests
# ---------------------------------------------------------------------------


class TestRepairCatalog:

    def test_repair_group_exists(self):
        from apps.cli.command_catalog import GROUPS
        assert "repair" in GROUPS

    def test_repair_start_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("repair.start")
        assert cmd.action_class == "write_metadata"
        assert cmd.supports_json is True
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False

    def test_repair_failure_show_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("repair.failure-show")
        assert cmd.action_class == "read_only"
        assert cmd.supports_json is True

    def test_repair_handlers_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "repair.start" in handlers
        assert "repair.failure-show" in handlers

    def test_validate_repair_start_command(self):
        from packages.orchestration.do_run import validate_next_safe_action_command
        assert validate_next_safe_action_command(
            "remedy repair start job123 fail456 --json"
        ) is True

    def test_validate_repair_failure_show_command(self):
        from packages.orchestration.do_run import validate_next_safe_action_command
        assert validate_next_safe_action_command(
            "remedy repair failure-show job123 fail456 --json"
        ) is True


# ---------------------------------------------------------------------------
# Step 949: DoRunResult integration
# ---------------------------------------------------------------------------


class TestDoRunIntegration:

    def test_failure_summary_field_exists(self):
        from packages.orchestration.do_run import DoRunResult
        result = DoRunResult()
        assert result.failure_summary is None

    def test_failure_summary_in_export(self):
        from packages.orchestration.do_run import DoRunResult, export_do_run_json
        result = DoRunResult(
            failure_summary={
                "failure_kind": "test_failed",
                "safe_summary": "3 tests failed",
                "fix_task_id": "fix-1",
                "repair_available": True,
            }
        )
        data = export_do_run_json(result)
        assert "failure_summary" in data
        assert data["failure_summary"]["failure_kind"] == "test_failed"

    def test_no_failure_summary_when_none(self):
        from packages.orchestration.do_run import DoRunResult, export_do_run_json
        result = DoRunResult()
        data = export_do_run_json(result)
        assert "failure_summary" not in data


# ---------------------------------------------------------------------------
# Step 961: Regression test for fake repair intent (must pass after fix)
# ---------------------------------------------------------------------------


class TestRepairIntentTruth:
    """Repair patch intent must be real — visible via approval queue."""

    def _setup_failure(self, tmp_path):
        job, task, data_dir, old = _make_job(tmp_path)
        failure = TestFailureArtifact(
            artifact_id="temp",
            job_id=str(job.id),
            task_id=str(task.id),
            failure_kind="test_failed",
            safe_summary="3 tests failed",
        )
        art = persist_failure_artifact(job, failure)
        return job, str(art.id), data_dir, old

    def test_repair_intent_visible_in_approval_queue(self, tmp_path):
        """repair_patch_intent_id must be findable via get_patch_intent."""
        from packages.orchestration.approval_queue import get_patch_intent
        from packages.orchestration.repair_loop import start_repair_loop_v0
        from packages.orchestration.storage import load_job

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            assert result.repair_patch_intent_id, "Should have repair_patch_intent_id"

            reloaded = load_job(str(job.id))
            intent = get_patch_intent(reloaded, result.repair_patch_intent_id)
            assert intent is not None, (
                f"get_patch_intent returned None for {result.repair_patch_intent_id}"
            )
        finally:
            _cleanup_env(old)

    def test_repair_intent_in_list(self, tmp_path):
        """repair_patch_intent_id must appear in list_patch_intents."""
        from packages.orchestration.approval_queue import list_patch_intents
        from packages.orchestration.repair_loop import start_repair_loop_v0
        from packages.orchestration.storage import load_job

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            reloaded = load_job(str(job.id))
            intents = list_patch_intents(reloaded)
            intent_ids = [i["intent_id"] for i in intents]
            assert result.repair_patch_intent_id in intent_ids
        finally:
            _cleanup_env(old)

    def test_repair_intent_next_action_points_to_real_intent(self, tmp_path):
        """next_safe_action must reference intent that actually exists."""
        from packages.orchestration.approval_queue import get_patch_intent
        from packages.orchestration.do_run import validate_next_safe_action_command
        from packages.orchestration.repair_loop import start_repair_loop_v0
        from packages.orchestration.storage import load_job

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            assert result.next_safe_action is not None
            assert validate_next_safe_action_command(result.next_safe_action.command)
            # Command references intent_id that exists
            assert result.repair_patch_intent_id in result.next_safe_action.command
            reloaded = load_job(str(job.id))
            assert get_patch_intent(reloaded, result.repair_patch_intent_id) is not None
        finally:
            _cleanup_env(old)

    def test_repair_intent_approval_state_pending(self, tmp_path):
        """Repair intent should be in pending state."""
        from packages.orchestration.approval_queue import get_patch_intent
        from packages.orchestration.repair_loop import start_repair_loop_v0
        from packages.orchestration.storage import load_job

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            reloaded = load_job(str(job.id))
            intent = get_patch_intent(reloaded, result.repair_patch_intent_id)
            assert intent["state"] == "pending"
        finally:
            _cleanup_env(old)

    def test_repair_intent_has_safe_metadata(self, tmp_path):
        """Repair intent metadata must have safe fields, no raw output."""
        from packages.orchestration.approval_queue import get_patch_intent
        from packages.orchestration.repair_loop import start_repair_loop_v0
        from packages.orchestration.storage import load_job

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            reloaded = load_job(str(job.id))
            intent = get_patch_intent(reloaded, result.repair_patch_intent_id)
            assert intent["target_path"]
            assert intent["action"]
            assert intent["risk"]
            assert intent["summary"]
            text = json.dumps(intent)
            assert "Traceback" not in text
            assert "stderr" not in text
        finally:
            _cleanup_env(old)

    def test_no_fake_intent_without_create_flag(self, tmp_path):
        """Without create_patch_intent, no intent ID should be set."""
        from packages.orchestration.repair_loop import start_repair_loop_v0

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=False)
            assert result.repair_patch_intent_id == ""
            assert result.stop_reason == "fix_task_created"
        finally:
            _cleanup_env(old)

    def test_related_files_safe(self, tmp_path):
        """related_files must be safe relative paths."""
        f = TestFailureArtifact(
            related_files=["tests/test_example.py", "src/main.py"],
        )
        for path in f.related_files:
            assert not path.startswith("/")
            assert ".." not in path

    def test_event_idempotency(self, tmp_path):
        """Repeated repair_loop_v0 should not duplicate failure creation events."""
        from packages.orchestration.repair_loop import start_repair_loop_v0
        from packages.orchestration.timeline import load_run_events

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            start_repair_loop_v0(str(job.id), fail_art_id)
            start_repair_loop_v0(str(job.id), fail_art_id)
            events = load_run_events(data_dir, job.id)
            creation_events = [e for e in events if e.get("event") == "test_failure_artifact_created"]
            assert len(creation_events) == 1, f"Expected 1 creation event, got {len(creation_events)}"
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 968: Runtime CLI tests for optional intent
# ---------------------------------------------------------------------------


class TestRepairCLIHandlers:
    """CLI handler integration tests (no subprocess, calls handler directly)."""

    def _setup_failure(self, tmp_path):
        job, task, data_dir, old = _make_job(tmp_path)
        failure = TestFailureArtifact(
            artifact_id="temp",
            job_id=str(job.id),
            task_id=str(task.id),
            failure_kind="test_failed",
            safe_summary="2 tests failed",
        )
        art = persist_failure_artifact(job, failure)
        return job, str(art.id), data_dir, old

    def test_repair_start_handler_no_intent(self, tmp_path, capsys):
        from apps.cli.commands.repair_cmd import _cmd_repair_start

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            ns = type("NS", (), {
                "job_id": str(job.id),
                "failure_artifact_id": fail_art_id,
                "fixture_patch_intent": "false",
                "json": False,
            })()
            _cmd_repair_start(ns)
            out = capsys.readouterr().out
            assert "Repair Loop" in out
            assert "fix_task_created" in out
        finally:
            _cleanup_env(old)

    def test_repair_start_handler_with_intent(self, tmp_path, capsys):
        from apps.cli.commands.repair_cmd import _cmd_repair_start

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            ns = type("NS", (), {
                "job_id": str(job.id),
                "failure_artifact_id": fail_art_id,
                "fixture_patch_intent": "true",
                "json": False,
            })()
            _cmd_repair_start(ns)
            out = capsys.readouterr().out
            assert "approval_required" in out
            assert "Approve repair patch" in out
        finally:
            _cleanup_env(old)

    def test_repair_start_handler_json_output(self, tmp_path, capsys):
        from apps.cli.commands.repair_cmd import _cmd_repair_start

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            ns = type("NS", (), {
                "job_id": str(job.id),
                "failure_artifact_id": fail_art_id,
                "fixture_patch_intent": "true",
                "json": True,
            })()
            _cmd_repair_start(ns)
            out = capsys.readouterr().out
            data = json.loads(out)
            assert data["repair_patch_intent_id"]
            assert data["stop_reason"] == "approval_required"
            assert data["next_safe_action"] is not None
        finally:
            _cleanup_env(old)

    def test_failure_show_handler(self, tmp_path, capsys):
        from apps.cli.commands.repair_cmd import _cmd_failure_show

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            ns = type("NS", (), {
                "job_id": str(job.id),
                "failure_artifact_id": fail_art_id,
                "json": False,
            })()
            _cmd_failure_show(ns)
            out = capsys.readouterr().out
            assert "test_failed" in out
        finally:
            _cleanup_env(old)

    def test_failure_show_handler_json(self, tmp_path, capsys):
        from apps.cli.commands.repair_cmd import _cmd_failure_show

        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            ns = type("NS", (), {
                "job_id": str(job.id),
                "failure_artifact_id": fail_art_id,
                "json": True,
            })()
            _cmd_failure_show(ns)
            out = capsys.readouterr().out
            data = json.loads(out)
            assert data["failure_kind"] == "test_failed"
            text = json.dumps(data)
            assert "Traceback" not in text
        finally:
            _cleanup_env(old)

    def test_repair_start_job_not_found(self, tmp_path):
        from apps.cli.commands.repair_cmd import _cmd_repair_start

        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            ns = type("NS", (), {
                "job_id": "00000000-0000-0000-0000-000000000000",
                "failure_artifact_id": "fake",
                "fixture_patch_intent": "false",
                "json": False,
            })()
            # Handler should not raise — result has stop_reason=job_not_found
            _cmd_repair_start(ns)
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 969: Proof/change alignment
# ---------------------------------------------------------------------------


class TestProofAlignment:
    """proof_status must be incomplete when repair intent is pending."""

    def _setup_failure(self, tmp_path):
        job, task, data_dir, old = _make_job(tmp_path)
        failure = TestFailureArtifact(
            artifact_id="temp",
            job_id=str(job.id),
            task_id=str(task.id),
            failure_kind="test_failed",
            safe_summary="2 tests failed",
        )
        art = persist_failure_artifact(job, failure)
        return job, str(art.id), data_dir, old

    def test_proof_status_incomplete_with_intent(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            assert result.proof_status == "incomplete"
        finally:
            _cleanup_env(old)

    def test_proof_status_incomplete_without_intent(self, tmp_path):
        from packages.orchestration.repair_loop import start_repair_loop_v0
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=False)
            assert result.proof_status == "incomplete"
        finally:
            _cleanup_env(old)

    def test_proof_status_in_json_export(self, tmp_path):
        from packages.orchestration.repair_loop import (
            export_repair_loop_json,
            start_repair_loop_v0,
        )
        job, fail_art_id, data_dir, old = self._setup_failure(tmp_path)
        try:
            result = start_repair_loop_v0(str(job.id), fail_art_id, create_patch_intent=True)
            data = export_repair_loop_json(result)
            assert data["proof_status"] == "incomplete"
        finally:
            _cleanup_env(old)
