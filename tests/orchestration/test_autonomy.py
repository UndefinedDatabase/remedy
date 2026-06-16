"""
Domain tests: orchestration/test_autonomy.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch
from unittest.mock import patch
from uuid import uuid4
import ast
import json
import os
import pytest
import shlex
import subprocess
import sys
import tempfile

from packages.core.models import Job, RunState, Task

_ROOT = Path(__file__).resolve().parent.parent.parent

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

ORCH = REPO_ROOT / "packages" / "orchestration"


def _make_job(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "description": "test job",
        "tasks": [
            Task(description="task 1", status=RunState.COMPLETED),
        ],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _make_job_s135(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = Task(
                description=t.get("description", task_type),
                inputs=inputs,
            )
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 135 — `remedy do "<goal>"` Direct Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s141(*, tasks=None, name="test"):
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


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


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
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        signals = _collect_signals(job, events)
        assert signals["no_open_decisions"] is False




class TestDevStatusHonestySchema:
    """Dev status must be honest about actual state."""

    def test_status_json_schema(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            required = {
                "version", "cli_ok", "latest_smoke", "ui_contract_ok",
                "task_progress_ok", "worker_cleanup_ok",
                "autocoder_fake_e2e_ok", "commit_readiness_ok",
                "remaining_blockers",
            }
            missing = required - set(data.keys())
            assert not missing

    def test_smoke_info_schema(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            smoke = data["latest_smoke"]
            assert "found" in smoke
            assert "status" in smoke
            assert "job_id" in smoke

    def test_no_smoke_reports_unknown(self):
        from apps.cli.commands.dev import _find_latest_smoke
        with patch("pathlib.Path.is_dir", return_value=False):
            result = _find_latest_smoke()
            assert result["found"] is False
            assert result["status"] == "unknown"

    def test_ui_contract_ok(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["ui_contract_ok"] is True
            assert data["task_progress_ok"] is True


# ═══════════════════════════════════════════════════════════════════════════
# Step 139 — Next Action Surface
# ═══════════════════════════════════════════════════════════════════════════




class TestNextActionGroundedInJobState:
    """Next action must be grounded in job state."""

    def test_completed_job_no_action(self):
        from packages.orchestration.ui_view_model import build_next_action
        from packages.core.models import RunState
        job = _make_job_s135(tasks=[{"type": "t1", "status": "completed"}])
        job.state = RunState.COMPLETED
        na = build_next_action(job, [])
        assert na["version"] == 1
        assert na["primary_action"]["label"] == "No action needed"

    def test_active_job_suggests_ui(self):
        from packages.orchestration.ui_view_model import build_next_action
        from packages.core.models import RunState
        job = _make_job_s135(tasks=[{"type": "t1", "status": "running"}])
        job.state = RunState.RUNNING
        na = build_next_action(job, [])
        assert "ui" in na["primary_action"]["command"].lower()

    def test_failed_test_suggests_inspect(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job_s135(tasks=[{"type": "t1", "status": "running"}])
        events = [{"event": "test_run_completed", "metadata": {"exit_code": 1}}]
        na = build_next_action(job, events)
        assert "test" in na["primary_action"]["label"].lower()

    def test_blocker_suggests_resolve(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job_s135()
        events = [{"event": "stop_reason_recorded", "outcome": "pending"}]
        na = build_next_action(job, events)
        assert "blocker" in na["primary_action"]["label"].lower()

    def test_reviewer_suggestion(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job_s135(tasks=[{
            "type": "review", "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        na = build_next_action(job, [])
        assert na["primary_action"]["requires_human"] is True

    def test_next_action_schema(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job_s135()
        na = build_next_action(job, [])
        required = {"version", "job_id", "stage", "primary_action", "secondary_actions"}
        assert not (required - set(na.keys()))
        pa = na["primary_action"]
        assert "label" in pa
        assert "command" in pa
        assert "risk" in pa
        assert "requires_human" in pa

    def test_secondary_actions_include_vram(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job_s135()
        na = build_next_action(job, [])
        cmds = [a["command"] for a in na["secondary_actions"]]
        assert any("worker unload" in c for c in cmds)

    def test_no_raw_leaks_in_next_action(self):
        from packages.orchestration.ui_view_model import build_next_action
        job = _make_job_s135()
        na = build_next_action(job, [])
        na_str = json.dumps(na)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in na_str

    def test_next_action_endpoint_registered(self):
        """next-action endpoint exists in UI server routes."""
        content = Path("packages/orchestration/ui_server.py").read_text()
        assert "next-action" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 140 — Commit-Readiness Preview
# ═══════════════════════════════════════════════════════════════════════════




class TestCommitReadinessPreviewReadOnly:
    """Commit readiness preview — read-only, no git writes."""

    def test_catalog_entry_exists(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next((c for c in CATALOG if c.command_id == "repo.commit-readiness"), None)
        assert cmd is not None

    def test_readiness_not_ready_no_tests(self):
        """Missing tests -> not ready."""
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="readiness-test")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["version"] == 1
            assert data["ready"] is False
            assert any("tests" in r for r in data["reasons"])

    def test_readiness_schema(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="schema-test")
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

    def test_readiness_no_proof(self):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="no-proof")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["proof_present"] is False
            assert any("proof" in r for r in data["reasons"])

    def test_readiness_does_not_mutate_git(self):
        """No subprocess git add/commit/push in repo.py (strings/comments OK)."""
        content = Path("apps/cli/commands/repo.py").read_text()
        assert "subprocess" not in content
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith(("'", '"', "print")):
                continue
            assert "git push" not in stripped

    def test_readiness_no_shell_true(self):
        content = Path("apps/cli/commands/repo.py").read_text()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""'):
                continue
            assert "shell=True" not in stripped

    def test_suggested_message_safe(self):
        """Suggested commit message should not contain raw content."""
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="msg-test")
        save_job(job)

        from apps.cli.commands.repo import _cmd_commit_readiness
        with patch("builtins.print") as mock_print:
            _cmd_commit_readiness(str(job.id), json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            msg = data["suggested_commit_message"]
            assert "remedy/" in msg
            for bad in ("raw_output", "Traceback", "diff_preview"):
                assert bad not in msg




class TestDevStatusIncludesCommitReadiness:
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




class TestCommitReadinessNextActionSurface:
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




class TestLiveRunningDefaultsFalseOnFailure:
    def test_live_running_defaults_false(self):
        """When liveData is empty (API failed), live.running must be false."""
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "liveData?.running ?? false" in src
        assert "liveData?.running ?? true" not in src

    def test_api_health_type_exists(self):
        src = (UI_SRC / "api" / "types.ts").read_text()
        assert "RemedyApiHealth" in src
        assert "degraded" in src
        assert "failedEndpoints" in src

    def test_dashboard_type_has_api_health(self):
        src = (UI_SRC / "api" / "types.ts").read_text()
        assert "apiHealth: RemedyApiHealth" in src

    def test_failed_endpoints_tracked(self):
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "failedEndpoints" in src
        # Dashboard-first: tracks failed endpoints including "dashboard" and "brain-view-model"
        assert "failedEndpoints" in src


# ── Step 257: Exact Dashboard Truth Contract v2 ─────────────────────────────




class TestDashboardV3RuntimeContract:
    def test_dashboard_v3_runtime(self):
        """Runtime test: _build_dashboard returns exact v2 contract shape."""
        from packages.core.models import Job
        from packages.orchestration.ui_server import _build_dashboard

        job = Job(name="truth-test", user_prompt="test contract")
        result = _build_dashboard(job)

        # Exact top-level fields
        assert result["version"] == 3
        assert "job_id" in result
        assert "generated_at" in result
        assert "source" in result
        assert result["source"] == "server"

        # Live block
        live = result["live"]
        assert "running" in live
        assert "state" in live
        assert "current_actor" in live
        assert "last_event_at" in live
        assert "stale" in live
        assert "confidence" in live

        # Metrics
        metrics = result["metrics"]
        assert "open" in metrics
        assert "planned" in metrics
        assert "done" in metrics
        assert "progress_percent" in metrics
        assert "source_counts" in metrics
        assert "computed_from" in metrics

        # Tasks list
        assert isinstance(result["tasks"], list)

        # Activity
        assert isinstance(result["activity"], list)

        # Phases
        assert isinstance(result["phases"], list)

        # Graph summary
        gs = result["graph_summary"]
        assert "node_count" in gs
        assert "edge_count" in gs
        assert "source" in gs
        assert "mode" in gs

        # Next action
        na = result["next_action"]
        assert "kind" in na
        assert "label" in na
        assert "requires_user" in na

        # Truth
        truth = result["truth"]
        assert "synthetic_count" in truth
        assert "demo_mode" in truth
        assert "missing_sources" in truth
        assert "computed_from" in truth

        # Redaction
        redaction = result["redaction"]
        assert redaction["raw_content_exposed"] is False
        assert "policy" in redaction

    def test_dashboard_with_tasks(self):
        """Dashboard with real tasks shows them correctly."""
        from packages.core.models import Job, Task
        from packages.orchestration.ui_server import _build_dashboard

        job = Job(
            name="has-tasks",
            user_prompt="test",
            tasks=[Task(description="First task"), Task(description="Second task")],
        )
        result = _build_dashboard(job)
        assert len(result["tasks"]) == 2
        assert result["tasks"][0]["title"] == "First task"
        assert result["tasks"][0]["source"] == "real"
        assert result["truth"]["demo_mode"] is False  # No events ≠ demo (Step 263 fix)
        assert result["truth"]["synthetic_count"] == 0

    def test_dashboard_no_fake_task_names(self):
        """Tasks must not have generic fake names."""
        from packages.core.models import Job, Task
        from packages.orchestration.ui_server import _build_dashboard

        job = Job(name="real", user_prompt="test", tasks=[Task(description="Parse the config file")])
        result = _build_dashboard(job)
        assert result["tasks"][0]["title"] == "Parse the config file"

    def test_dashboard_no_raw_content(self):
        """Dashboard must not expose raw content."""
        from packages.core.models import Job
        from packages.orchestration.ui_server import _build_dashboard

        job = Job(name="test", user_prompt="secret prompt with API_KEY=abc123")
        result = _build_dashboard(job)
        payload = json.dumps(result)
        assert "API_KEY" not in payload
        assert "abc123" not in payload


# ── Step 258: Generated Command Contract ────────────────────────────────────




class TestGeneratedCommandCatalogConsistency:
    def test_remedy_test_list_is_a_valid_command(self):
        """`remedy test list` became a real catalog command in Real Test Execution v1 (Step 1887):
        a read-only safe listing of test run records. It was previously a hallucination guard; now it
        is valid, so the assertion is inverted to require it to be a registered catalog command."""
        from apps.cli.command_catalog import CATALOG
        ids = {(c.group_id, c.subcommand) for c in CATALOG}
        assert ("test", "list") in ids, "remedy test list must be a registered catalog command"

    def test_permit_arg_order_correct(self):
        """remedy job permit order: <job_id> <permission> <action>."""
        from apps.cli.command_catalog import get_command
        cmd = get_command("job.permit")
        # Args should be: job_id, permission, action
        arg_names = [a.name for a in cmd.args]
        assert arg_names == ["job_id", "permission", "action"]

    def test_generated_commands_reference_catalog(self):
        """Generated guidance commands should use valid catalog entries."""
        from apps.cli.command_catalog import CATALOG
        valid_commands = {f"{c.group_id} {c.subcommand}" for c in CATALOG}

        # Check readiness next_actions
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        from packages.core.models import Job

        job = Job(name="test", user_prompt="test")
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
        from packages.core.models import Job

        job = Job(name="test", user_prompt="test")
        # Request level 4 (bounded_loop) but job has no signals → blocked
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=4)
        assert result.final_decision == "blocked"
        # Must be blocked for valid reason (readiness or active blockers)
        reason = result.cycles[0].reason.lower()
        assert "blocker" in reason or "readiness" in reason

    def test_levels_6_7_blocked(self):
        """Levels 6-7 must be blocked (future only)."""
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        from packages.core.models import Job

        job = Job(name="test", user_prompt="test")
        report = assess_job_readiness(job, [])
        assert report.levels[6].eligible is False
        assert report.levels[7].eligible is False
        assert "not_connected" in report.levels[6].blockers[0] or "not_implemented" in str(report.levels[6].blockers)


# ── Step 260: Mutation + Execution Safety Quick Wins ────────────────────────




class TestMutationExecutionSafetyInvariants:
    # Part A: source_apply permission boundary
    def test_source_apply_permission_denied(self):
        """source_apply blocks without repo_generated_write permission."""
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import StructuredPatch
        from packages.core.models import Job

        job = Job(name="test", user_prompt="test", metadata={"permissions": {}})
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

    def test_localhost_only(self):
        src = (ORCH / "ui_server.py").read_text()
        assert "127.0.0.1" in src




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

    def test_export_json(self):
        from packages.orchestration.git_status import (
            export_git_status_json,
            read_git_status,
        )

        status = read_git_status(".")
        data = export_git_status_json(status)
        assert data["version"] == 1
        assert data["is_git_repo"] is True
        assert isinstance(data["modified_files"], list)

    def test_summarize(self):
        from packages.orchestration.git_status import (
            read_git_status,
            summarize_git_status,
        )

        status = read_git_status(".")
        text = summarize_git_status(status)
        assert "Branch:" in text

    def test_no_shell_true(self):
        """Verify _run_git never uses shell=True."""
        import ast

        with open("packages/orchestration/git_status.py") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg == "shell":
                if isinstance(node.value, ast.Constant) and node.value.value is True:
                    pytest.fail("shell=True found in git_status.py")




class TestGitReadinessSignal:
    def test_signal_present(self):
        from packages.orchestration.autonomy_readiness import _collect_signals

        job = Job(
            id=uuid4(), name="sig-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        signals = _collect_signals(job, [])
        assert "git_status" in signals
        assert signals["git_status"] is False

    def test_signal_true_with_event(self):
        from packages.orchestration.autonomy_readiness import _collect_signals

        job = Job(
            id=uuid4(), name="sig-test", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        events = [{"event": "git_status_read", "metadata": {}}]
        signals = _collect_signals(job, events)
        assert signals["git_status"] is True




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

        job = Job(id=uuid4(), name="d1", user_prompt="test", metadata={})
        reasons = derive_stop_reasons(job, [])
        codes = [r.reason_code for r in reasons]
        assert "no_target_repo" in codes

    def test_derive_test_failed(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = Job(
            id=uuid4(), name="d2", user_prompt="test",
            metadata={"target_repo": "/tmp/repo"},
        )
        events = [
            {"event": "test_run_completed", "metadata": {"status": "failed"}},
        ]
        reasons = derive_stop_reasons(job, events)
        codes = [r.reason_code for r in reasons]
        assert "test_failed" in codes

    def test_derive_dirty_repo(self):
        from packages.orchestration.stop_reasons import derive_stop_reasons

        job = Job(
            id=uuid4(), name="d3", user_prompt="test",
            metadata={"target_repo": "/tmp/repo"},
        )
        events = [
            {"event": "git_status_read", "metadata": {"dirty": True}},
        ]
        reasons = derive_stop_reasons(job, events)
        codes = [r.reason_code for r in reasons]
        assert "dirty_repo_blocks_level" in codes




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
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop0", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        assert result.version == 1
        assert result.final_decision == "complete"
        assert result.autonomy_level == 0
        assert len(result.cycles) == 1
        assert result.cycles[0].decision == "complete"

    def test_level_1_needs_approval(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop1", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "needs_approval"

    def test_completed_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-done", user_prompt="test",
            tasks=[Task(description="t", status=RunState.COMPLETED)],
            state=RunState.COMPLETED,
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=3, autonomy_level=1)
        assert result.final_decision == "complete"

    def test_blocked_by_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-blocked", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={},  # No target_repo → blocker
        )
        save_job(job)
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
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-ex", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
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
        from packages.orchestration.storage import save_job

        job = Job(
            id=uuid4(), name="loop-sum", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
            metadata={"target_repo": "."},
        )
        save_job(job)
        result = run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        text = summarize_loop_result(result)
        assert "Autonomy Loop" in text
        assert "Level: 0" in text

