"""Runtime subprocess tests for ``remedy review bundle`` grouped CLI.

No shell=True. No background pytest. No in-process handler calls.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


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


def _setup_job(tmp_path: Path) -> tuple[str, str]:
    """Create a job. Returns (job_id, data_dir)."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        from packages.core.models import Job, Task
        from packages.orchestration.storage import save_job

        job = Job(name="bundle-runtime-test", user_prompt="test bundle CLI")
        task = Task(description="initial task")
        job.tasks = [task]
        save_job(job)
        return str(job.id), str(data_dir)
    finally:
        if old:
            os.environ["REMEDY_DATA_DIR"] = old
        else:
            os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# Runtime subprocess tests
# ---------------------------------------------------------------------------


class TestReviewBundleRuntime:

    def test_exit_zero_json(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_json_parses(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert data["bundle_version"] == 1
        assert data["job_id"] == job_id

    def test_output_zip_exists(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert Path(data["output_path"]).exists()

    def test_custom_output_path(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        out_path = str(tmp_path / "custom.zip")
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--output", out_path, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        assert data["output_path"] == out_path
        assert Path(out_path).exists()

    def test_missing_job_safe(self, tmp_path):
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        result = _run_grouped_cli(
            ["review", "bundle", "00000000-0000-0000-0000-000000000000", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )
        assert result.returncode != 0

    def test_no_traceback(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr

    def test_text_output(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0
        assert "Review Bundle" in result.stdout
        assert "Sections" in result.stdout

    def test_safety_in_json(self, tmp_path):
        job_id, data_dir = _setup_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        assert data["safety"]["is_safe"] is True
