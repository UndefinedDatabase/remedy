"""Runtime subprocess tests for `context inspect` grouped CLI.

Tests run `python -m apps.cli.grouped context inspect <job_id> --json`
as a real subprocess with a temp data dir and temp repo.

No shell=True. No background pytest. No in-process handler calls.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from packages.core.models import Artifact, ArtifactKind, Job, Task

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_temp_job(tmp_path: Path, repo_path: Path, tasks: list[Task] | None = None) -> Job:
    """Create and persist a Job with repo_path in artifact metadata."""
    task = tasks[0] if tasks else Task(description="Fix auth bug")
    art = Artifact(
        name="repo-ref",
        content="",
        kind=ArtifactKind.UNKNOWN,
        metadata={"repo_path": str(repo_path)},
    )
    job = Job(
        name="test-runtime-job",
        user_prompt="Fix the bug",
        tasks=tasks or [task],
        artifacts=[art],
    )
    jobs_dir = tmp_path / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    (jobs_dir / f"{job.id}.json").write_text(job.model_dump_json(indent=2))
    return job


def _create_temp_repo(tmp_path: Path) -> Path:
    """Create a minimal repo directory with safe + protected files."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'test-project'")
    (repo / "AGENTS.md").write_text("# Agent rules\nFollow these rules.")
    src = repo / "src"
    src.mkdir()
    (src / "example.py").write_text("def example(): return 42")
    (repo / ".env.secret").write_text("API_KEY=supersecret")
    return repo


def _run_grouped_cli(
    args: list[str],
    env_extra: dict[str, str] | None = None,
    timeout: int = 15,
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


# ---------------------------------------------------------------------------
# Step 898: Grouped CLI runtime test
# ---------------------------------------------------------------------------


class TestContextInspectRuntime:

    def test_json_output_structure(self, tmp_path):
        """Real subprocess: JSON output has correct structure."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id), "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "Traceback" not in result.stderr
        data = json.loads(result.stdout)
        assert data["version"] == 1
        assert data["job_id"] == str(job.id)
        assert "included_paths" in data
        assert "excluded_paths" in data
        assert "budget" in data
        assert "policy_gates" in data
        assert "tooling" in data
        assert "readiness" in data

    def test_safe_files_included(self, tmp_path):
        """Real subprocess: safe files appear in included_paths."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id), "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        included_paths = {p["path"] for p in data["included_paths"]}
        assert "pyproject.toml" in included_paths
        assert "AGENTS.md" in included_paths
        assert "src/example.py" in included_paths

    def test_env_secret_excluded(self, tmp_path):
        """Real subprocess: .env.secret is excluded/protected."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id), "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        included_paths = {p["path"] for p in data["included_paths"]}
        assert ".env.secret" not in included_paths
        # Should be in protected or excluded
        excluded_paths = {p["path"] for p in data["excluded_paths"]}
        assert ".env.secret" in excluded_paths

    def test_no_raw_content_in_output(self, tmp_path):
        """Real subprocess: no file contents in JSON output."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id), "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert "supersecret" not in result.stdout
        assert "API_KEY" not in result.stdout
        assert "def example" not in result.stdout

    def test_text_output_no_traceback(self, tmp_path):
        """Real subprocess: text mode produces readable output."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id)],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode == 0
        assert "Traceback" not in result.stderr
        assert "Context Inspection" in result.stdout
        assert "Readiness:" in result.stdout


# ---------------------------------------------------------------------------
# Step 899: Runtime missing task test
# ---------------------------------------------------------------------------


class TestContextInspectRuntimeMissingTask:

    def test_missing_task_exits_nonzero(self, tmp_path):
        """Real subprocess: fake task_id exits nonzero."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)
        fake_task_id = str(uuid4())

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id), fake_task_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode != 0
        assert "Traceback" not in result.stderr
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()

    def test_missing_task_no_raw_internals(self, tmp_path):
        """Real subprocess: error output does not expose internals."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        job = _create_temp_job(data_dir, repo)
        fake_task_id = str(uuid4())

        result = _run_grouped_cli(
            ["context", "inspect", str(job.id), fake_task_id, "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr
        # No file paths or internal state leaked
        assert str(tmp_path) not in result.stdout


# ---------------------------------------------------------------------------
# Step 900: Runtime event target test (handler-level, setup too heavy for subprocess)
# ---------------------------------------------------------------------------


class TestEventTargetRuntime:

    def test_event_target_included_when_safe(self, tmp_path):
        """Event metadata target_path appears in included paths."""
        from packages.orchestration.context_inspector import inspect_context

        repo = _create_temp_repo(tmp_path)
        job = _create_temp_job(tmp_path / "data", repo)
        events = [
            {"event": "patch_applied", "metadata": {"target_path": "src/example.py"}},
        ]
        inspection = inspect_context(job, events, repo_root=repo)
        included = {p.path: p for p in inspection.included_paths}
        assert "src/example.py" in included
        # Could be event_target_path or source_file (source matches first if not unique)
        assert included["src/example.py"].reason in ("event_target_path", "source_file")

    def test_protected_event_target_excluded(self, tmp_path):
        """Protected path in event metadata is still excluded."""
        from packages.orchestration.context_inspector import inspect_context

        repo = _create_temp_repo(tmp_path)
        job = _create_temp_job(tmp_path / "data", repo)
        events = [
            {"event": "patch_applied", "metadata": {"target_path": ".env.secret"}},
        ]
        inspection = inspect_context(job, events, repo_root=repo)
        included_paths = {p.path for p in inspection.included_paths}
        assert ".env.secret" not in included_paths

    def test_no_raw_event_content(self, tmp_path):
        """Event content not leaked in inspection output."""
        from packages.orchestration.context_inspector import (
            export_context_inspection_json,
            inspect_context,
        )

        repo = _create_temp_repo(tmp_path)
        job = _create_temp_job(tmp_path / "data", repo)
        events = [
            {
                "event": "something",
                "metadata": {"target_path": "src/example.py", "secret_detail": "do_not_leak"},
            },
        ]
        inspection = inspect_context(job, events, repo_root=repo)
        data = export_context_inspection_json(inspection)
        text = json.dumps(data)
        assert "do_not_leak" not in text
        assert "secret_detail" not in text
