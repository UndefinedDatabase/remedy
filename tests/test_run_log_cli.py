"""
CLI-level run log tests for apps/cli/main.py.

Tests cover:
  - plan-job-local writes planning_started and planning_completed
  - plan-job-local noop writes planning_completed with outcome=noop
  - run-next-task-local no-pending writes task_run_noop
  - run-next-task-local success writes task_run_started, builder_started,
    builder_completed, workspace_materialized, verification_passed,
    task_run_completed
  - verification failure writes verification_failed and task_run_failed
  - repo permission denied writes repo_application_skipped with reason
  - patch intent created writes patch_intent_created with count and risks

All tests are deterministic — no live Ollama. REMEDY_DATA_DIR is injected
via monkeypatch so tests write to tmp_path.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.run_log import read_run_events
from packages.orchestration.storage import load_job, save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_and_save_job(tmp_path, monkeypatch, **metadata_overrides) -> Job:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = Job(name="test", state=RunState.PENDING)
    job.metadata.update(metadata_overrides)
    save_job(job)
    return job


def _find_run_log(tmp_path, job_id) -> Path | None:
    """Find the first .jsonl file for a given job_id under tmp_path/runs/."""
    runs_dir = tmp_path / "runs" / str(job_id)
    if not runs_dir.exists():
        return None
    files = list(runs_dir.glob("*.jsonl"))
    return files[0] if files else None


def _run_events_for_job(tmp_path, job_id) -> list[dict]:
    log_path = _find_run_log(tmp_path, job_id)
    if log_path is None:
        return []
    return read_run_events(log_path)


def _event_names(events: list[dict]) -> list[str]:
    return [e["event"] for e in events]


# ---------------------------------------------------------------------------
# plan-job-local run log
# ---------------------------------------------------------------------------


class TestPlanJobLocalRunLog:
    """plan-job-local writes planning events to the run log."""

    def _make_mock_planner(self, *, model="test-model", changed=True, task_count=2):
        """Return (mock_planner_cls, mock_planner_instance, mock_plan_job_with_llm)."""
        from packages.orchestration.job_runner import PlanJobResult

        job_holder: list[Job] = []

        def fake_plan_job_with_llm(job, _call_planner):
            if changed:
                from packages.core.models import Task

                for i in range(task_count):
                    task = Task(description=f"task {i}", inputs={"task_type": f"type_{i}"})
                    job.tasks.append(task)
            return PlanJobResult(job=job, changed=changed)

        planner_instance = MagicMock()
        planner_instance.model = model
        planner_instance.plan = MagicMock()

        planner_cls = MagicMock(return_value=planner_instance)
        return planner_cls, planner_instance, fake_plan_job_with_llm

    def test_writes_planning_started(self, tmp_path, monkeypatch):
        job = _make_and_save_job(tmp_path, monkeypatch)
        planner_cls, planner_instance, fake_plan = self._make_mock_planner(changed=True)

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner",
                planner_cls,
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=fake_plan,
            ),
            patch("packages.orchestration.llm_planner.annotate_planning_result"),
        ):
            from apps.cli.main import _cmd_plan_job_local

            _cmd_plan_job_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert any(e["event"] == "planning_started" for e in events)

    def test_writes_planning_completed_on_success(self, tmp_path, monkeypatch):
        job = _make_and_save_job(tmp_path, monkeypatch)
        planner_cls, planner_instance, fake_plan = self._make_mock_planner(changed=True)

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner",
                planner_cls,
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=fake_plan,
            ),
            patch("packages.orchestration.llm_planner.annotate_planning_result"),
        ):
            from apps.cli.main import _cmd_plan_job_local

            _cmd_plan_job_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert any(e["event"] == "planning_completed" for e in events)

    def test_planning_completed_outcome_changed(self, tmp_path, monkeypatch):
        job = _make_and_save_job(tmp_path, monkeypatch)
        planner_cls, planner_instance, fake_plan = self._make_mock_planner(changed=True)

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner",
                planner_cls,
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=fake_plan,
            ),
            patch("packages.orchestration.llm_planner.annotate_planning_result"),
        ):
            from apps.cli.main import _cmd_plan_job_local

            _cmd_plan_job_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        completed = next(e for e in events if e["event"] == "planning_completed")
        assert completed["outcome"] == "changed"

    def test_planning_completed_noop_outcome(self, tmp_path, monkeypatch):
        """Already-planned job: planning_completed with outcome=noop."""
        job = _make_and_save_job(tmp_path, monkeypatch)
        planner_cls, planner_instance, fake_plan = self._make_mock_planner(changed=False)

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner",
                planner_cls,
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=fake_plan,
            ),
            patch("packages.orchestration.llm_planner.annotate_planning_result"),
        ):
            from apps.cli.main import _cmd_plan_job_local

            _cmd_plan_job_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        completed = next(e for e in events if e["event"] == "planning_completed")
        assert completed["outcome"] == "noop"

    def test_planning_started_includes_provider_role_model(self, tmp_path, monkeypatch):
        job = _make_and_save_job(tmp_path, monkeypatch)
        planner_cls, planner_instance, fake_plan = self._make_mock_planner(
            changed=True, model="qwen3"
        )

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner",
                planner_cls,
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=fake_plan,
            ),
            patch("packages.orchestration.llm_planner.annotate_planning_result"),
        ):
            from apps.cli.main import _cmd_plan_job_local

            _cmd_plan_job_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        started = next(e for e in events if e["event"] == "planning_started")
        assert started["provider"] == "ollama"
        assert started["role"] == "planner"
        assert started["model"] == "qwen3"

    def test_plan_job_local_output_includes_log_path(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        planner_cls, planner_instance, fake_plan = self._make_mock_planner(changed=True)

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner",
                planner_cls,
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=fake_plan,
            ),
            patch("packages.orchestration.llm_planner.annotate_planning_result"),
        ):
            from apps.cli.main import _cmd_plan_job_local

            _cmd_plan_job_local(str(job.id))

        out = capsys.readouterr().out
        assert "log=" in out


# ---------------------------------------------------------------------------
# run-next-task-local run log — no pending tasks
# ---------------------------------------------------------------------------


class TestRunNextTaskLocalNoop:
    def test_noop_writes_task_run_noop(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        from apps.cli.main import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert any(e["event"] == "task_run_noop" for e in events)

    def test_noop_outcome_is_no_pending_tasks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        from apps.cli.main import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        noop = next(e for e in events if e["event"] == "task_run_noop")
        assert noop["outcome"] == "no_pending_tasks"

    def test_noop_output_includes_log_path(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        from apps.cli.main import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))

        out = capsys.readouterr().out
        assert "log=" in out


# ---------------------------------------------------------------------------
# run-next-task-local run log — full success path
# ---------------------------------------------------------------------------


def _build_success_mocks(tmp_path, job: Job, task: Task):
    """Build a complete set of mock objects for a successful run-next-task-local call."""
    from packages.orchestration.task_runner import RunTaskResult
    from packages.orchestration.verifier import VerificationResult
    from packages.orchestration.workspace import MaterializedFile

    artifact = Artifact(
        name=f"task_output_{task.inputs.get('task_type', 'unknown')}",
        content=(
            "Summary:\n  Quick summary.\n\nProposed Changes:\n"
            "  - Change A\n  - Change B\n\nNotes:\n  - None\n"
        ),
        mime_type="text/plain",
        task_id=task.id,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        metadata={"task_type": task.inputs.get("task_type", "unknown"), "summary": "done"},
    )
    task.output_artifact_ids.append(artifact.id)
    job.artifacts.append(artifact)

    ws_file = tmp_path / "fake_ws.txt"
    ws_file.write_text("  - Change A\n  - Change B\n")
    artifact.metadata["workspace_file"] = str(ws_file)
    task.status = RunState.RUNNING

    run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
    vr = VerificationResult(task_id=task.id, passed=True, checks=[])
    fake_mf = MaterializedFile(path=ws_file, content="  - Change A\n", size=14)

    def fake_finalize(r, v):
        for t in r.job.tasks:
            if t.id == r.task_id:
                t.status = RunState.COMPLETED

    return run_result, vr, fake_mf, fake_finalize


class TestRunNextTaskLocalSuccess:
    """Full success path: all expected run log events are written."""

    def _run_success(self, tmp_path, monkeypatch, task_type="write_readme"):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        job = Job(name="test", state=RunState.RUNNING)
        task = Task(description="write readme", inputs={"task_type": task_type})
        job.tasks.append(task)
        save_job(job)

        run_result, vr, fake_mf, fake_finalize = _build_success_mocks(tmp_path, job, task)

        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder",
                builder_cls,
            ),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                return_value=run_result,
            ),
            patch("packages.orchestration.task_runner.annotate_task_result"),
            patch(
                "packages.orchestration.task_runner.materialize_task_output",
                return_value=fake_mf,
            ),
            patch(
                "packages.orchestration.verifier.verify_task_output",
                return_value=vr,
            ),
            patch(
                "packages.orchestration.task_runner.finalize_task",
                side_effect=fake_finalize,
            ),
        ):
            from apps.cli.main import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        return job, _run_events_for_job(tmp_path, job.id)

    def test_writes_task_run_started(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        assert "task_run_started" in _event_names(events)

    def test_writes_builder_started(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        assert "builder_started" in _event_names(events)

    def test_writes_builder_completed(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        assert "builder_completed" in _event_names(events)

    def test_writes_workspace_materialized(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        assert "workspace_materialized" in _event_names(events)

    def test_writes_verification_passed(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        assert "verification_passed" in _event_names(events)

    def test_writes_task_run_completed(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        assert "task_run_completed" in _event_names(events)

    def test_builder_started_has_provider_role_model(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "builder_started")
        assert ev["provider"] == "ollama"
        assert ev["role"] == "builder"
        assert ev["model"] == "test-model"

    def test_workspace_materialized_has_workspace_file(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "workspace_materialized")
        assert "workspace_file" in ev["metadata"]

    def test_verification_passed_has_verifier_profile(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "verification_passed")
        assert "verifier_profile" in ev["metadata"]

    def test_task_run_completed_outcome_is_pass(self, tmp_path, monkeypatch):
        _, events = self._run_success(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "task_run_completed")
        assert ev["outcome"] == "pass"

    def test_success_output_includes_log_path(self, tmp_path, monkeypatch, capsys):
        self._run_success(tmp_path, monkeypatch)
        out = capsys.readouterr().out
        assert "log=" in out


# ---------------------------------------------------------------------------
# run-next-task-local — verification failure
# ---------------------------------------------------------------------------


class TestRunNextTaskVerificationFailure:
    def _run_verification_failure(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        job = Job(name="test", state=RunState.RUNNING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        job.tasks.append(task)
        save_job(job)

        artifact = Artifact(
            name="task_output_write_readme",
            content="Missing sections",
            mime_type="text/plain",
            task_id=task.id,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={"task_type": "write_readme", "summary": "done"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.artifacts.append(artifact)
        task.status = RunState.RUNNING

        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationCheckResult, VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
        vr = VerificationResult(
            task_id=task.id,
            passed=False,
            checks=[
                VerificationCheckResult(
                    check="required_section:Summary:",
                    passed=False,
                    message="missing section",
                )
            ],
        )
        ws_file = tmp_path / "ws.txt"
        ws_file.write_text("content")
        fake_mf = MaterializedFile(path=ws_file, content="content", size=7)

        def fake_finalize(r, v):
            for t in r.job.tasks:
                if t.id == r.task_id:
                    t.status = RunState.PENDING

        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder",
                builder_cls,
            ),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                return_value=run_result,
            ),
            patch("packages.orchestration.task_runner.annotate_task_result"),
            patch(
                "packages.orchestration.task_runner.materialize_task_output",
                return_value=fake_mf,
            ),
            patch(
                "packages.orchestration.verifier.verify_task_output",
                return_value=vr,
            ),
            patch(
                "packages.orchestration.task_runner.finalize_task",
                side_effect=fake_finalize,
            ),
        ):
            from apps.cli.main import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        return _run_events_for_job(tmp_path, job.id)

    def test_writes_verification_failed(self, tmp_path, monkeypatch):
        events = self._run_verification_failure(tmp_path, monkeypatch)
        assert "verification_failed" in _event_names(events)

    def test_writes_task_run_failed(self, tmp_path, monkeypatch):
        events = self._run_verification_failure(tmp_path, monkeypatch)
        assert "task_run_failed" in _event_names(events)

    def test_verification_failed_has_failure_count(self, tmp_path, monkeypatch):
        events = self._run_verification_failure(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "verification_failed")
        assert ev["metadata"]["failure_count"] == 1

    def test_verification_failed_has_failed_checks(self, tmp_path, monkeypatch):
        events = self._run_verification_failure(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "verification_failed")
        assert "required_section:Summary:" in ev["metadata"]["failed_checks"]

    def test_task_run_failed_outcome_is_fail(self, tmp_path, monkeypatch):
        events = self._run_verification_failure(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["outcome"] == "fail"


# ---------------------------------------------------------------------------
# run-next-task-local — repo permission denied
# ---------------------------------------------------------------------------


class TestRunNextTaskRepoPermissionDenied:
    def test_repo_permission_denied_writes_repo_application_skipped(
        self, tmp_path, monkeypatch
    ):
        """When repo_generated_write is denied, log repo_application_skipped."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()

        job = Job(name="test", state=RunState.RUNNING)
        job.metadata["target_repo"] = str(repo_dir)
        set_permission(job, Capability.repo_generated_write, allow=False)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        job.tasks.append(task)
        save_job(job)

        artifact = Artifact(
            name="task_output_write_readme",
            content=(
                "Summary:\n  Quick summary.\n\nProposed Changes:\n"
                "  - Change A\n  - Change B\n\nNotes:\n  - None\n"
            ),
            mime_type="text/plain",
            task_id=task.id,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={"task_type": "write_readme", "summary": "done"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.artifacts.append(artifact)

        ws_file = tmp_path / "fake_ws.txt"
        ws_file.write_text("  - Change A\n")
        artifact.metadata["workspace_file"] = str(ws_file)
        task.status = RunState.RUNNING

        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
        vr = VerificationResult(task_id=task.id, passed=True, checks=[])
        fake_mf = MaterializedFile(path=ws_file, content="  - Change A\n", size=14)

        def fake_finalize(r, v):
            for t in r.job.tasks:
                if t.id == r.task_id:
                    t.status = RunState.COMPLETED

        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder",
                builder_cls,
            ),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                return_value=run_result,
            ),
            patch("packages.orchestration.task_runner.annotate_task_result"),
            patch(
                "packages.orchestration.task_runner.materialize_task_output",
                return_value=fake_mf,
            ),
            patch(
                "packages.orchestration.verifier.verify_task_output",
                return_value=vr,
            ),
            patch(
                "packages.orchestration.task_runner.finalize_task",
                side_effect=fake_finalize,
            ),
        ):
            from apps.cli.main import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        skipped = next(
            (e for e in events if e["event"] == "repo_application_skipped"), None
        )
        assert skipped is not None, f"Expected repo_application_skipped, got: {_event_names(events)}"
        assert skipped["metadata"]["reason"] == "permission_denied"


