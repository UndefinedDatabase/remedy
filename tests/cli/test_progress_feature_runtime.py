"""Runtime subprocess tests for ``remedy progress`` and ``remedy feature`` CLI.

No shell=True. No background pytest.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

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


# ---------------------------------------------------------------------------
# progress checklist --agent
# ---------------------------------------------------------------------------


class TestProgressChecklistRuntime:

    def test_agent_mode_exit_zero(self):
        result = _run_grouped_cli(["progress", "checklist", "--agent", "--json"])
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_agent_mode_json_parses(self):
        result = _run_grouped_cli(["progress", "checklist", "--agent", "--json"])
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert "version" in data
        assert "items" in data
        assert "done_count" in data

    def test_agent_mode_text_output(self):
        result = _run_grouped_cli(["progress", "checklist", "--agent"])
        assert result.returncode == 0
        assert "Progress Ledger" in result.stdout

    def test_no_traceback(self):
        result = _run_grouped_cli(["progress", "checklist", "--agent", "--json"])
        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr

    def test_missing_job_safe(self, tmp_path):
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        result = _run_grouped_cli(
            ["progress", "checklist", "00000000-0000-0000-0000-000000000000", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )
        assert result.returncode != 0


# ---------------------------------------------------------------------------
# feature plan --agent
# ---------------------------------------------------------------------------


class TestFeaturePlanRuntime:

    def test_agent_mode_exit_zero(self):
        result = _run_grouped_cli(["feature", "plan", "--agent", "--json"])
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_agent_mode_json_parses(self):
        result = _run_grouped_cli(["feature", "plan", "--agent", "--json"])
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        assert "version" in data
        assert "suggestions" in data
        assert "suggestion_count" in data

    def test_agent_mode_text_output(self):
        result = _run_grouped_cli(["feature", "plan", "--agent"])
        assert result.returncode == 0
        assert "Feature Plan" in result.stdout

    def test_no_traceback(self):
        result = _run_grouped_cli(["feature", "plan", "--agent", "--json"])
        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr

    def test_suggestions_exist(self):
        result = _run_grouped_cli(["feature", "plan", "--agent", "--json"])
        data = json.loads(result.stdout)
        assert data["suggestion_count"] >= 1

    def test_suggestion_has_required_fields(self):
        result = _run_grouped_cli(["feature", "plan", "--agent", "--json"])
        data = json.loads(result.stdout)
        if data["suggestions"]:
            sug = data["suggestions"][0]
            assert "suggestion_id" in sug
            assert "title" in sug
            assert "priority" in sug
            assert "source_type" in sug


# ---------------------------------------------------------------------------
# feature accept
# ---------------------------------------------------------------------------


class TestFeatureAcceptRuntime:

    def test_invalid_suggestion_safe(self, tmp_path):
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        from packages.core.models import Job, Task
        from packages.orchestration.storage import save_job
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            job = Job(name="accept-test", user_prompt="test")
            job.tasks = [Task(description="test")]
            save_job(job)
            job_id = str(job.id)
        finally:
            if old:
                os.environ["REMEDY_DATA_DIR"] = old
            else:
                os.environ.pop("REMEDY_DATA_DIR", None)

        result = _run_grouped_cli(
            ["feature", "accept", job_id, "nonexistent-sug", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )
        assert result.returncode != 0

    def test_no_traceback_on_error(self, tmp_path):
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        result = _run_grouped_cli(
            ["feature", "accept", "00000000-0000-0000-0000-000000000000", "fake", "--json"],
            env_extra={"REMEDY_DATA_DIR": str(data_dir)},
        )
        assert "Traceback" not in result.stdout
        assert "Traceback" not in result.stderr
