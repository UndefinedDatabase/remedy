"""Runtime CLI tests for snapshot inspect, list-applies, and patch revert commands.

Step 1151: Snapshot/revert CLI runtime tests (subprocess).
No shell=True. No Traceback in stderr on error paths.
"""

from __future__ import annotations

import json
import subprocess
import sys

_NULL_JOB_ID = "00000000-0000-0000-0000-000000000000"
_NULL_SNAP_ID = "00000000-0000-0000-0000-111111111111"
_NULL_INTENT_ID = "00000000-0"


def _run_cli(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Run CLI command via subprocess. No shell=True."""
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + list(args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# snapshot inspect
# ---------------------------------------------------------------------------


class TestSnapshotInspectCLI:

    def test_missing_job_safe(self):
        """Unknown job_id → error, no traceback."""
        r = _run_cli("snapshot", "inspect", _NULL_JOB_ID, _NULL_SNAP_ID, "--json")
        assert r.returncode != 0
        assert "Traceback" not in r.stderr

    def test_json_output_on_error(self):
        r = _run_cli("snapshot", "inspect", _NULL_JOB_ID, _NULL_SNAP_ID, "--json")
        out = json.loads(r.stdout)
        assert "error" in out or "status" in out

    def test_invalid_job_id_safe(self):
        r = _run_cli("snapshot", "inspect", "not-a-uuid", _NULL_SNAP_ID, "--json")
        assert "Traceback" not in r.stderr

    def test_no_shell_true_in_source(self):
        import inspect

        from apps.cli.commands import snapshot_cmds
        source = inspect.getsource(snapshot_cmds)
        assert "shell=True" not in source

    def test_no_raw_content_in_error_output(self):
        """Error output must not leak blobs, diffs, or file content."""
        r = _run_cli("snapshot", "inspect", _NULL_JOB_ID, _NULL_SNAP_ID, "--json")
        combined = r.stdout + r.stderr
        for forbidden in ("blob_", "diff --git", "Traceback", "recovery_blob"):
            assert forbidden not in combined, f"Forbidden term in output: {forbidden}"


# ---------------------------------------------------------------------------
# snapshot list-applies
# ---------------------------------------------------------------------------


class TestSnapshotListAppliesCLI:

    def test_missing_job_safe(self):
        r = _run_cli("snapshot", "list-applies", _NULL_JOB_ID, "--json")
        assert "Traceback" not in r.stderr

    def test_json_output_parseable(self):
        r = _run_cli("snapshot", "list-applies", _NULL_JOB_ID, "--json")
        out = json.loads(r.stdout)
        assert isinstance(out, dict)

    def test_invalid_job_id_safe(self):
        r = _run_cli("snapshot", "list-applies", "not-a-uuid", "--json")
        assert "Traceback" not in r.stderr

    def test_no_raw_content_in_error_output(self):
        r = _run_cli("snapshot", "list-applies", _NULL_JOB_ID, "--json")
        combined = r.stdout + r.stderr
        for forbidden in ("blob_", "diff --git", "Traceback", "recovery_blob"):
            assert forbidden not in combined


# ---------------------------------------------------------------------------
# patch revert
# ---------------------------------------------------------------------------


class TestPatchRevertCLI:

    def test_missing_job_safe(self):
        """Unknown job_id → permission denied, no traceback."""
        r = _run_cli("patch", "revert", _NULL_JOB_ID, _NULL_INTENT_ID, "--json")
        assert "Traceback" not in r.stderr

    def test_error_output_on_missing_job(self):
        """Missing job → error message in stdout or stderr."""
        r = _run_cli("patch", "revert", _NULL_JOB_ID, _NULL_INTENT_ID, "--json")
        combined = r.stdout + r.stderr
        assert combined.strip(), "Expected some output on missing job"

    def test_missing_job_returns_nonzero(self):
        r = _run_cli("patch", "revert", _NULL_JOB_ID, _NULL_INTENT_ID, "--json")
        assert r.returncode != 0

    def test_invalid_job_id_safe(self):
        r = _run_cli("patch", "revert", "not-a-uuid", _NULL_INTENT_ID, "--json")
        assert "Traceback" not in r.stderr

    def test_no_raw_content_in_error_output(self):
        r = _run_cli("patch", "revert", _NULL_JOB_ID, _NULL_INTENT_ID, "--json")
        combined = r.stdout + r.stderr
        for forbidden in ("blob_", "diff --git", "Traceback", "recovery_blob"):
            assert forbidden not in combined

    def test_no_shell_true_in_patch_source(self):
        import inspect

        from apps.cli.commands import patch
        source = inspect.getsource(patch)
        assert "shell=True" not in source
