"""
Domain tests: orchestration/test_autonomy.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import ast
import shlex
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import mint_job_id
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

ORCH = REPO_ROOT / "packages" / "orchestration"


def _make_job(**overrides) -> JobPlan:
    defaults = {
        "job_id": uuid4(),
        "job_title": "test-job",
        "user_prompt": "test prompt",
        "tasks": [
            TaskEntry(title="task 1", status=RunState.COMPLETED),
        ],
        "state": RunState.COMPLETED,
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return JobPlan(**defaults)


# ── Step 68.1: Event Schema Registry ────────────────────────────────────


class TestReadinessDecisionIntegration:
    def test_readiness_signals_include_decisions(self):
        from packages.orchestration.autonomy_readiness import _collect_signals
        job = _make_job()
        signals = _collect_signals(job, [])
        assert "no_open_decisions" in signals

    def test_no_open_decisions_true_when_clean(self):
        from packages.orchestration.autonomy_readiness import _collect_signals
        job = _make_job()
        signals = _collect_signals(job, [])
        assert signals["no_open_decisions"] is True

    def test_no_open_decisions_false_with_failures(self):
        from packages.orchestration.autonomy_readiness import _collect_signals
        job = _make_job()
        events = [
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.job_id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        signals = _collect_signals(job, events)
        assert signals["no_open_decisions"] is False


# ── Step 258: Generated Command Contract ────────────────────────────────────


class TestGeneratedCommandCatalogConsistency:
    def test_remedy_test_list_is_a_valid_command(self):
        """`remedy test list` became a real catalog command in Real Test Execution v1 (Step 1887):
        a read-only safe listing of test run records. It was previously a hallucination guard; now it
        is valid, so the assertion is inverted to require it to be a registered catalog command."""
        from apps.cli.command_catalog import CATALOG
        ids = {(c.group_id, c.subcommand) for c in CATALOG}
        assert ("test", "list") in ids, "remedy test list must be a registered catalog command"

    def test_generated_commands_reference_catalog(self):
        """Generated guidance commands should use valid catalog entries."""
        from apps.cli.command_catalog import CATALOG
        valid_commands = {f"{c.group_id} {c.subcommand}" for c in CATALOG}

        # Check readiness next_actions
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan(job_title="test", user_prompt="test")
        report = assess_job_readiness(job, [])
        for action in report.next_actions:
            if action.startswith("remedy "):
                # Extract "group subcommand" from "remedy group subcommand ..."
                parts = action.split()
                if len(parts) >= 3:
                    cmd_key = f"{parts[1]} {parts[2]}"
                    assert cmd_key in valid_commands, f"Invalid command: {action}"


# ── Step 259: Autonomy Level Single Source Of Truth ─────────────────────────


class TestAutonomyLevelSingleSourceOfTruth:
    def test_loop_imports_shared_levels(self):
        """Loop uses LEVELS from autonomy_readiness."""
        src = (ORCH / "autonomy_loop.py").read_text()
        assert "from packages.orchestration.autonomy_readiness import LEVELS" in src

    def test_level_names_match(self):
        """Level names in readiness and loop must agree."""
        from packages.orchestration.autonomy_readiness import LEVELS

        expected_names = ["observe", "propose", "approved_apply", "test_execution",
                         "bounded_loop", "revert_capable", "external_tools", "provider_autonomy"]
        for lvl in LEVELS:
            assert lvl["name"] == expected_names[lvl["level"]]

    def test_loop_respects_readiness(self):
        """Loop blocks if requested level exceeds readiness or has blockers."""
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan(job_title="test", user_prompt="test")
        # Request level 4 (bounded_loop) but job has no signals → blocked
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=4)
        assert result.final_decision == "blocked"
        # Must be blocked for valid reason (readiness or active blockers)
        reason = result.cycles[0].reason.lower()
        assert "blocker" in reason or "readiness" in reason

    def test_levels_6_7_blocked(self):
        """Levels 6-7 must be blocked (future only)."""
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan(job_title="test", user_prompt="test")
        report = assess_job_readiness(job, [])
        assert report.levels[6].eligible is False
        assert report.levels[7].eligible is False
        assert "not_connected" in report.levels[6].blockers[0] or "not_implemented" in str(report.levels[6].blockers)


# ── Step 260: Mutation + Execution Safety Quick Wins ────────────────────────


class TestMutationExecutionSafetyInvariants:
    # Part A: source_apply permission boundary
    def test_source_apply_permission_denied(self):
        """source_apply blocks without repo_generated_write permission."""
        from packages.orchestration.pingpong_job import JobPlan
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import StructuredPatch

        job = JobPlan(job_title="test", user_prompt="test", metadata={"permissions": {}})
        patch = StructuredPatch(intent_kind="file_ops", file_ops=[], unified_diffs=[])
        result = apply_structured_patch(patch, Path("/tmp/fake"), job=job)
        assert result.success is False
        assert "permission denied" in result.errors[0]

    def test_source_apply_no_public_cli_route_without_permission(self):
        """No CLI command calls source_apply without permission check context."""
        # The only CLI usage is in dev.py which just checks it's callable
        src = (REPO_ROOT / "apps" / "cli" / "commands" / "dev.py").read_text()
        assert "callable(apply_structured_patch)" in src
        # Not actually calling it to apply patches
        assert "apply_structured_patch(patch" not in src.replace("callable(apply_structured_patch)", "")

    # Part B: test runner output bound
    def test_output_truncation_constant(self):
        src = (ORCH / "test_runner.py").read_text()
        assert "MAX_TEST_OUTPUT_BYTES" in src
        assert "1_048_576" in src or "1048576" in src

    def test_truncation_marker(self):
        src = (ORCH / "test_runner.py").read_text()
        assert "[remedy output truncated]" in src

    # Part C: command discovery uses shlex
    def test_command_discovery_uses_shlex(self):
        src = (ORCH / "command_discovery.py").read_text()
        assert "import shlex" in src
        assert "shlex.split" in src

    def test_shell_metacharacters_rejected(self):
        """Constitution commands with shell ops are rejected."""
        src = (ORCH / "command_discovery.py").read_text()
        assert "_SHELL_METACHARACTERS" in src
        for mc in ("|", "&&", ";", "`", "$("):
            assert mc in src

    def test_shlex_parses_quoted_args(self):
        """shlex correctly handles quoted args."""
        result = shlex.split('python3 -m pytest "tests/my test"')
        assert result == ["python3", "-m", "pytest", "tests/my test"]

    # Part D: repo hygiene
    def test_no_forbidden_paths_tracked(self):
        """Forbidden generated paths must not be git-tracked."""
        import subprocess
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=10,
        )
        tracked = result.stdout.strip().split("\n")
        forbidden_prefixes = [
            "apps/ui/node_modules/",
            "__pycache__/",
            ".pytest_cache/",
        ]
        for fp in tracked:
            for prefix in forbidden_prefixes:
                assert not fp.startswith(prefix), f"Forbidden tracked path: {fp}"

    # Safety invariants
    def test_no_shell_true_in_orchestration(self):
        """No shell=True in subprocess calls (excluding test_runner docs)."""
        exempt = {"test_runner.py"}
        for f in ORCH.glob("*.py"):
            if f.name in exempt:
                continue
            src = f.read_text()
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.keyword) and node.arg == "shell":
                    if isinstance(node.value, ast.Constant) and node.value.value is True:
                        pytest.fail(f"{f.name} has shell=True in code")

    def test_no_0000_bind(self):
        for f in ORCH.glob("*.py"):
            src = f.read_text()
            assert "0.0.0.0" not in src, f"{f.name} binds 0.0.0.0"


class TestGitStatusReader:
    def test_read_current_repo(self):
        from packages.orchestration.git_status import read_git_status

        status = read_git_status(".")
        assert status.is_git_repo is True
        assert len(status.current_branch) > 0
        assert len(status.head_sha) > 0

    def test_read_nonexistent_dir(self):
        from packages.orchestration.git_status import read_git_status

        status = read_git_status("/tmp/nonexistent_dir_xyz_12345")
        assert status.is_git_repo is False
        assert "not a directory" in status.error

    def test_read_non_git_dir(self, tmp_path):
        from packages.orchestration.git_status import read_git_status

        status = read_git_status(str(tmp_path))
        assert status.is_git_repo is False

    def test_read_git_repo_with_untracked(self, tmp_path):
        from packages.orchestration.git_status import read_git_status

        # Create a git repo with an untracked file
        subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
        subprocess.run(
            ["git", "-C", str(tmp_path), "config", "user.email", "test@test.com"],
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(tmp_path), "config", "user.name", "Test"],
            capture_output=True,
        )
        # Need at least one commit for HEAD to exist
        (tmp_path / "README.md").write_text("hello")
        subprocess.run(["git", "-C", str(tmp_path), "add", "."], capture_output=True)
        subprocess.run(
            ["git", "-C", str(tmp_path), "commit", "-m", "init"],
            capture_output=True,
        )
        # Add untracked file
        (tmp_path / "untracked.txt").write_text("x")

        status = read_git_status(str(tmp_path))
        assert status.is_git_repo is True
        assert status.is_clean is False
        assert "untracked.txt" in status.untracked_files

    def test_no_shell_true(self):
        """Verify _run_git never uses shell=True."""
        import ast

        with open("packages/orchestration/git_status.py") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg == "shell":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    pytest.fail("shell=True found in git_status.py")


class TestStopReasonsCRUD:
    def test_create_and_list(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            list_stop_reasons,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id,
            source="test",
            reason_code="test_failed",
            safe_summary="Test failed in CI.",
            next_actions=("re-run tests",),
        )
        assert sr.status == "active"
        assert sr.reason_code == "test_failed"

        all_stops = list_stop_reasons(job_id)
        assert len(all_stops) == 1
        assert all_stops[0].id == sr.id

    def test_get_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            get_stop_reason,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id, source="test", reason_code="no_target_repo",
            safe_summary="No repo.", next_actions=(),
        )
        found = get_stop_reason(job_id, sr.id)
        assert found is not None
        assert found.reason_code == "no_target_repo"

        missing = get_stop_reason(job_id, "nonexistent")
        assert missing is None

    def test_resolve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            get_stop_reason,
            resolve_stop_reason,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id, source="test", reason_code="not_approved",
            safe_summary="Waiting.", next_actions=(),
        )
        resolved = resolve_stop_reason(job_id, sr.id, "approved now")
        assert resolved is not None
        assert resolved.status == "resolved"
        assert resolved.resolved_at is not None

        # Verify persistence
        loaded = get_stop_reason(job_id, sr.id)
        assert loaded.status == "resolved"


class TestStopReasonsDerive:
    def test_derive_no_repo(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = JobPlan(job_id=mint_job_id(), job_title="d1", user_prompt="test", metadata={})
        reasons = derive_stop_reasons(job, [])
        codes = [r.reason_code for r in reasons]
        assert "no_target_repo" in codes

    def test_derive_test_failed(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = JobPlan(
            job_id=mint_job_id(), job_title="d2", user_prompt="test",
            metadata={"target_repo": "/tmp/repo"},
        )
        events = [
            {"event": "test_run_completed", "metadata": {"status": "failed"}},
        ]
        reasons = derive_stop_reasons(job, events)
        codes = [r.reason_code for r in reasons]
        assert "test_failed" in codes

class TestStopReasonExport:
    def test_export_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.stop_reasons import (
            create_stop_reason,
            export_stop_reason_json,
        )

        job_id = uuid4().hex[:16]
        sr = create_stop_reason(
            job_id, source="test", reason_code="test_failed",
            safe_summary="Failed.", next_actions=("fix",),
        )
        data = export_stop_reason_json(sr)
        assert data["reason_code"] == "test_failed"
        assert data["status"] == "active"
        assert isinstance(data["next_actions"], list)


class TestAutonomyLoopBasic:
    def test_level_0_observe(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(
            job_id=mint_job_id(), job_title="loop0", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job_plan(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        assert result.version == 1
        assert result.final_decision == "complete"
        assert result.autonomy_level == 0
        assert len(result.cycles) == 1
        assert result.cycles[0].decision == "complete"

    def test_level_1_needs_approval(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(
            job_id=mint_job_id(), job_title="loop1", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job_plan(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "needs_approval"

    def test_completed_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(
            job_id=mint_job_id(), job_title="loop-done", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.COMPLETED)],
            state=RunState.COMPLETED,
            metadata={"target_repo": "."},
        )
        save_job_plan(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "complete"

    def test_blocked_by_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(
            job_id=mint_job_id(), job_title="loop-blocked", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
            metadata={},  # No target_repo → blocker
        )
        save_job_plan(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "blocked"
        assert len(result.stop_reasons) >= 1


class TestAutonomyLoopExport:
    def test_export_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import (
            export_loop_result_json,
            run_autonomy_loop,
        )
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(
            job_id=mint_job_id(), job_title="loop-ex", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job_plan(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        data = export_loop_result_json(result)
        assert data["version"] == 1
        assert isinstance(data["cycles"], list)
        assert data["final_decision"] == "complete"

    def test_summarize(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import (
            run_autonomy_loop,
            summarize_loop_result,
        )
        from packages.orchestration.pingpong_job import save_job_plan

        job = JobPlan(
            job_id=mint_job_id(), job_title="loop-sum", user_prompt="test",
            tasks=[TaskEntry(title="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job_plan(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        text = summarize_loop_result(result)
        assert "Autonomy Loop" in text
        assert "Level: 0" in text


class TestTheLevelFiveGateReadsDurableSnapshotTruth:
    """F277 T001: autonomy level 5 was blocked for every job that reached it.

    `autonomy_loop._decide` gated level 5 on a `snapshot_created` event, a name
    nothing in this repository writes, so the `any(...)` was always False and
    the loop answered "no snapshot for revert" however good the snapshot was.
    The signal that answers the question is `verified_snapshot`, which
    `autonomy_readiness` derives from `repository_snapshot.build_snapshot_truth`
    (Step 1159) and which `run_autonomy_loop` computes one statement before it
    calls `_decide`.  The branch had no test at all until this one.
    """

    @staticmethod
    def _decide_at_level_5(signals):
        from packages.orchestration.autonomy_loop import _decide

        job = JobPlan(job_id=mint_job_id(), job_title="revert-gate",
                      user_prompt="t", tasks=[TaskEntry(title="t")])
        return _decide(job, [], 5, 5, [], 1, signals)

    def test_a_durably_verified_snapshot_unblocks_the_level(self):
        decision, reason, _, blocked_by = self._decide_at_level_5(
            {"verified_snapshot": True}
        )
        assert decision == "complete"
        assert blocked_by == ""
        assert "revert capability confirmed" in reason

    def test_no_durable_snapshot_blocks_the_level(self):
        decision, reason, _, blocked_by = self._decide_at_level_5(
            {"verified_snapshot": False}
        )
        assert decision == "blocked"
        assert blocked_by == "missing_snapshot"
        assert "durably verified" in reason

    def test_the_retired_event_no_longer_decides_anything(self):
        """A `snapshot_created` event is not proof and must not unblock."""
        from packages.orchestration.autonomy_loop import _decide

        job = JobPlan(job_id=mint_job_id(), job_title="revert-gate",
                      user_prompt="t", tasks=[TaskEntry(title="t")])
        events = [{"event": "snapshot_created", "metadata": {"snapshot_id": "s-1"}},
                  {"event": "snapshot_create_completed", "metadata": {}}]
        decision, _, _, blocked_by = _decide(job, events, 5, 5, [], 1,
                                             {"verified_snapshot": False})
        assert decision == "blocked"
        assert blocked_by == "missing_snapshot"

    def test_the_loop_hands_the_gate_the_signals_it_computed(self, tmp_path, monkeypatch):
        """The wiring, not the branch: `run_autonomy_loop` must pass `signals`.

        A default of None would make the gate block silently forever, which is
        indistinguishable on the page from the defect this round removes.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import packages.orchestration.autonomy_loop as loop

        seen = {}
        real = loop._decide

        def spy(*args):
            seen["argc"] = len(args)
            seen["signals"] = args[6] if len(args) > 6 else None
            return real(*args)

        monkeypatch.setattr(loop, "_decide", spy)
        job = JobPlan(job_id=mint_job_id(), job_title="wiring", user_prompt="t",
                      tasks=[TaskEntry(title="t", status=RunState.PENDING)])
        loop.run_autonomy_loop(job, [], max_cycles=1, autonomy_level=5)
        assert seen["argc"] == 7, "run_autonomy_loop stopped passing the signal dict"
        assert isinstance(seen["signals"], dict)
        assert "verified_snapshot" in seen["signals"]
