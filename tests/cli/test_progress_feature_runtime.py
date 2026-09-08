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
