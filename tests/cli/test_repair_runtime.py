"""Runtime subprocess tests for ``remedy repair`` grouped CLI.

Tests run ``python -m apps.cli.grouped repair start <job_id> <fail_id> --json``
as a real subprocess with a temp data dir.

No shell=True. No background pytest. No in-process handler calls.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_grouped_cli(
    args: list[str],
    env_extra: dict[str, str] | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    """Run grouped CLI as subprocess. No shell=True."""
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + args
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )


def _setup_job_with_failure(tmp_path: Path) -> tuple[str, str, str]:
    """Create a job with a persisted failure artifact. Returns (job_id, fail_art_id, data_dir)."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        from packages.core.models import Job, Task
        from packages.orchestration.storage import save_job
        from packages.orchestration.test_failure_artifact import (
            TestFailureArtifact,
            persist_failure_artifact,
        )

        job = Job(name="runtime-test", user_prompt="test")
        task = Task(description="initial task")
        job.tasks = [task]
        save_job(job)

        failure = TestFailureArtifact(
            artifact_id="temp",
            job_id=str(job.id),
            task_id=str(task.id),
            failure_kind="test_failed",
            safe_summary="3 tests failed in test_example.py",
        )
        art = persist_failure_artifact(job, failure)
        return str(job.id), str(art.id), str(data_dir)
    finally:
        if old:
            os.environ["REMEDY_DATA_DIR"] = old
        else:
            os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# Runtime subprocess tests
# ---------------------------------------------------------------------------


class TestRepairStartRuntime:

    def test_exit_zero_json(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_json_parses(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_json_has_required_keys(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert data["version"] == 1
        assert data["job_id"] == job_id
        assert data["fix_task_id"]
        assert data["stop_reason"] in ("fix_task_created", "approval_required")

    def test_json_no_raw_content(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        text = result.stdout
        assert "Traceback" not in text
        assert "stderr" not in text.lower()

    def test_text_output(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0
        assert "Repair Loop" in result.stdout
        assert "Fix task" in result.stdout


class TestRepairStartWithIntentRuntime:
    """Step 976: Close R-0006 — subprocess test for --fixture-patch-intent."""

    def test_exit_zero_with_intent(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--fixture-patch-intent", "true", "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_json_parses_with_intent(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--fixture-patch-intent", "true", "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert data["repair_patch_intent_id"], "repair_patch_intent_id must be non-empty"
        assert data["stop_reason"] == "approval_required"

    def test_next_action_references_real_intent(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--fixture-patch-intent", "true", "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        intent_id = data["repair_patch_intent_id"]
        assert intent_id in data["next_safe_action"]["command"]

    def test_intent_resolvable_via_approval_queue(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--fixture-patch-intent", "true", "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        intent_id = data["repair_patch_intent_id"]

        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = data_dir
        try:
            from packages.orchestration.approval_queue import get_patch_intent
            from packages.orchestration.storage import load_job
            job = load_job(job_id)
            intent = get_patch_intent(job, intent_id)
            assert intent is not None, f"get_patch_intent returned None for {intent_id}"
            assert intent["state"] == "pending"
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)

    def test_no_raw_content_with_intent(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "start", job_id, fail_id, "--fixture-patch-intent", "true", "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr


class TestRepairFailureShowRuntime:

    def test_exit_zero_json(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "failure-show", job_id, fail_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_json_has_failure_kind(self, tmp_path):
        job_id, fail_id, data_dir = _setup_job_with_failure(tmp_path)
        result = _run_grouped_cli(
            ["repair", "failure-show", job_id, fail_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert data["failure_kind"] == "test_failed"
        assert "3 tests failed" in data["safe_summary"]
