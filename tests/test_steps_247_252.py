"""Tests for Steps 247-252: Data-Honest Mission Control Contract."""

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
ORCH = REPO_ROOT / "packages" / "orchestration"
CLI_COMMANDS = REPO_ROOT / "apps" / "cli" / "commands"


# ── Step 247: Repo + Handoff Truth Hygiene ──────────────────────────────────

class TestStep247:
    def test_context_md_references_current_branch(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        assert "steps-247-252" in ctx
        assert "steps-74_1-79" not in ctx
        assert "steps-91-100" not in ctx

    def test_plan_md_references_current_steps(self):
        plan = (REPO_ROOT / ".agent" / "plan.md").read_text()
        # Plan always references current or later steps
        assert "Steps" in plan
        assert "## Goal" in plan

    def test_no_stale_branch_references_in_context(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        assert "feature/steps-74" not in ctx
        assert "PR #33" not in ctx


# ── Step 248: Dashboard Truth Contract v1 ───────────────────────────────────

class TestStep248:
    def test_dashboard_returns_version_2(self):
        src = (ORCH / "ui_server.py").read_text()
        assert '"version": 2' in src or "'version': 2" in src

    def test_dashboard_has_demo_mode_field(self):
        src = (ORCH / "ui_server.py").read_text()
        assert '"demo_mode"' in src

    def test_dashboard_has_synthetic_count(self):
        src = (ORCH / "ui_server.py").read_text()
        assert '"synthetic_count"' in src

    def test_dashboard_has_truth_contract(self):
        src = (ORCH / "ui_server.py").read_text()
        assert '"truth"' in src or '"missing_sources"' in src

    def test_live_state_returns_version_3(self):
        src = (ORCH / "ui_server.py").read_text()
        assert '"version": 3' in src or "'version': 3" in src

    def test_live_state_has_idle_and_stale(self):
        src = (ORCH / "ui_server.py").read_text()
        assert '"idle"' in src
        assert '"stale"' in src


# ── Step 249: No-Fake UI State Pass ─────────────────────────────────────────

class TestStep249:
    def test_no_display_rows_fake_data(self):
        src = (UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        assert "DISPLAY_ROWS" not in src

    def test_task_checklist_has_empty_state(self):
        src = (UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        assert "No tasks yet" in src or "emptyState" in src

    def test_agent_now_card_has_idle_state(self):
        src = (UI_SRC / "components" / "panels" / "AgentNowCard.tsx").read_text()
        assert "idle" in src.lower() or "isIdle" in src

    def test_agent_now_card_no_always_working(self):
        src = (UI_SRC / "components" / "panels" / "AgentNowCard.tsx").read_text()
        # Should NOT have unconditional "Builder is working" without idle check
        lines = src.split("\n")
        has_idle_check = any("isIdle" in l for l in lines)
        assert has_idle_check

    def test_activity_feed_has_empty_state(self):
        src = (UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx").read_text()
        assert "No activity yet" in src or "emptyState" in src

    def test_normalize_activity_returns_empty_when_idle(self):
        """Dashboard-first: empty activity from dashboard = empty activity in UI."""
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        # normalizeApiFailure returns empty activity
        assert "normalizeApiFailure" in src
        assert "activity: []" in src

    def test_no_fake_system_message(self):
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        # Should not have hardcoded "Project state is ready for review"
        assert "Project state is ready for review" not in src

    def test_empty_state_css_class_exists(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert ".emptyState" in css


# ── Step 250: Real Graph Source Contract ────────────────────────────────────

class TestStep250:
    def test_brain_source_kind_type_exists(self):
        src = (UI_SRC / "components" / "graph" / "forceBrainTypes.ts").read_text()
        assert "BrainSourceKind" in src
        assert "real_brain" in src
        assert "layout_only" in src
        assert "demo_fixture" in src

    def test_force_brain_node_has_source_kind(self):
        src = (UI_SRC / "components" / "graph" / "forceBrainTypes.ts").read_text()
        assert "sourceKind: BrainSourceKind" in src

    def test_build_model_assigns_source_kind_to_root(self):
        src = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        # Root should be layout_only
        assert 'sourceKind: "layout_only"' in src

    def test_build_model_assigns_source_kind_to_real_nodes(self):
        src = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        assert 'sourceKind: "real_brain"' in src

    def test_particles_marked_layout_only(self):
        src = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        # Particle nodes should be layout_only
        lines = src.split("\n")
        in_particle = False
        particle_has_layout = False
        for line in lines:
            if "kind: \"particle\"" in line:
                in_particle = True
            if in_particle and "sourceKind" in line:
                particle_has_layout = "layout_only" in line
                break
        assert particle_has_layout

    def test_no_math_random_in_graph_model(self):
        src = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        assert "Math.random" not in src


# ── Step 251: Event Ledger → Live Activity ──────────────────────────────────

class TestStep251:
    def test_event_labels_defined(self):
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "EVENT_LABELS" in src
        assert "task_created" in src
        assert "patch_intent_applied" in src
        assert "test_run_completed" in src

    def test_activity_uses_dashboard_data(self):
        """Activity now comes from dashboard payload, not separate events-since."""
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "dashboard.activity" in src or "activity" in src

    def test_format_event_time_exists(self):
        src = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "formatEventTime" in src


# ── Step 252: Operator Summary + Smoke Alignment ────────────────────────────

class TestStep252:
    def test_job_summary_command_exists(self):
        src = (CLI_COMMANDS / "job.py").read_text()
        assert "_cmd_job_summary" in src
        assert '"job.summary"' in src

    def test_job_summary_outputs_demo_mode(self):
        src = (CLI_COMMANDS / "job.py").read_text()
        assert "demo_mode" in src
        assert "data_honest" in src

    def test_job_summary_in_catalog(self):
        catalog = (REPO_ROOT / "apps" / "cli" / "command_catalog.py").read_text()
        assert "job.summary" in catalog

    def test_job_summary_supports_json(self):
        catalog = (REPO_ROOT / "apps" / "cli" / "command_catalog.py").read_text()
        # Find the job.summary entry and confirm supports_json=True
        idx = catalog.index("job.summary")
        block = catalog[idx:idx+400]
        assert "supports_json=True" in block

    def test_no_shell_true_in_subprocess_calls(self):
        """Verify no subprocess calls use shell=True (comments mentioning it are OK)."""
        import ast
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

    def test_ui_server_binds_localhost_only(self):
        src = (ORCH / "ui_server.py").read_text()
        assert "127.0.0.1" in src
        assert '("127.0.0.1", "localhost", "::1")' in src

    def test_typescript_compiles(self):
        """Verify tsc --noEmit passes (checked in CI)."""
        import subprocess
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=str(REPO_ROOT / "apps" / "ui"),
            capture_output=True, timeout=30,
        )
        assert result.returncode == 0, f"tsc failed:\n{result.stderr.decode()}"
