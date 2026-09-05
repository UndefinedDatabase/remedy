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
from packages.orchestration.storage import save_job

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

        # Mirrors plan_job_with_llm's real signature (llm_planner.py:105): F115
        # added the keyword-only on_prompt_composed hook, and a double that drops
        # it turns the CLI call into a TypeError that job.py swallows as exit 1.
        def fake_plan_job_with_llm(job, _call_planner, *, on_prompt_composed=None):
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
            from apps.cli.commands.job import _cmd_plan_job_local

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
            from apps.cli.commands.job import _cmd_plan_job_local

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
            from apps.cli.commands.job import _cmd_plan_job_local

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
            from apps.cli.commands.job import _cmd_plan_job_local

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
            from apps.cli.commands.job import _cmd_plan_job_local

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
            from apps.cli.commands.job import _cmd_plan_job_local

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

        from apps.cli.commands.job import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert any(e["event"] == "task_run_noop" for e in events)

    def test_noop_outcome_is_no_pending_tasks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        from apps.cli.commands.job import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        noop = next(e for e in events if e["event"] == "task_run_noop")
        assert noop["outcome"] == "no_pending_tasks"

    def test_noop_output_includes_log_path(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        from apps.cli.commands.job import _cmd_run_next_task_local

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
            from apps.cli.commands.job import _cmd_run_next_task_local

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
            from apps.cli.commands.job import _cmd_run_next_task_local

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
            from apps.cli.commands.job import _cmd_run_next_task_local

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
            from apps.cli.commands.job import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        created = next(
            (e for e in events if e["event"] == "patch_intent_created"), None
        )
        assert created is not None, f"Expected patch_intent_created, got: {_event_names(events)}"
        assert created["metadata"]["intent_count"] == 1
        assert "risk_levels" in created["metadata"]

    def test_patch_intent_created_writes_created_at_on_explanation(
        self, tmp_path, monkeypatch
    ):
        """Patch intent explanations carry a created_at timestamp (F262 T002)."""
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
            PatchDryRunResult,
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
        fake_dry_run = [
            PatchDryRunResult(
                target_path="README.md",
                action="modify",
                risk_level="medium",
                reason="task type 'write_readme'",
                summary="Add installation section",
                diff_preview="--- README.md",
            )
        ]

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
                return_value=fake_dry_run,
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        from packages.orchestration.storage import load_job

        reloaded = load_job(job.id)
        explanations = reloaded.artifacts[0].metadata["patch_intent_explanations"]
        assert explanations[0]["created_at"]


# ---------------------------------------------------------------------------
# Terminal-event invariant — workspace_write denial
# ---------------------------------------------------------------------------


class TestRunNextTaskWorkspaceWriteDenialTerminal:
    """workspace_write denial must emit task_run_started then task_run_failed."""

    def _run_denied(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from packages.orchestration.permissions import Capability, set_permission

        job = Job(name="test", state=RunState.RUNNING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        job.tasks.append(task)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)

        from apps.cli.commands.job import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))

        return _run_events_for_job(tmp_path, job.id)

    def test_task_run_started_is_logged(self, tmp_path, monkeypatch):
        events = self._run_denied(tmp_path, monkeypatch)
        assert "task_run_started" in _event_names(events)

    def test_task_run_failed_is_logged(self, tmp_path, monkeypatch):
        events = self._run_denied(tmp_path, monkeypatch)
        assert "task_run_failed" in _event_names(events)

    def test_task_run_failed_outcome_is_permission_denied(self, tmp_path, monkeypatch):
        events = self._run_denied(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["outcome"] == "permission_denied"

    def test_task_run_failed_metadata_has_capability(self, tmp_path, monkeypatch):
        events = self._run_denied(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["metadata"].get("capability") == "workspace_write"

    def test_task_run_started_precedes_task_run_failed(self, tmp_path, monkeypatch):
        events = self._run_denied(tmp_path, monkeypatch)
        names = _event_names(events)
        assert names.index("task_run_started") < names.index("task_run_failed")

    def test_no_orphaned_started_without_terminal(self, tmp_path, monkeypatch):
        """task_run_started must be closed by exactly one terminal event."""
        events = self._run_denied(tmp_path, monkeypatch)
        names = _event_names(events)
        terminal = {"task_run_completed", "task_run_failed", "task_run_noop"}
        started_count = names.count("task_run_started")
        terminal_count = sum(names.count(t) for t in terminal)
        assert started_count == terminal_count == 1


# ---------------------------------------------------------------------------
# Terminal-event invariant — builder exception paths
# ---------------------------------------------------------------------------


def _make_task_job(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = Job(name="test", state=RunState.RUNNING)
    task = Task(description="write readme", inputs={"task_type": "write_readme"})
    job.tasks.append(task)
    save_job(job)
    return job, task


class TestRunNextTaskImportErrorTerminal:
    def test_import_error_logs_task_run_failed(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_cls = MagicMock(side_effect=ImportError("no module"))

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert "task_run_failed" in _event_names(events)

    def test_import_error_outcome_is_missing_dependency(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_cls = MagicMock(side_effect=ImportError("no module"))

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["outcome"] == "missing_dependency"

    def test_import_error_raw_text_absent_from_log(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        secret_msg = "secret-import-path abc123"
        builder_cls = MagicMock(side_effect=ImportError(secret_msg))

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        log_path = _find_run_log(tmp_path, job.id)
        assert log_path is not None
        assert secret_msg not in log_path.read_text(encoding="utf-8")

    def test_structural_invariant_import_error_started_before_failed(self, tmp_path, monkeypatch):
        """task_run_started count == 1, terminal count == 1, and ordering is correct."""
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_cls = MagicMock(side_effect=ImportError("no module"))

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        names = _event_names(events)
        terminal = {"task_run_completed", "task_run_failed", "task_run_noop"}
        assert names.count("task_run_started") == 1
        assert sum(names.count(t) for t in terminal) == 1
        assert names.index("task_run_started") < names.index("task_run_failed")


def _make_validation_error():
    """Create a real pydantic.ValidationError for use in tests."""
    from pydantic import ValidationError

    from packages.orchestration.builder_models import BuilderOutput

    with pytest.raises(ValidationError) as exc_info:
        # summary is required; proposed_changes min_length=1 is also violated
        BuilderOutput(summary="x", proposed_changes=[])
    return exc_info.value


class TestRunNextTaskValidationErrorTerminal:
    def test_validation_error_logs_task_run_failed(self, tmp_path, monkeypatch):
        real_exc = _make_validation_error()
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=real_exc,
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert "task_run_failed" in _event_names(events)

    def test_validation_error_outcome_is_invalid_builder_output(self, tmp_path, monkeypatch):
        real_exc = _make_validation_error()
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=real_exc,
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["outcome"] == "invalid_builder_output"

    def test_validation_error_raw_text_absent_from_log(self, tmp_path, monkeypatch):
        """ValidationError path must not write raw exception text to the JSONL log."""
        # Use a real ValidationError so the except ValidationError branch is exercised.
        real_exc = _make_validation_error()
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch("packages.orchestration.task_runner.run_next_task", side_effect=real_exc),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        log_path = _find_run_log(tmp_path, job.id)
        assert log_path is not None
        raw = log_path.read_text(encoding="utf-8")
        # The log must record error_category, not the full pydantic error text
        assert "ValidationError" in raw  # error_category value is safe
        assert "proposed_changes" not in raw  # field names from pydantic error body are not safe

    def test_structural_invariant_validation_error_started_before_failed(self, tmp_path, monkeypatch):
        real_exc = _make_validation_error()
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch("packages.orchestration.task_runner.run_next_task", side_effect=real_exc),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        names = _event_names(_run_events_for_job(tmp_path, job.id))
        terminal = {"task_run_completed", "task_run_failed", "task_run_noop"}
        assert names.count("task_run_started") == 1
        assert sum(names.count(t) for t in terminal) == 1
        assert names.index("task_run_started") < names.index("task_run_failed")


class TestRunNextTaskValueErrorTerminal:
    def test_value_error_logs_task_run_failed(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=ValueError("bad config"),
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert "task_run_failed" in _event_names(events)

    def test_value_error_outcome_is_configuration_error(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=ValueError("bad config"),
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["outcome"] == "configuration_error"

    def test_structural_invariant_value_error_started_before_failed(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch("packages.orchestration.task_runner.run_next_task",
                  side_effect=ValueError("bad config")),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        names = _event_names(_run_events_for_job(tmp_path, job.id))
        terminal = {"task_run_completed", "task_run_failed", "task_run_noop"}
        assert names.count("task_run_started") == 1
        assert sum(names.count(t) for t in terminal) == 1
        assert names.index("task_run_started") < names.index("task_run_failed")


class TestRunNextTaskGenericExceptionTerminal:
    def test_generic_exception_logs_task_run_failed(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=RuntimeError("something exploded"),
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        assert "task_run_failed" in _event_names(events)

    def test_generic_exception_outcome_is_builder_error(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=RuntimeError("something exploded"),
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["outcome"] == "builder_error"

    def test_generic_exception_error_category_in_metadata(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=RuntimeError("something exploded"),
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        events = _run_events_for_job(tmp_path, job.id)
        ev = next(e for e in events if e["event"] == "task_run_failed")
        assert ev["metadata"].get("error_category") == "RuntimeError"

    def test_raw_exception_text_absent_from_log(self, tmp_path, monkeypatch):
        secret_msg = "secret-token xyzzy99"
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                side_effect=RuntimeError(secret_msg),
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        log_path = _find_run_log(tmp_path, job.id)
        assert log_path is not None
        assert secret_msg not in log_path.read_text(encoding="utf-8")

    def test_structural_invariant_generic_exception_started_before_failed(self, tmp_path, monkeypatch):
        job, _ = _make_task_job(tmp_path, monkeypatch)
        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch("packages.orchestration.task_runner.run_next_task",
                  side_effect=RuntimeError("boom")),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            with pytest.raises(SystemExit):
                _cmd_run_next_task_local(str(job.id))

        names = _event_names(_run_events_for_job(tmp_path, job.id))
        terminal = {"task_run_completed", "task_run_failed", "task_run_noop"}
        assert names.count("task_run_started") == 1
        assert sum(names.count(t) for t in terminal) == 1
        assert names.index("task_run_started") < names.index("task_run_failed")


# ---------------------------------------------------------------------------
# Terminal-event invariant — result.changed=False (builder no-change)
# ---------------------------------------------------------------------------


class TestRunNextTaskBuilderNoChange:
    def _run_no_change(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        job = Job(name="test", state=RunState.RUNNING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        job.tasks.append(task)
        save_job(job)

        from packages.orchestration.task_runner import RunTaskResult

        run_result = RunTaskResult(job=job, task_id=task.id, changed=False)

        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch("packages.providers.ollama_builder.provider.OllamaBuilder", builder_cls),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                return_value=run_result,
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        return _run_events_for_job(tmp_path, job.id)

    def test_logs_task_run_noop(self, tmp_path, monkeypatch):
        events = self._run_no_change(tmp_path, monkeypatch)
        assert "task_run_noop" in _event_names(events)

    def test_task_run_noop_outcome_is_no_change(self, tmp_path, monkeypatch):
        events = self._run_no_change(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "task_run_noop")
        assert ev["outcome"] == "no_change"

    def test_task_run_noop_reason_is_builder_returned_no_change(self, tmp_path, monkeypatch):
        events = self._run_no_change(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "task_run_noop")
        assert ev["metadata"].get("reason") == "builder_returned_no_change"

    def test_no_orphaned_started_without_terminal(self, tmp_path, monkeypatch):
        events = self._run_no_change(tmp_path, monkeypatch)
        names = _event_names(events)
        terminal = {"task_run_completed", "task_run_failed", "task_run_noop"}
        started_count = names.count("task_run_started")
        terminal_count = sum(names.count(t) for t in terminal)
        assert started_count == terminal_count == 1

    def test_cli_output_says_builder_returned_no_change(
        self, tmp_path, monkeypatch, capsys
    ):
        self._run_no_change(tmp_path, monkeypatch)
        out = capsys.readouterr().out
        assert "builder returned no change" in out

    def test_cli_output_does_not_say_no_pending_tasks(
        self, tmp_path, monkeypatch, capsys
    ):
        self._run_no_change(tmp_path, monkeypatch)
        out = capsys.readouterr().out
        assert "no pending tasks" not in out.lower()


# ---------------------------------------------------------------------------
# planning_failed — redaction
# ---------------------------------------------------------------------------


class TestPlanJobLocalPlanningFailed:
    def _run_planning_failed(self, tmp_path, monkeypatch, exc_to_raise=None):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        if exc_to_raise is None:
            exc_to_raise = RuntimeError("secret-token abc123")

        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        planner_instance = MagicMock()
        planner_instance.model = "test-model"
        planner_cls = MagicMock(return_value=planner_instance)

        with (
            patch(
                "packages.providers.ollama_planner.provider.OllamaPlanner", planner_cls
            ),
            patch(
                "packages.orchestration.llm_planner.plan_job_with_llm",
                side_effect=exc_to_raise,
            ),
        ):
            from apps.cli.commands.job import _cmd_plan_job_local

            with pytest.raises(SystemExit):
                _cmd_plan_job_local(str(job.id))

        return _run_events_for_job(tmp_path, job.id)

    def test_planning_failed_event_written(self, tmp_path, monkeypatch):
        events = self._run_planning_failed(tmp_path, monkeypatch)
        assert "planning_failed" in _event_names(events)

    def test_planning_failed_outcome_is_error(self, tmp_path, monkeypatch):
        events = self._run_planning_failed(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "planning_failed")
        assert ev["outcome"] == "error"

    def test_planning_failed_message_is_fixed_safe_text(self, tmp_path, monkeypatch):
        events = self._run_planning_failed(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "planning_failed")
        assert ev.get("message") == "planning failed"

    def test_planning_failed_metadata_has_error_category(self, tmp_path, monkeypatch):
        events = self._run_planning_failed(tmp_path, monkeypatch)
        ev = next(e for e in events if e["event"] == "planning_failed")
        assert ev["metadata"].get("error_category") == "RuntimeError"

    def test_raw_exception_text_absent_from_log(self, tmp_path, monkeypatch):
        secret_msg = "secret-token abc123"
        events = self._run_planning_failed(
            tmp_path, monkeypatch, exc_to_raise=RuntimeError(secret_msg)
        )
        log_path = _find_run_log(tmp_path, next(e["job_id"] for e in events))
        raw = log_path.read_text(encoding="utf-8")
        assert secret_msg not in raw

    def test_planning_started_precedes_planning_failed(self, tmp_path, monkeypatch):
        events = self._run_planning_failed(tmp_path, monkeypatch)
        names = _event_names(events)
        assert names.index("planning_started") < names.index("planning_failed")
