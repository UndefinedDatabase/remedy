"""
CLI-level tests for permission-related commands in apps/cli/main.py.

Tests cover:
  - set-permission: reserved capability notice printed to stdout
  - set-permission: no notice for active capabilities
  - show-permissions: displays all four capabilities
  - show-permissions: all capabilities labeled [active] or [reserved]
  - show-permissions: effective allow/deny is reflected correctly
  - workspace_write denial: exits non-zero before builder call, no state mutation
  - patch intent errors: recorded in metadata, warning emitted, no file written

All tests are deterministic — no live Ollama, no builder, no verifier.
A temporary REMEDY_DATA_DIR is injected via monkeypatch so tests do not
touch the real .data/ directory.
"""

from __future__ import annotations

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.permissions import Capability, set_permission
from packages.orchestration.storage import load_job, save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_and_save_job(tmp_path, monkeypatch, **metadata_overrides) -> Job:
    """Create a minimal job, persist it in a temp data dir, and return it."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = Job(name="test", state=RunState.PENDING)
    job.metadata.update(metadata_overrides)
    save_job(job)
    return job


# ---------------------------------------------------------------------------
# set-permission: reserved capability notice
# ---------------------------------------------------------------------------


class TestSetPermissionReservedNotice:
    def test_reserved_cap_prints_notice_on_allow(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "allow", "repo_overwrite")
        out = capsys.readouterr().out
        assert "reserved" in out
        assert "repo_overwrite" in out

    def test_reserved_cap_prints_notice_on_deny(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "deny", "shell_exec")
        out = capsys.readouterr().out
        assert "reserved" in out
        assert "shell_exec" in out

    def test_active_cap_no_reserved_notice(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "allow", "repo_generated_write")
        out = capsys.readouterr().out
        assert "reserved" not in out

    def test_workspace_write_no_reserved_notice(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission

        _cmd_set_permission(str(job.id), "deny", "workspace_write")
        out = capsys.readouterr().out
        assert "reserved" not in out

    def test_set_permission_still_persists_for_reserved_cap(self, tmp_path, monkeypatch):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_set_permission
        from packages.orchestration.storage import load_job

        _cmd_set_permission(str(job.id), "allow", "repo_overwrite")
        reloaded = load_job(job.id)
        assert reloaded.metadata["permissions"]["repo_overwrite"] == "allow"


# ---------------------------------------------------------------------------
# show-permissions
# ---------------------------------------------------------------------------


class TestShowPermissions:
    def test_shows_all_four_capabilities(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        assert "workspace_write" in out
        assert "repo_generated_write" in out
        assert "repo_overwrite" in out
        assert "shell_exec" in out

    def test_reserved_capabilities_are_labeled(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        assert "[reserved]" in out

    def test_active_capabilities_are_labeled(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        assert "[active]" in out

    def test_workspace_write_line_has_active_label(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "workspace_write" in l]
        assert any("[active]" in l for l in lines)

    def test_repo_overwrite_line_has_reserved_label(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "repo_overwrite" in l]
        assert any("[reserved]" in l for l in lines)

    def test_default_workspace_write_shows_allow(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        # workspace_write is allowed by default
        lines = [l for l in out.splitlines() if "workspace_write" in l]
        assert any("allow" in l for l in lines)

    def test_explicit_allow_reflected(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        set_permission(job, Capability.repo_generated_write, allow=True)
        save_job(job)

        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "repo_generated_write" in l]
        assert any("allow" in l for l in lines)

    def test_explicit_deny_reflected(self, tmp_path, monkeypatch, capsys):
        job = _make_and_save_job(tmp_path, monkeypatch)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)

        from apps.cli.main import _cmd_show_permissions

        _cmd_show_permissions(str(job.id))
        out = capsys.readouterr().out
        lines = [l for l in out.splitlines() if "workspace_write" in l]
        assert any("deny" in l for l in lines)


# ---------------------------------------------------------------------------
# workspace_write denial: pre-builder enforcement (Step 9.6)
# ---------------------------------------------------------------------------


class TestWorkspaceWriteDenialPreBuilder:
    """workspace_write denial must stop execution before the builder is called.

    These tests verify the early guard in _cmd_run_next_task_local:
    - exits non-zero immediately
    - prints a clear error to stderr naming the denied permission
    - does not mutate task state (no RUNNING tasks)
    - does not create artifacts
    - does not save any modified job state
    """

    def _setup_denied_job(self, tmp_path, monkeypatch) -> Job:
        job = _make_and_save_job(tmp_path, monkeypatch)
        # Add a pending task so the scenario is meaningful
        task = Task(description="test task", inputs={"task_type": "test"})
        job.tasks.append(task)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)
        return job

    def test_denied_exits_nonzero(self, tmp_path, monkeypatch):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit) as exc_info:
            _cmd_run_next_task_local(str(job.id))
        assert exc_info.value.code == 1

    def test_denied_prints_error_to_stderr(self, tmp_path, monkeypatch, capsys):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))
        err = capsys.readouterr().err
        assert "workspace_write" in err
        assert "permission" in err.lower()

    def test_denied_does_not_mutate_task_state(self, tmp_path, monkeypatch):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))
        reloaded = load_job(job.id)
        # No task should have transitioned to RUNNING (builder was never called)
        assert all(t.status == RunState.PENDING for t in reloaded.tasks)

    def test_denied_does_not_create_artifacts(self, tmp_path, monkeypatch):
        job = self._setup_denied_job(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_run_next_task_local

        with pytest.raises(SystemExit):
            _cmd_run_next_task_local(str(job.id))
        reloaded = load_job(job.id)
        assert len(reloaded.artifacts) == 0


# ---------------------------------------------------------------------------
# no-pending-tasks behavior with workspace_write denied (Step 10 fix)
# ---------------------------------------------------------------------------


class TestNoPendingTasksWithPermissionDenied:
    """No-pending-tasks must exit 0 cleanly regardless of workspace_write status."""

    def test_no_tasks_workspace_write_denied_exits_zero(self, tmp_path, monkeypatch, capsys):
        """A job with no tasks and workspace_write=deny should exit 0, not 1."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)

        from apps.cli.main import _cmd_run_next_task_local

        # Should return normally (no SystemExit) even with workspace_write denied
        _cmd_run_next_task_local(str(job.id))
        out = capsys.readouterr().out
        assert "no pending tasks" in out

    def test_no_tasks_workspace_write_denied_prints_no_pending(
        self, tmp_path, monkeypatch, capsys
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        set_permission(job, Capability.workspace_write, allow=False)
        save_job(job)

        from apps.cli.main import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))
        out = capsys.readouterr().out
        assert str(job.id) in out

    def test_no_tasks_workspace_write_allowed_exits_normally(
        self, tmp_path, monkeypatch, capsys
    ):
        """Baseline: no tasks, workspace_write allowed → same clean exit."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = Job(name="test", state=RunState.PENDING)
        save_job(job)

        from apps.cli.main import _cmd_run_next_task_local

        _cmd_run_next_task_local(str(job.id))
        out = capsys.readouterr().out
        assert "no pending tasks" in out


# ---------------------------------------------------------------------------
# CLI-level patch intent error coverage (Step 10.6)
# ---------------------------------------------------------------------------


class TestPatchIntentErrorsCLI:
    """_cmd_run_next_task_local correctly handles verify_patch_intent_set returning errors.

    Uses mocks/stubs for Ollama and the orchestration layer so no live services
    are required.  Verifies:
      - patch_intent_errors is persisted in the saved artifact metadata
      - patch_intent_file is NOT present in the saved artifact metadata
      - task completion is governed by the task verifier (vr.passed=True)
      - a warning is emitted to stderr
    """

    def test_patch_intent_errors_recorded_in_saved_metadata(
        self, tmp_path, monkeypatch, capsys
    ):
        from pathlib import Path
        from unittest.mock import MagicMock, patch

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from packages.core.models import Artifact
        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        # Build a job with one pending task and a pre-built artifact.
        job = Job(name="test-pi-cli", state=RunState.PENDING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        artifact = Artifact(
            name="task_output_write_readme",
            content="Proposed Changes:\n  - Update readme",
            mime_type="text/plain",
            task_id=task.id,
            metadata={"task_type": "write_readme", "summary": "Update readme"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.tasks.append(task)
        job.artifacts.append(artifact)
        save_job(job)  # saved with task in PENDING status

        # Simulate run_next_task having run the task (task now RUNNING).
        task.status = RunState.RUNNING
        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
        vr = VerificationResult(task_id=task.id, passed=True)
        fake_mf = MaterializedFile(
            path=Path(tmp_path) / "fake_workspace.txt",
            content="x",
            size=1,
        )

        def fake_finalize(r, v):
            for t in r.job.tasks:
                if t.id == r.task_id:
                    t.status = RunState.COMPLETED

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder"
            ) as MockBuilder,
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
                "packages.orchestration.patch_intent.verify_patch_intent_set",
                return_value=["intent[0].target_path: absolute paths are not allowed"],
            ),
        ):
            instance = MagicMock()
            instance.model = "test-model"
            instance.build = MagicMock()
            MockBuilder.return_value = instance

            from apps.cli.main import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        # Verify saved metadata.
        reloaded = load_job(job.id)
        saved_artifact = next(
            (a for a in reloaded.artifacts if str(a.task_id) == str(task.id)), None
        )
        assert saved_artifact is not None, "Artifact not found in saved job"
        assert "patch_intent_errors" in saved_artifact.metadata
        assert len(saved_artifact.metadata["patch_intent_errors"]) > 0
        assert "patch_intent_file" not in saved_artifact.metadata

        # Verify stderr warning.
        err = capsys.readouterr().err
        assert "warning" in err.lower()
        assert "patch intent" in err.lower()

    def test_patch_intent_skipped_on_verifier_failure(self, tmp_path, monkeypatch):
        """When task verification fails, the entire patch intent block is skipped.

        The `if vr.passed:` guard in the CLI must prevent any patch intent
        function from being called and must leave the artifact metadata free of
        all patch intent keys.

        Uses the real finalize_task so task lifecycle is also verified:
        on failure the task must roll back to PENDING (safe to retry).
        """
        from pathlib import Path
        from unittest.mock import MagicMock, patch

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from packages.core.models import Artifact
        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationCheckResult, VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        job = Job(name="test-pi-verifier-fail", state=RunState.PENDING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        artifact = Artifact(
            name="task_output_write_readme",
            content="Proposed Changes:\n  - Update readme",
            mime_type="text/plain",
            task_id=task.id,
            metadata={"task_type": "write_readme", "summary": "Update readme"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.tasks.append(task)
        job.artifacts.append(artifact)
        save_job(job)  # saved with task in PENDING status

        task.status = RunState.RUNNING
        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)

        # Verifier fails — patch intent block must not be entered at all.
        vr = VerificationResult(
            task_id=task.id,
            passed=False,
            checks=[
                VerificationCheckResult(
                    check="has_artifact", passed=False, message="no artifact"
                )
            ],
        )
        fake_mf = MaterializedFile(
            path=Path(tmp_path) / "fake_workspace.txt",
            content="x",
            size=1,
        )

        mock_derive = MagicMock(name="derive_patch_intents")
        mock_verify_pi = MagicMock(name="verify_patch_intent_set")

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder"
            ) as MockBuilder,
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
            # finalize_task is NOT mocked — the real implementation runs so that
            # the task lifecycle (RUNNING → PENDING on failure) is also verified.
            patch("packages.orchestration.patch_intent.derive_patch_intents", mock_derive),
            patch(
                "packages.orchestration.patch_intent.verify_patch_intent_set", mock_verify_pi
            ),
        ):
            instance = MagicMock()
            instance.model = "test-model"
            instance.build = MagicMock()
            MockBuilder.return_value = instance

            from apps.cli.main import _cmd_run_next_task_local

            # CLI exits non-zero on verifier failure — expected behavior.
            with pytest.raises(SystemExit) as exc_info:
                _cmd_run_next_task_local(str(job.id))
            assert exc_info.value.code == 1

        # Patch intent functions must never have been invoked.
        mock_derive.assert_not_called()
        mock_verify_pi.assert_not_called()

        # Reload and inspect the persisted state.
        reloaded = load_job(job.id)

        # Task lifecycle: real finalize_task must have rolled back to PENDING and
        # cleared output_artifact_ids (safe-to-retry state for the next cycle).
        reloaded_task = next(t for t in reloaded.tasks if t.id == task.id)
        assert reloaded_task.status == RunState.PENDING
        assert reloaded_task.output_artifact_ids == []

        # No patch intent keys in the persisted artifact metadata.
        # The artifact is kept in job.artifacts for diagnostics even after
        # finalize_task clears task.output_artifact_ids, so search by task_id.
        saved_artifact = next(
            (a for a in reloaded.artifacts if str(a.task_id) == str(task.id)), None
        )
        assert saved_artifact is not None, "Artifact not found in saved job"
        assert "patch_intent_file" not in saved_artifact.metadata
        assert "patch_intent_count" not in saved_artifact.metadata
        assert "patch_intent_errors" not in saved_artifact.metadata


# ---------------------------------------------------------------------------
# CLI-level risk coverage (Step 12.5)
# ---------------------------------------------------------------------------


class TestPatchIntentRisksCLI:
    """Four focused tests for the patch_intent_risks CLI contract.

    Each test exercises exactly one contract:
      1. patch_intent_risks key exists in saved artifact metadata
      2. stored risk list length equals the intent count (one intent → one risk)
      3. all stored risk values are members of RISK_LEVELS
      4. CLI stdout contains the exact risk value (RISK_UNKNOWN, no repo attached)

    All patch-intent functions (derive, verify, generate_dry_run, format) run
    naturally — no mocks — so the risk contract is exercised end-to-end.
    """

    def _run_risk_scenario(self, tmp_path, monkeypatch, capsys):
        """Run the CLI risk happy path; return (saved_artifact, stdout_text).

        Sets up a job with one write_readme task, mocks the Ollama/runner/verifier
        layer, lets all patch-intent logic run naturally, and returns the reloaded
        artifact and captured stdout for the caller to assert against.
        """
        from pathlib import Path
        from unittest.mock import MagicMock, patch

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        from packages.core.models import Artifact
        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        job = Job(name="test-risk-cli", state=RunState.PENDING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        artifact = Artifact(
            name="task_output_write_readme",
            content="Proposed Changes:\n  - Update readme\n  - Add installation",
            mime_type="text/plain",
            task_id=task.id,
            metadata={"task_type": "write_readme", "summary": "Update readme"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.tasks.append(task)
        job.artifacts.append(artifact)
        save_job(job)

        task.status = RunState.RUNNING
        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
        vr = VerificationResult(task_id=task.id, passed=True)
        fake_mf = MaterializedFile(
            path=Path(tmp_path) / "fake_workspace.txt",
            content="x",
            size=1,
        )

        def fake_finalize(r, v):
            for t in r.job.tasks:
                if t.id == r.task_id:
                    t.status = RunState.COMPLETED

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder"
            ) as MockBuilder,
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
            # derive_patch_intents, verify_patch_intent_set, generate_dry_run_preview,
            # and format_dry_run_explanations all run naturally — no mocks.
        ):
            instance = MagicMock()
            instance.model = "test-model"
            instance.build = MagicMock()
            MockBuilder.return_value = instance

            from apps.cli.main import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        reloaded = load_job(job.id)
        saved_artifact = next(
            (a for a in reloaded.artifacts if str(a.task_id) == str(task.id)), None
        )
        out = capsys.readouterr().out
        return saved_artifact, out

    def test_patch_intent_risks_key_stored_in_metadata(
        self, tmp_path, monkeypatch, capsys
    ):
        """patch_intent_risks key must be present in the saved artifact metadata."""
        saved_artifact, _ = self._run_risk_scenario(tmp_path, monkeypatch, capsys)
        assert saved_artifact is not None, "Artifact not found in saved job"
        assert "patch_intent_risks" in saved_artifact.metadata

    def test_stored_risk_count_matches_intent_count(
        self, tmp_path, monkeypatch, capsys
    ):
        """patch_intent_risks length must equal the number of intents (one here)."""
        saved_artifact, _ = self._run_risk_scenario(tmp_path, monkeypatch, capsys)
        assert saved_artifact is not None, "Artifact not found in saved job"
        stored_risks = saved_artifact.metadata["patch_intent_risks"]
        assert isinstance(stored_risks, list)
        assert len(stored_risks) == 1  # one intent → one risk level

    def test_all_stored_risk_values_are_in_risk_levels(
        self, tmp_path, monkeypatch, capsys
    ):
        """All values in patch_intent_risks must be members of RISK_LEVELS."""
        # Public risk contract constant — RISK_LEVELS is part of patch_intent's public API.
        from packages.orchestration.patch_intent import RISK_LEVELS

        saved_artifact, _ = self._run_risk_scenario(tmp_path, monkeypatch, capsys)
        assert saved_artifact is not None, "Artifact not found in saved job"
        stored_risks = saved_artifact.metadata["patch_intent_risks"]
        assert isinstance(stored_risks, list)
        assert all(r in RISK_LEVELS for r in stored_risks)

    def test_cli_output_contains_exact_risk_value(
        self, tmp_path, monkeypatch, capsys
    ):
        """CLI stdout must contain the exact RISK_UNKNOWN risk line.

        No target_repo is attached, so action == "preview-only" and
        classify_risk("preview-only") returns RISK_UNKNOWN.
        """
        # Public risk contract constant — RISK_UNKNOWN is part of patch_intent's public API.
        from packages.orchestration.patch_intent import RISK_UNKNOWN

        _, out = self._run_risk_scenario(tmp_path, monkeypatch, capsys)
        assert f"risk   : {RISK_UNKNOWN}" in out


# ---------------------------------------------------------------------------
# Project Registry CLI (Step 28 / 28.1)
# ---------------------------------------------------------------------------


class TestProjectCommandsCLI:
    """CLI-level tests for project management commands."""

    def _env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    def test_create_project_prints_uuid(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_project
        import uuid
        _cmd_create_project("MyApp", None)
        out = capsys.readouterr().out.strip()
        uuid.UUID(out)  # must be parseable

    def test_project_alias_json_version_1(self, tmp_path, monkeypatch, capsys):
        import json
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_project, _cmd_show_project
        _cmd_create_project("AliasTest", None)
        project_id = capsys.readouterr().out.strip()
        _cmd_show_project(project_id, json_output=True)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert d["version"] == 1

    def test_show_project_json_version_1(self, tmp_path, monkeypatch, capsys):
        import json
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_project, _cmd_show_project
        _cmd_create_project("ShowTest", None)
        project_id = capsys.readouterr().out.strip()
        _cmd_show_project(project_id, json_output=True)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert d["version"] == 1

    def test_show_project_missing_exits_1(self, tmp_path, monkeypatch):
        import pytest
        from uuid import uuid4
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_project
        with pytest.raises(SystemExit) as exc:
            _cmd_show_project(str(uuid4()), json_output=False)
        assert exc.value.code == 1

    def test_show_project_missing_stderr_safe(self, tmp_path, monkeypatch, capsys):
        import pytest
        from uuid import uuid4
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_show_project
        with pytest.raises(SystemExit):
            _cmd_show_project(str(uuid4()), json_output=False)
        err = capsys.readouterr().err
        assert "traceback" not in err.lower()
        assert "project not found" in err.lower() or "error" in err.lower()

    def test_attach_project_repo_idempotent_message(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_attach_project_repo, _cmd_create_project
        _cmd_create_project("RepoTest", None)
        project_id = capsys.readouterr().out.strip()
        repo = str(tmp_path / "myrepo")
        import os; os.makedirs(repo)
        _cmd_attach_project_repo(project_id, repo)
        capsys.readouterr()
        _cmd_attach_project_repo(project_id, repo)
        out = capsys.readouterr().out
        assert "no-op" in out

    def test_attach_project_job_sets_metadata(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_attach_project_job, _cmd_create_job, _cmd_create_project
        from packages.orchestration.storage import load_job
        from uuid import UUID
        _cmd_create_project("JobLink", None)
        project_id = capsys.readouterr().out.strip()
        _cmd_create_job("test prompt")
        job_id = capsys.readouterr().out.strip()
        _cmd_attach_project_job(project_id, job_id)
        capsys.readouterr()
        job = load_job(UUID(job_id))
        assert job.metadata.get("project_id") == project_id

    def test_create_job_with_valid_project_links(self, tmp_path, monkeypatch, capsys):
        import json
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_job, _cmd_create_project, _cmd_show_project
        _cmd_create_project("Linked", None)
        project_id = capsys.readouterr().out.strip()
        _cmd_create_job("linked prompt", project_id=project_id)
        job_id = capsys.readouterr().out.strip()
        _cmd_show_project(project_id, json_output=True)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert any(j["id"] == job_id for j in d["jobs"])

    def test_create_job_with_missing_project_warns(self, tmp_path, monkeypatch, capsys):
        from uuid import uuid4
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_job
        _cmd_create_job("warn prompt", project_id=str(uuid4()))
        out = capsys.readouterr()
        assert "warning" in out.err.lower()
        assert "traceback" not in out.err.lower()

    def test_create_job_missing_project_does_not_set_metadata(self, tmp_path, monkeypatch, capsys):
        from uuid import UUID, uuid4
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_job
        from packages.orchestration.storage import load_job
        _cmd_create_job("no-link prompt", project_id=str(uuid4()))
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert "project_id" not in job.metadata

    def test_malformed_project_id_no_placeholder_in_brain(self, tmp_path, monkeypatch, capsys):
        import json
        self._env(tmp_path, monkeypatch)
        from packages.core.models import Job, RunState
        from packages.orchestration.project_brain import build_project_brain, export_project_brain_json
        from packages.orchestration.storage import save_job
        job = Job(name="bad-project", state=RunState.PENDING, metadata={"project_id": "not-a-uuid"})
        save_job(job)
        graph = build_project_brain(job, [])
        d = export_project_brain_json(graph)
        types = {n["type"] for n in d["nodes"]}
        assert "project_placeholder" not in types


class TestCreateJobTaskType:
    """Tests for create-job --task-type / --task-description (Step 30.12)."""

    def _env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    # ------------------------------------------------------------------
    # Happy-path: --task-type creates one task and sets state PLANNED
    # ------------------------------------------------------------------

    def test_task_type_creates_one_task(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.orchestration.storage import load_job
        _cmd_create_job("smoke prompt", task_type="write_readme")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert len(job.tasks) == 1

    def test_task_type_sets_state_planned(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.core.models import RunState
        from packages.orchestration.storage import load_job
        _cmd_create_job("smoke prompt", task_type="write_readme")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert job.state == RunState.PLANNED

    def test_task_type_stored_in_task_inputs(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.orchestration.storage import load_job
        _cmd_create_job("prompt", task_type="analyze_code")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert job.tasks[0].inputs.get("task_type") == "analyze_code"

    def test_task_description_stored_in_task(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.orchestration.storage import load_job
        _cmd_create_job("prompt", task_type="write_readme", task_description="Custom desc.")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert job.tasks[0].description == "Custom desc."

    def test_default_description_when_none_given(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.orchestration.storage import load_job
        _cmd_create_job("prompt", task_type="write_readme")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert "write_readme" in job.tasks[0].description

    def test_no_task_type_leaves_state_pending(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.core.models import RunState
        from packages.orchestration.storage import load_job
        _cmd_create_job("plain prompt")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert job.state == RunState.PENDING
        assert len(job.tasks) == 0

    def test_hyphens_and_underscores_allowed_in_task_type(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job
        from packages.orchestration.storage import load_job
        _cmd_create_job("prompt", task_type="analyze-code_v2")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert job.tasks[0].inputs.get("task_type") == "analyze-code_v2"

    # ------------------------------------------------------------------
    # Error cases
    # ------------------------------------------------------------------

    def test_empty_task_type_exits_1(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_job
        with pytest.raises(SystemExit) as exc_info:
            _cmd_create_job("prompt", task_type="   ")
        assert exc_info.value.code == 1
        assert "empty" in capsys.readouterr().err.lower()

    def test_invalid_chars_in_task_type_exits_1(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_job
        with pytest.raises(SystemExit) as exc_info:
            _cmd_create_job("prompt", task_type="bad type!")
        assert exc_info.value.code == 1
        err = capsys.readouterr().err
        assert "invalid characters" in err.lower()

    def test_task_description_without_task_type_exits_1(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.main import _cmd_create_job
        with pytest.raises(SystemExit) as exc_info:
            _cmd_create_job("prompt", task_description="some desc")
        assert exc_info.value.code == 1
        assert "--task-type" in capsys.readouterr().err

    def test_combined_project_and_task_type(self, tmp_path, monkeypatch, capsys):
        """--project + --task-type: metadata linked, 1 task, state PLANNED, project shows job."""
        import json
        self._env(tmp_path, monkeypatch)
        from uuid import UUID
        from apps.cli.main import _cmd_create_job, _cmd_create_project, _cmd_show_project
        from packages.core.models import RunState
        from packages.orchestration.storage import load_job
        _cmd_create_project("CombinedTest", None)
        project_id = capsys.readouterr().out.strip()
        _cmd_create_job("combined prompt", project_id=project_id, task_type="write_readme")
        job_id = capsys.readouterr().out.strip()
        job = load_job(UUID(job_id))
        assert job.metadata.get("project_id") == project_id
        assert len(job.tasks) == 1
        assert job.tasks[0].inputs["task_type"] == "write_readme"
        assert job.state == RunState.PLANNED
        _cmd_show_project(project_id, json_output=True)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert any(j["id"] == job_id for j in d["jobs"])
