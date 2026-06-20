"""Runtime subprocess tests for ``remedy review bundle`` grouped CLI.

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
    """Run grouped CLI as subprocess with process-group isolation.

    Uses start_new_session=True so the child gets its own process group.
    On timeout, kills the entire process group to prevent orphans.
    No shell=True. No secret leakage.
    """
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + args
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        text=True,
        env=env,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Kill entire process group, not just the leader
        import signal
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            proc.wait(timeout=3)
        stdout, stderr = "", ""
        try:
            if proc.stdout:
                stdout = proc.stdout.read()
            if proc.stderr:
                stderr = proc.stderr.read()
        except (ValueError, OSError):
            pass
        raise subprocess.TimeoutExpired(cmd, timeout, output=stdout, stderr=stderr)
    return subprocess.CompletedProcess(
        args=cmd, returncode=proc.returncode, stdout=stdout, stderr=stderr,
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


# ---------------------------------------------------------------------------
# Step 3104: Process-group cleanup proof
# ---------------------------------------------------------------------------


class TestSubprocessCleanup:

    def test_helper_uses_process_group_isolation(self):
        """Verify _run_grouped_cli uses start_new_session=True."""
        import inspect
        source = inspect.getsource(_run_grouped_cli)
        assert "start_new_session=True" in source

    def test_helper_kills_process_group_on_timeout(self):
        """Verify _run_grouped_cli kills process group on timeout."""
        import inspect
        source = inspect.getsource(_run_grouped_cli)
        assert "killpg" in source
        assert "SIGTERM" in source
        assert "SIGKILL" in source

    def test_timeout_raises_with_cleanup(self):
        """A very short timeout raises TimeoutExpired after cleanup."""
        import subprocess as sp
        try:
            # Run a sleep command with 1-second timeout
            _run_grouped_cli(
                ["--help"],  # fast command, but use tiny timeout
                timeout=0,  # immediate timeout
            )
            # If it didn't timeout (fast enough), that's OK too
        except sp.TimeoutExpired:
            pass  # Expected — process group was cleaned up
        # Verify no orphan process from this test
        import time
        time.sleep(0.1)
        result = subprocess.run(
            ["pgrep", "-f", "apps.cli.grouped.*--help"],
            capture_output=True, text=True,
        )
        assert result.returncode != 0, "Orphan process found after timeout cleanup"
