"""Runtime subprocess tests for ``remedy do`` grouped CLI.

Tests run ``python -m apps.cli.grouped do "safe docs change" --repo <tmp> --autonomy-level 3 --json``
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

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_temp_repo(tmp_path: Path) -> Path:
    """Create a minimal git repo with safe + protected files."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname = 'test-project'")
    (repo / "README.md").write_text("# Test Project\nSafe docs change target.")
    src = repo / "src"
    src.mkdir()
    (src / "example.py").write_text("def example(): return 42")
    (repo / ".env.secret").write_text("API_KEY=supersecret")
    # Init git so context inspector can work
    subprocess.run(
        ["git", "init"], cwd=repo, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "add", "."], cwd=repo, capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "init", "--allow-empty"],
        cwd=repo, capture_output=True, check=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _register_fixture_project(data_dir: Path, repo: Path) -> None:
    """Write a minimal project JSON so select_project resolves for repo."""
    projects = data_dir / "projects"
    projects.mkdir(parents=True, exist_ok=True)
    pid = str(uuid4())
    real_repo = str(repo.resolve())
    (projects / f"{pid}.json").write_text(json.dumps({
        "id": pid,
        "name": "test-project",
        "slug": "test-project",
        "repo_paths": [real_repo],
        "canonical_repo_path": real_repo,
        "job_ids": [],
    }))


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


# ---------------------------------------------------------------------------
# Step 919: Runtime subprocess tests for remedy do
# ---------------------------------------------------------------------------


class TestDoRuntime:
    """Full subprocess tests: remedy do --json."""

    def test_exit_zero_json(self, tmp_path):
        """Real subprocess: exit 0 with --json flag."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_json_parses(self, tmp_path):
        """Real subprocess: stdout is valid JSON."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_json_has_required_keys(self, tmp_path):
        """Real subprocess: JSON contains all required top-level keys."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        required = {
            "version", "job_id", "task_id", "artifact_ids",
            "patch_intent_id", "proof_status", "phases",
            "stop_reason", "next_safe_action", "autonomy_level",
            "repo_path_safe", "context_summary",
        }
        assert required.issubset(data.keys()), f"Missing: {required - data.keys()}"

    def test_stop_reason_approval(self, tmp_path):
        """Real subprocess: stop_reason is approval_required."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        sr = data["stop_reason"]
        assert sr["reason"] == "approval_required"

    def test_next_safe_action_present(self, tmp_path):
        """Real subprocess: next_safe_action contains a real command."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        nsa = data["next_safe_action"]
        assert isinstance(nsa, dict)
        assert "command" in nsa
        assert "remedy" in nsa["command"]

    def test_phases_present(self, tmp_path):
        """Real subprocess: phases list is non-empty."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        assert len(data["phases"]) >= 4  # init, plan, context, build, ...

    def test_no_traceback_in_output(self, tmp_path):
        """Real subprocess: no Python tracebacks in stdout or stderr."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr

    def test_no_raw_content_leaked(self, tmp_path):
        """Real subprocess: no file contents or secrets in JSON output."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert "supersecret" not in result.stdout
        assert "API_KEY" not in result.stdout
        assert "def example" not in result.stdout

    def test_no_absolute_paths_in_json(self, tmp_path):
        """Real subprocess: no absolute paths in JSON output."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        # repo_path_safe should be basename only
        assert "/" not in data["repo_path_safe"]


class TestDoRuntimeText:
    """Subprocess tests for text (non-JSON) output."""

    def test_text_output_readable(self, tmp_path):
        """Real subprocess: text mode produces readable summary."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode == 0
        assert "Traceback" not in result.stderr
        out = result.stdout.lower()
        assert "phase" in out or "stop" in out or "approval" in out


# ---------------------------------------------------------------------------
# Step 934: Runtime CLI contract/truth tests
# ---------------------------------------------------------------------------


class TestDoRuntimeTruth:
    """Subprocess tests for truth closure fields."""

    def test_autonomy_7_capped_in_json(self, tmp_path):
        """Real subprocess: --autonomy-level 7 shows capped in JSON."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "7", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["autonomy_level"] == 3
        assert data["requested_autonomy_level"] == 7
        assert data["autonomy_capped"] is True

    def test_run_contract_in_json(self, tmp_path):
        """Real subprocess: JSON output contains run_contract."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "3", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        data = json.loads(result.stdout)
        assert "run_contract" in data
        rc = data["run_contract"]
        assert rc["stop_before_apply"] is True
        assert rc["source"] in ("do_v1_minimal", "do_v1_caller_override")

    def test_max_cycles_zero_safe(self, tmp_path):
        """Real subprocess: --max-cycles 0 exits 0 with invalid_input."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--max-cycles", "0", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["stop_reason"]["reason"] == "invalid_input"
        assert "Traceback" not in result.stderr

    def test_no_raw_content_high_autonomy(self, tmp_path):
        """Real subprocess: high autonomy still no raw content."""
        repo = _create_temp_repo(tmp_path)
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        _register_fixture_project(data_dir, repo)

        result = _run_grouped_cli(
            ["do", "safe docs change", "--repo", str(repo),
             "--autonomy-level", "7", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )

        assert "supersecret" not in result.stdout
        assert "API_KEY" not in result.stdout
