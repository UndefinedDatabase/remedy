"""CLI subprocess tests for Managed Builder Execution v1 commands.

Uses the approved remedy_pytest runner pattern.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped"] + args,
        capture_output=True, text=True, timeout=30,
    )


class TestManagedBuilderExecutionCLI(unittest.TestCase):

    def test_template_list(self):
        r = _run(["execution", "template-list", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)
        assert len(data) >= 2  # default templates

    def test_template_show(self):
        r = _run(["execution", "template-show", "claude-code-repair-v0", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["template_id"] == "claude-code-repair-v0"
        assert data["enabled"] is False

    def test_template_show_invalid(self):
        r = _run(["execution", "template-show", "nonexistent-template-xyz", "--json"])
        assert r.returncode != 0

    def test_execution_show_invalid(self):
        r = _run(["execution", "show", "nonexistent-execution-xyz", "--json"])
        assert r.returncode != 0

    def test_execution_list(self):
        r = _run(["execution", "list", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)

    def test_debug_bundle_invalid(self):
        r = _run(["execution", "debug-bundle", "nonexistent-xyz", "--json"])
        assert r.returncode != 0

    def test_integrity(self):
        r = _run(["execution", "integrity", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert "passed" in data
        assert "violation_count" in data
        assert "approval_count" in data  # v1.1

    def test_approval_show_invalid(self):
        r = _run(["execution", "approval-show", "nonexistent-session-xyz", "--json"])
        assert r.returncode != 0

    def test_approval_validate_invalid(self):
        r = _run(["execution", "approval-validate", "nonexistent-session-xyz",
                   "--template", "nonexistent-tmpl", "--json"])
        assert r.returncode == 0  # returns codes, not error
        data = json.loads(r.stdout)
        assert data["valid"] is False
        assert "approval_not_found" in data["codes"]

    def test_approval_list(self):
        r = _run(["execution", "approval-list", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)

    def test_execution_list_limit(self):
        r = _run(["execution", "list", "--json", "--limit", "1"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)
        assert len(data) <= 1

    def test_execution_list_unknown_sort_field_exits_nonzero(self):
        r = _run(["execution", "list", "--json", "--sort", "bogus"])
        assert r.returncode != 0
        assert "unknown --sort field" in r.stderr


if __name__ == "__main__":
    unittest.main()
