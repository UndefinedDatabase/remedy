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


# ---------------------------------------------------------------------------
# Step 1002: Runtime safety — secret prompt + protected path
# ---------------------------------------------------------------------------


def _setup_secret_job(tmp_path: Path) -> tuple[str, str]:
    """Create job with secret prompt and .env.secret patch target."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        from packages.core.models import Artifact, ArtifactKind, Job, Task
        from packages.orchestration.storage import save_job

        job = Job(
            name="secret-runtime",
            user_prompt="Deploy with key sk-live-abc123def456 to prod",
        )
        task = Task(description="deploy")
        job.tasks = [task]
        art = Artifact(
            name="deploy-patch",
            content="patch",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=task.id,
            metadata={
                "patch_intent_explanations": [
                    {
                        "file": ".env.secret",
                        "action": "modify",
                        "risk": "high",
                        "reason": "update api key",
                        "summary": "update secret env",
                    },
                    {
                        "file": "src/deploy.py",
                        "action": "modify",
                        "risk": "low",
                        "reason": "fix deploy",
                        "summary": "fix deploy script",
                    },
                ],
                "patch_intent_approvals": {},
            },
        )
        job.artifacts.append(art)
        save_job(job)
        return str(job.id), str(data_dir)
    finally:
        if old:
            os.environ["REMEDY_DATA_DIR"] = old
        else:
            os.environ.pop("REMEDY_DATA_DIR", None)


class TestRuntimeSafety:

    def test_secret_prompt_not_in_zip(self, tmp_path):
        import zipfile

        job_id, data_dir = _setup_secret_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        zip_path = data["output_path"]
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                content = zf.read(name).decode("utf-8", errors="replace")
                assert "sk-live-abc123def456" not in content, f"Secret leaked in {name}"

    def test_env_secret_not_in_zip(self, tmp_path):
        import zipfile

        job_id, data_dir = _setup_secret_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        data = json.loads(result.stdout)
        zip_path = data["output_path"]
        with zipfile.ZipFile(zip_path) as zf:
            for name in zf.namelist():
                content = zf.read(name).decode("utf-8", errors="replace")
                assert ".env.secret" not in content, f".env.secret leaked in {name}"

    def test_safe_path_still_in_bundle(self, tmp_path):
        import zipfile

        job_id, data_dir = _setup_secret_job(tmp_path)
        result = _run_grouped_cli(
            ["review", "bundle", job_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": data_dir},
        )
        data = json.loads(result.stdout)
        zip_path = data["output_path"]
        with zipfile.ZipFile(zip_path) as zf:
            cf = json.loads(zf.read("changed_files_safe.json"))
            paths = [f["path"] for f in cf["files"]]
            assert "src/deploy.py" in paths
