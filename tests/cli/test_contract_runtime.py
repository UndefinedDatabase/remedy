"""Runtime CLI tests for contract inspect and contract check commands."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest


def _run_cli(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Run CLI command via subprocess. No shell=True."""
    cmd = [sys.executable, "-m", "apps.cli.grouped"] + list(args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


class TestContractInspectCLI:
    def test_missing_job_safe(self):
        r = _run_cli("contract", "inspect", "00000000-0000-0000-0000-000000000000", "--json")
        assert r.returncode != 0
        assert "Traceback" not in r.stderr
        out = json.loads(r.stdout)
        assert "error" in out

    def test_invalid_job_safe(self):
        r = _run_cli("contract", "inspect", "not-a-uuid", "--json")
        assert r.returncode != 0
        assert "Traceback" not in r.stderr


class TestContractCheckCLI:
    def test_missing_job_safe(self):
        r = _run_cli("contract", "check", "00000000-0000-0000-0000-000000000000", "apply", "--json")
        assert r.returncode != 0
        assert "Traceback" not in r.stderr

    def test_json_parses(self):
        """Even error output should be valid JSON when --json is passed."""
        r = _run_cli("contract", "check", "00000000-0000-0000-0000-000000000000", "apply", "--json")
        out = json.loads(r.stdout)
        assert "error" in out

    def test_no_shell_true_in_source(self):
        """Verify no shell=True in contract_cmd.py."""
        import inspect
        from apps.cli.commands import contract_cmd
        source = inspect.getsource(contract_cmd)
        assert "shell=True" not in source

    def test_no_traceback_on_bad_action(self):
        r = _run_cli("contract", "check", "00000000-0000-0000-0000-000000000000", "totally_fake_action", "--json")
        assert "Traceback" not in r.stderr
