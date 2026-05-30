"""Tests for Steps 141-146 — Commit-readiness closure, safe-smoke final pass,
dev status integration, next action polish, CLI help.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _make_job(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = Task(description=t.get("description", task_type), inputs=inputs)
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 141 — Commit-Readiness Task Summary Bugfix
# ═══════════════════════════════════════════════════════════════════════════


class TestStep141_SafeTaskLabel:
    """_safe_task_label must not crash and must sanitize output."""

    def test_task_with_inputs_task_type(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="d", inputs={"task_type": "readme_draft"})
        assert _safe_task_label(t) == "readme_draft"

    def test_task_with_inputs_type(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="d", inputs={"type": "code_fix"})
        assert _safe_task_label(t) == "code_fix"

    def test_task_with_description_only(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="Fix the broken auth module")
        assert _safe_task_label(t) == "Fix the broken auth module"

    def test_task_with_neither(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="")
        assert _safe_task_label(t) == "task"

    def test_malicious_multiline_description(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="Line one\nLine two\nLine three")
        label = _safe_task_label(t)
        assert "\n" not in label
        assert label == "Line one"

    def test_long_description_truncated(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="A" * 200)
        label = _safe_task_label(t)
        assert len(label) <= 60

    def test_no_raw_leaks(self):
        from apps.cli.commands.repo import _safe_task_label
        from packages.core.models import Task
        t = Task(description="raw_output is bad", inputs={"task_type": "safe_label"})
        label = _safe_task_label(t)
        assert "raw_output" not in label

    def test_commit_readiness_no_crash(self):
        """The actual crash site: commit-readiness with real Task objects."""
        from packages.core.models import Job, Task
        from packages.orchestration.storage import save_job
        job = Job(name="no-crash")
        job.tasks.append(Task(description="fix stuff", inputs={"task_type": "bugfix"}))
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert "suggested_commit_message" in data
            assert "remedy/" in data["suggested_commit_message"]
            assert "bugfix" in data["suggested_commit_message"]

    def test_commit_readiness_no_task_type_attr(self):
        """Task objects must not require .task_type attribute."""
        from packages.core.models import Task
        t = Task(description="some work")
        assert not hasattr(t, "task_type") or getattr(t, "task_type", None) is None


# ═══════════════════════════════════════════════════════════════════════════
# Step 142 — Commit-Readiness Contract Hardening
# ═══════════════════════════════════════════════════════════════════════════


class TestStep142_ContractHardening:
    """Commit-readiness schema must be complete and safe."""

    def test_full_schema(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="schema")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            required = {
                "version", "job_id", "repo_path", "ready", "reasons",
                "changed_files", "changed_files_truncated",
                "tests_passed", "proof_present",
                "revert_available", "suggested_commit_message",
                "next_action",
            }
            missing = required - set(data.keys())
            assert not missing, f"Missing: {missing}"

    def test_changed_files_truncated_false(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="trunc-false")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["changed_files_truncated"] is False

    def test_missing_tests_not_ready(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="missing-tests")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["ready"] is False
            assert any("tests" in r for r in data["reasons"])

    def test_missing_proof_not_ready(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="missing-proof")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["proof_present"] is False
            assert any("proof" in r for r in data["reasons"])

    def test_no_git_mutation(self):
        """repo.py must not contain subprocess or git write commands."""
        content = Path("apps/cli/commands/repo.py").read_text()
        assert "subprocess" not in content
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith(("'", '"', "print")):
                continue
            assert "git push" not in stripped

    def test_no_shell_true(self):
        content = Path("apps/cli/commands/repo.py").read_text()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""'):
                continue
            assert "shell=True" not in stripped

    def test_no_raw_leaks(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="leaks")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            output = mock_print.call_args[0][0]
            for bad in ("raw_output", "command_output", "Traceback",
                         "diff_preview", "approval_reason"):
                assert bad not in output

    def test_human_output_concise(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="human")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=False)
            calls = [str(c) for c in mock_print.call_args_list]
            output = "\n".join(calls)
            assert "Commit readiness:" in output
            assert "read-only" in output.lower() or "No git" in output


# ═══════════════════════════════════════════════════════════════════════════
# Step 143 — Dev Status Includes Commit-Readiness
# ═══════════════════════════════════════════════════════════════════════════


class TestStep143_DevStatusCommitReadiness:
    """Dev status must include commit_readiness_ok."""

    def test_schema_includes_commit_readiness(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert "commit_readiness_ok" in data

    def test_no_smoke_returns_null(self):
        from apps.cli.commands.dev import _dev_status
        with patch("apps.cli.commands.dev._find_latest_smoke") as mock_smoke:
            mock_smoke.return_value = {
                "found": False, "status": "unknown",
                "job_id": "", "project_id": "", "smoke_log": "",
            }
            with patch("builtins.print") as mock_print:
                _dev_status(json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                assert data["commit_readiness_ok"] is None

    def test_exception_captured_safely(self):
        """If commit-readiness crashes, dev status still works."""
        from apps.cli.commands.dev import _dev_status
        with patch("apps.cli.commands.dev._find_latest_smoke") as mock_smoke:
            mock_smoke.return_value = {
                "found": True, "status": "passed",
                "job_id": str(uuid4()), "project_id": "", "smoke_log": "",
            }
            with patch("builtins.print") as mock_print:
                _dev_status(json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                # Job won't exist so commit_readiness should be False
                assert data["commit_readiness_ok"] is False

    def test_blocker_reported_when_not_ready(self):
        from apps.cli.commands.dev import _dev_status
        with patch("apps.cli.commands.dev._find_latest_smoke") as mock_smoke:
            mock_smoke.return_value = {
                "found": True, "status": "passed",
                "job_id": str(uuid4()), "project_id": "", "smoke_log": "",
            }
            with patch("builtins.print") as mock_print:
                _dev_status(json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                if data["commit_readiness_ok"] is False:
                    assert any("commit-readiness" in b for b in data["remaining_blockers"])


# ═══════════════════════════════════════════════════════════════════════════
# Step 144 — Smoke Closure
# ═══════════════════════════════════════════════════════════════════════════


class TestStep144_SmokeClosure:
    """Smoke script must include commit-readiness check."""

    def test_smoke_has_commit_readiness(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "commit-readiness" in content

    def test_smoke_validates_commit_readiness_schema(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "next_action" in content
        assert "changed_files_truncated" in content

    def test_smoke_checks_raw_leaks(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        # The commit-readiness section checks for raw leaks
        assert "raw_output" in content
        assert "command_output" in content

    def test_smoke_shows_help_on_failure(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "commit-readiness --help" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 145 — Commit-Readiness Next Action Surface
# ═══════════════════════════════════════════════════════════════════════════


class TestStep145_NextAction:
    """Commit-readiness must include grounded next_action."""

    def test_next_action_schema(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job
        job = Job(name="na-schema")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            na = data["next_action"]
            for field in ("label", "command", "risk", "requires_human"):
                assert field in na, f"next_action missing: {field}"

    def test_missing_tests_action(self):
        from apps.cli.commands.repo import _build_readiness_next_action
        na = _build_readiness_next_action(
            False, ["tests not passed after apply"], str(uuid4()), [],
        )
        assert "test" in na["label"].lower() or "test" in na["command"].lower()

    def test_missing_proof_action(self):
        from apps.cli.commands.repo import _build_readiness_next_action
        na = _build_readiness_next_action(
            False, ["no proof collected"], str(uuid4()), [],
        )
        assert "patch" in na["command"].lower()

    def test_missing_revert_action(self):
        from apps.cli.commands.repo import _build_readiness_next_action
        na = _build_readiness_next_action(
            False, ["no revert snapshot available"], str(uuid4()), [],
        )
        assert "revert" in na["label"].lower() or "patch" in na["command"].lower()

    def test_ready_action(self):
        from apps.cli.commands.repo import _build_readiness_next_action
        na = _build_readiness_next_action(True, [], str(uuid4()), [])
        assert na["requires_human"] is True
        assert na["risk"] == "medium"

    def test_no_raw_leaks_in_action(self):
        from apps.cli.commands.repo import _build_readiness_next_action
        na = _build_readiness_next_action(
            False, ["tests not passed after apply"], str(uuid4()), [],
        )
        na_str = json.dumps(na)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in na_str


# ═══════════════════════════════════════════════════════════════════════════
# Step 146 — Docs / CLI Help Polish
# ═══════════════════════════════════════════════════════════════════════════


class TestStep146_HelpPolish:
    """CLI help must include key commands and no stale content."""

    def test_root_help_includes_happy_path(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["--help"])
            output = str(mock_print.call_args[0][0])
            assert "remedy do" in output
            assert "remedy ui" in output
            assert "commit-readiness" in output
            assert "worker unload" in output
            assert "dev status" in output

    def test_repo_group_includes_commit_readiness(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["repo", "--help"])
            output = str(mock_print.call_args[0][0])
            assert "commit-readiness" in output
            assert "read-only" in output.lower() or "does not commit" in output.lower()

    def test_no_flat_commands_in_help(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["--help"])
            output = str(mock_print.call_args[0][0])
            # No flat argparse subcommands
            assert "add_subparsers" not in output

    def test_help_no_raw_leak_words(self):
        from apps.cli.grouped import main as grouped_main
        with patch("builtins.print") as mock_print:
            grouped_main(["--help"])
            output = str(mock_print.call_args[0][0])
            for bad in ("raw_output", "command_output", "Traceback"):
                assert bad not in output

    def test_main_py_under_120_lines(self):
        content = Path("apps/cli/main.py").read_text()
        assert len(content.splitlines()) <= 120

    def test_commit_readiness_read_only_documented(self):
        """Repo group description mentions read-only / does not commit."""
        from apps.cli.command_catalog import GROUPS
        desc = GROUPS["repo"].description.lower()
        assert "read-only" in desc or "does not commit" in desc
