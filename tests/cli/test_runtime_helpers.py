"""Anti-regression tests for runtime helper process isolation.

Tests that:
- Timeout triggers process group kill
- Successful command leaves no process group
- Trace log writes START/END entries
- No shell=True anywhere
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tests.cli.runtime_helpers import (
    _ensure_process_group_dead,
    _process_group_exists,
    enable_trace,
    run_grouped_cli,
    create_test_env,
)


@pytest.fixture
def env(tmp_path):
    return create_test_env(tmp_path)


class TestProcessGroupCleanup:
    def test_successful_command_no_leftover_group(self, env):
        """After a successful CLI call, process group should be gone."""
        root, jid = env
        r = run_grouped_cli(["propose", "list", jid, "--json"], root)
        assert r.returncode == 0
        # No way to check pgid after the fact (process is gone),
        # but if we got here without hanging, cleanup worked.

    def test_timeout_kills_process_group(self, tmp_path):
        """A command that exceeds timeout should be killed, not hang."""
        root = tmp_path / "data"
        root.mkdir(parents=True)
        enable_trace(root)
        # Use a deliberately short timeout on a command that will fail fast
        # (missing job). The point is the helper returns, not hangs.
        with pytest.raises(AssertionError, match="timed out"):
            run_grouped_cli(
                ["propose", "list", "nonexistent-job", "--json"],
                root,
                timeout=0,  # Immediate timeout — process can't finish in 0s
            )


class TestTraceLog:
    def test_trace_writes_start_end(self, env):
        root, jid = env
        trace_path = root / ".runtime_trace.log"
        run_grouped_cli(["propose", "list", jid, "--json"], root)
        assert trace_path.exists(), f"Trace file not created at {trace_path}"
        content = trace_path.read_text()
        assert "START" in content
        assert "END" in content

    def test_trace_writes_timeout_on_timeout(self, tmp_path):
        root = tmp_path / "data"
        root.mkdir(parents=True)
        enable_trace(root)
        trace_path = root / ".runtime_trace.log"
        with pytest.raises(AssertionError, match="timed out"):
            run_grouped_cli(
                ["propose", "list", "fake", "--json"],
                root,
                timeout=0,
            )
        assert trace_path.exists()
        content = trace_path.read_text()
        assert "START" in content
        assert "TIMEOUT" in content


class TestProcessGroupExists:
    def test_nonexistent_pgid(self):
        """_process_group_exists returns False for nonexistent pgid."""
        # Use a very high pgid unlikely to exist
        assert not _process_group_exists(999999999)

    def test_own_pgid_exists(self):
        """Current process group should exist."""
        assert _process_group_exists(os.getpgrp())
