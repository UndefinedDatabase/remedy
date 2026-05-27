"""
Behavioral tests for the group-first CLI (apps.cli.grouped).

Coverage:
  - Group help exits 0 for each group
  - Group help includes expected subcommands
  - Grouped aliases execute real underlying behavior
  - JSON commands output parseable JSON only
  - Invalid subcommands fail cleanly with no traceback
  - Public help does not present old flat commands
  - No help page leaks raw prompt/artifact/diff/approval/output content
"""

from __future__ import annotations

import json
import subprocess
import sys
from io import StringIO
from uuid import uuid4

import pytest

from apps.cli.command_catalog import GROUPS, get_commands_for_group
from apps.cli.grouped import build_parser, main as grouped_main
from packages.core.models import Job, Task
from packages.orchestration.storage import save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job() -> Job:
    return Job(
        id=uuid4(),
        name="test-job",
        user_prompt="test prompt",
        tasks=[Task(id=uuid4(), description="task-0")],
    )


def _capture_grouped(argv: list[str]) -> tuple[str, str, int]:
    """Run grouped CLI via subprocess, return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped"] + argv,
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout, result.stderr, result.returncode


# ---------------------------------------------------------------------------
# Group help tests
# ---------------------------------------------------------------------------


class TestGroupHelpExitsZero:
    """Typing a group name alone must show help and exit 0."""

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_group_help_exits_zero(self, group_id: str) -> None:
        stdout, stderr, rc = _capture_grouped([group_id])
        assert rc == 0, f"remedy {group_id} exited {rc}: {stderr}"
        assert group_id in stdout or "Commands" in stdout or "usage" in stdout.lower()


class TestGroupHelpContent:
    """Group help must list expected subcommands."""

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_group_help_lists_subcommands(self, group_id: str) -> None:
        stdout, _, _ = _capture_grouped([group_id])
        cmds = get_commands_for_group(group_id)
        for cmd in cmds:
            assert cmd.subcommand in stdout, (
                f"'remedy {group_id}' help missing subcommand '{cmd.subcommand}'"
            )


class TestGroupHelpNoLeaks:
    """Help pages must not contain sensitive content."""

    FORBIDDEN = (
        "sk-", "ghp_", "password=", "BEGIN PRIVATE KEY",
        "raw_stdout", "raw_stderr", "diff_preview",
        "approval_reason", "Traceback",
    )

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_help_no_sensitive_leaks(self, group_id: str) -> None:
        stdout, stderr, _ = _capture_grouped([group_id])
        combined = stdout + stderr
        for bad in self.FORBIDDEN:
            assert bad not in combined, (
                f"'remedy {group_id}' help leaks: {bad}"
            )


# ---------------------------------------------------------------------------
# Top-level help
# ---------------------------------------------------------------------------


class TestTopLevelHelp:
    def test_no_args_shows_help(self) -> None:
        stdout, _, rc = _capture_grouped([])
        assert rc == 0
        assert "remedy" in stdout.lower()
        for gid in GROUPS:
            assert gid in stdout, f"Top-level help missing group: {gid}"

    def test_no_old_flat_commands_in_help(self) -> None:
        stdout, _, _ = _capture_grouped([])
        old_flat = [
            "create-job", "list-jobs", "show-job", "attach-repo",
            "set-permission", "brain-node", "run-contract",
            "token-policy", "list-patch-intents",
        ]
        for old in old_flat:
            assert old not in stdout, (
                f"Top-level help still shows old flat command: {old}"
            )


# ---------------------------------------------------------------------------
# Error behavior
# ---------------------------------------------------------------------------


class TestCleanErrors:
    def test_invalid_group_no_traceback(self) -> None:
        stdout, stderr, rc = _capture_grouped(["nonexistent"])
        assert rc != 0
        assert "Traceback" not in stderr
        assert "Traceback" not in stdout

    def test_invalid_subcommand_no_traceback(self) -> None:
        stdout, stderr, rc = _capture_grouped(["job", "nonexistent"])
        assert rc != 0
        assert "Traceback" not in stderr
        assert "Traceback" not in stdout

    def test_missing_required_arg_no_traceback(self) -> None:
        stdout, stderr, rc = _capture_grouped(["brain", "graph"])
        assert rc != 0
        assert "Traceback" not in stderr


# ---------------------------------------------------------------------------
# Real command execution through grouped CLI
# ---------------------------------------------------------------------------


class TestGroupedExecution:
    def test_worker_list_json(self) -> None:
        stdout, stderr, rc = _capture_grouped(["worker", "list", "--json"])
        assert rc == 0, f"worker list --json failed: {stderr}"
        data = json.loads(stdout)
        assert data["version"] == 1
        assert isinstance(data["providers"], list)

    def test_job_list(self) -> None:
        stdout, stderr, rc = _capture_grouped(["job", "list"])
        assert rc == 0, f"job list failed: {stderr}"

    def test_project_list(self) -> None:
        stdout, stderr, rc = _capture_grouped(["project", "list"])
        assert rc == 0, f"project list failed: {stderr}"

    def test_policy_contract_json(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        stdout, stderr, rc = _capture_grouped(["policy", "contract", str(job.id), "--json"])
        assert rc == 0, f"policy contract --json failed: {stderr}"
        data = json.loads(stdout)
        assert data["scope"] == "job"
        assert isinstance(data["autonomy_level"], int)

    def test_policy_token_json(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        stdout, stderr, rc = _capture_grouped(["policy", "token", str(job.id), "--json"])
        assert rc == 0, f"policy token --json failed: {stderr}"
        data = json.loads(stdout)
        assert data["scope"] == "job"

    def test_brain_graph_json(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        stdout, stderr, rc = _capture_grouped(["brain", "graph", str(job.id), "--json"])
        assert rc == 0, f"brain graph --json failed: {stderr}"
        data = json.loads(stdout)
        assert "nodes" in data
        assert "edges" in data

    def test_test_discover_json(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        stdout, stderr, rc = _capture_grouped(["test", "discover", str(job.id), "--json"])
        # Without a repo, discover exits 1 but still outputs valid JSON to stderr
        raw = stdout or stderr
        data = json.loads(raw)
        assert isinstance(data, dict)
        assert "job_id" in data

    def test_dev_smoke_help(self) -> None:
        stdout, stderr, rc = _capture_grouped(["dev", "smoke-help"])
        assert rc == 0
        assert "smoke" in stdout.lower()


# ---------------------------------------------------------------------------
# Bridge: apps.cli.main delegates group names to grouped CLI
# ---------------------------------------------------------------------------


def _capture_main(argv: list[str]) -> tuple[str, str, int]:
    """Run old main entry point via subprocess, return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main"] + argv,
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout, result.stderr, result.returncode