# ---------------------------------------------------------------------------
# run-next-task-local — patch intent created
# ---------------------------------------------------------------------------


class TestRunNextTaskPatchIntentCreated:
    def test_patch_intent_created_writes_event_with_count_and_risks(
        self, tmp_path, monkeypatch
    ):
        """Patch intent creation logs patch_intent_created with count and risk_levels."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        job = Job(name="test", state=RunState.RUNNING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        job.tasks.append(task)
        save_job(job)

        artifact = Artifact(
            name="task_output_write_readme",
            content=(
                "Summary:\n  Quick summary.\n\nProposed Changes:\n"
                "  - Change A\n  - Change B\n\nNotes:\n  - None\n"
            ),
            mime_type="text/plain",
            task_id=task.id,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={"task_type": "write_readme", "summary": "done"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.artifacts.append(artifact)

        ws_file = tmp_path / "fake_ws.txt"
        ws_file.write_text("  - Change A\n  - Change B\n")
        artifact.metadata["workspace_file"] = str(ws_file)
        task.status = RunState.RUNNING

        from packages.orchestration.patch_intent import (
            PatchIntent,
            PatchIntentSet,
        )
        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
        vr = VerificationResult(task_id=task.id, passed=True, checks=[])
        fake_mf = MaterializedFile(path=ws_file, content="  - Change A\n", size=14)

        fake_pis = PatchIntentSet(
            task_id=task.id,
            artifact_id=artifact.id,
            intents=[
                PatchIntent(
                    target_path="README.md",
                    intent="Add installation section",
                )
            ],
        )
        fake_pi_mf = MaterializedFile(
            path=tmp_path / "pi.json", content="{}", size=2
        )

        def fake_finalize(r, v):
            for t in r.job.tasks:
                if t.id == r.task_id:
                    t.status = RunState.COMPLETED

        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder",
                builder_cls,
            ),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                return_value=run_result,
            ),
            patch("packages.orchestration.task_runner.annotate_task_result"),
            patch(
                "packages.orchestration.task_runner.materialize_task_output",
                return_value=fake_mf,
            ),
            patch(
                "packages.orchestration.verifier.verify_task_output",
                return_value=vr,
            ),
            patch(
                "packages.orchestration.task_runner.finalize_task",
                side_effect=fake_finalize,
            ),
            patch(
                "packages.orchestration.patch_intent.derive_patch_intents",
                return_value=fake_pis,
            ),
            patch(
                "packages.orchestration.patch_intent.verify_patch_intent_set",
                return_value=[],
            ),
            patch(
                "packages.orchestration.patch_intent.materialize_patch_intents",
                return_value=fake_pi_mf,
            ),
            patch(
                "packages.orchestration.patch_intent.generate_dry_run_preview",
                return_value=[],
            ),
        ):
            from apps.cli.main import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        created = next(
            (e for e in events if e["event"] == "patch_intent_created"), None
        )
        assert created is not None, f"Expected patch_intent_created, got: {_event_names(events)}"
        assert created["metadata"]["intent_count"] == 1
        assert "risk_levels" in created["metadata"]
