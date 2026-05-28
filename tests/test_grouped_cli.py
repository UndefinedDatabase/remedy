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


# ---------------------------------------------------------------------------
# Step 43: Bootcamp-style UX lock tests
# ---------------------------------------------------------------------------


class TestBootcampStyleRootHelp:
    """Root help must be Bootcamp-style with boxes, no old flat commands."""

    def test_grouped_root_help_exits_zero(self) -> None:
        stdout, _, rc = _capture_grouped([])
        assert rc == 0

    def test_grouped_root_help_has_boxes(self) -> None:
        stdout, _, _ = _capture_grouped([])
        assert "\u256d" in stdout, "Root help missing box top-left corner"
        assert "\u256f" in stdout, "Root help missing box bottom-right corner"
        assert "Commands" in stdout

    def test_grouped_root_help_has_usage(self) -> None:
        stdout, _, _ = _capture_grouped([])
        assert "Usage:" in stdout

    def test_grouped_root_help_has_options(self) -> None:
        stdout, _, _ = _capture_grouped([])
        assert "Options" in stdout
        assert "--help" in stdout

    def test_main_root_help_exits_zero(self) -> None:
        stdout, _, rc = _capture_main([])
        assert rc == 0

    def test_main_root_help_has_boxes(self) -> None:
        stdout, _, _ = _capture_main([])
        assert "Commands" in stdout
        assert "\u256d" in stdout

    def test_grouped_help_flag_exits_zero(self) -> None:
        stdout, _, rc = _capture_grouped(["--help"])
        assert rc == 0
        assert "Commands" in stdout

    def test_main_help_flag_exits_zero(self) -> None:
        stdout, _, rc = _capture_main(["--help"])
        assert rc == 0
        assert "Commands" in stdout


class TestBootcampStyleGroupHelp:
    """Group help must have Usage, Options, Commands sections."""

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_group_help_has_usage(self, group_id: str) -> None:
        stdout, _, _ = _capture_grouped([group_id])
        assert "Usage:" in stdout

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_group_help_has_options(self, group_id: str) -> None:
        stdout, _, _ = _capture_grouped([group_id])
        assert "Options" in stdout
        assert "--help" in stdout

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_group_help_has_commands_box(self, group_id: str) -> None:
        stdout, _, _ = _capture_grouped([group_id])
        assert "Commands" in stdout
        assert "\u256d" in stdout

    @pytest.mark.parametrize("group_id", list(GROUPS.keys()))
    def test_group_help_flag(self, group_id: str) -> None:
        stdout, _, rc = _capture_grouped([group_id, "--help"])
        assert rc == 0
        assert "Commands" in stdout


class TestBootcampStyleCommandHelp:
    """Command-level help must be clean and contain expected info."""

    def test_job_create_help(self) -> None:
        stdout, _, rc = _capture_grouped(["job", "create", "--help"])
        assert rc == 0
        assert "prompt" in stdout.lower()
        assert "Arguments" in stdout or "Options" in stdout

    def test_patch_apply_help(self) -> None:
        stdout, _, rc = _capture_grouped(["patch", "apply", "--help"])
        assert rc == 0
        assert "job_id" in stdout.lower()
        assert "intent_id" in stdout.lower()

    def test_brain_graph_help(self) -> None:
        stdout, _, rc = _capture_grouped(["brain", "graph", "--help"])
        assert rc == 0
        assert "--json" in stdout
        assert "job_id" in stdout.lower()

    def test_test_run_help(self) -> None:
        stdout, _, rc = _capture_grouped(["test", "run", "--help"])
        assert rc == 0
        assert "job_id" in stdout.lower()


class TestBootcampStyleErrors:
    """Error output must be clean, no traceback, no argparse noise."""

    def test_unknown_group_clean(self) -> None:
        stdout, stderr, rc = _capture_grouped(["bogus"])
        assert rc == 2
        combined = stdout + stderr
        assert "Traceback" not in combined
        assert "Error" in combined

    def test_unknown_subcommand_clean(self) -> None:
        stdout, stderr, rc = _capture_grouped(["job", "bogus"])
        assert rc == 2
        combined = stdout + stderr
        assert "Traceback" not in combined
        assert "Error" in combined

    def test_missing_args_shows_command_help(self) -> None:
        stdout, stderr, rc = _capture_grouped(["job", "create"])
        assert rc == 2
        combined = stdout + stderr
        assert "Traceback" not in combined
        # Should show command help with prompt info
        assert "prompt" in combined.lower()

    def test_no_old_flat_error_format(self) -> None:
        """Error must not say 'invalid choice' (old argparse)."""
        stdout, stderr, rc = _capture_grouped(["bogus"])
        combined = stdout + stderr
        assert "invalid choice" not in combined

    def test_no_traceback_on_bad_nested_args(self) -> None:
        stdout, stderr, rc = _capture_grouped(["brain", "graph", "--bogus-flag"])
        combined = stdout + stderr
        assert "Traceback" not in combined


class TestRootHelpNoOldFlatCommands:
    """Root help must not show any old flat command names."""

    OLD_FLAT = [
        "create-job", "list-jobs", "show-job", "plan-job", "plan-job-local",
        "attach-repo", "set-permission", "show-permissions",
        "run-next-task-local", "run-tests-local", "discover-commands",
        "brain-node", "brain-view", "list-patch-intents", "show-patch-intent",
        "approve-patch-intent", "apply-patch-intent", "reject-patch-intent",
        "create-project", "list-projects", "attach-project-repo",
        "attach-project-job", "show-project", "project-context",
        "run-contract", "token-policy",
    ]

    def test_grouped_no_old_flat(self) -> None:
        stdout, _, _ = _capture_grouped([])
        for old in self.OLD_FLAT:
            assert old not in stdout, f"Root help still shows old flat command: {old}"

    def test_main_no_old_flat(self) -> None:
        stdout, _, _ = _capture_main([])
        for old in self.OLD_FLAT:
            assert old not in stdout, f"Main root help still shows old flat command: {old}"