class TestMainEntrypointDelegatesGroupHelp:
    """Bug: stale installed `remedy` pointed to apps.cli.main:main.

    Typing `remedy job` produced 'invalid choice: job' instead of group help.
    The bridge in main() must detect group names and delegate to grouped CLI.
    """

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_main_entrypoint_delegates_group_help_to_grouped_cli(self, group_id: str) -> None:
        stdout, stderr, rc = _capture_main([group_id])
        assert rc == 0, f"remedy {group_id} via main exited {rc}: {stderr}"
        # Must show grouped help, not old flat "invalid choice" error
        assert "invalid choice" not in stderr, (
            f"remedy {group_id} via main still shows old flat argparse error"
        )
        assert "Traceback" not in stderr
        # Must include expected subcommands
        cmds = get_commands_for_group(group_id)
        for cmd in cmds:
            assert cmd.subcommand in stdout, (
                f"'remedy {group_id}' via main missing subcommand '{cmd.subcommand}'"
            )


class TestMainEntrypointDelegatesGroupDispatch:
    """Grouped commands dispatched through apps.cli.main must execute correctly."""

    def test_worker_list_json_via_main(self) -> None:
        stdout, stderr, rc = _capture_main(["worker", "list", "--json"])
        assert rc == 0, f"worker list --json via main failed: {stderr}"
        data = json.loads(stdout)
        assert data["version"] == 1

    def test_policy_contract_json_via_main(self) -> None:
        job = _make_job()
        save_job(job)
        stdout, stderr, rc = _capture_main(["policy", "contract", str(job.id), "--json"])
        assert rc == 0, f"policy contract --json via main failed: {stderr}"
        data = json.loads(stdout)
        assert data["scope"] == "job"


class TestMainEntrypointFlatCommandsStillWork:
    """Old flat commands must still work when invoked through main."""

    def test_list_jobs_flat(self) -> None:
        stdout, stderr, rc = _capture_main(["list-jobs"])
        assert rc == 0, f"list-jobs flat failed: {stderr}"

    def test_workers_flat(self) -> None:
        stdout, stderr, rc = _capture_main(["workers", "--json"])
        assert rc == 0, f"workers flat failed: {stderr}"
        data = json.loads(stdout)
        assert data["version"] == 1
