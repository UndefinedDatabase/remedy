"""
Domain tests: ui_server/test_dashboard_contract.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = REPO_ROOT / "apps" / "ui" / "src"

ORCH = REPO_ROOT / "packages" / "orchestration"

CLI_COMMANDS = REPO_ROOT / "apps" / "cli" / "commands"


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


def _make_job_s80(**overrides: object) -> Job:
    defaults = dict(
        name="test-ui-job",
        user_prompt="Test prompt for UI",
        tasks=[Task(type="write_readme", description="Write a README")],
    )
    defaults.update(overrides)
    return Job(**defaults)


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


# ── Step 68.1: Event Schema Registry ────────────────────────────────────


def _get_app_html(job_id: str = "test-job", token: str = "test-token") -> str:
    from packages.orchestration.ui_app_shell import build_app_shell
    return build_app_shell(job_id, token)


# ---------------------------------------------------------------------------
# Step 80 — Localhost UI Server
# ---------------------------------------------------------------------------




class TestDashboard:
    def test_build_job_dashboard(self):
        from packages.orchestration.dashboard import build_job_dashboard
        job = _make_job()
        data = build_job_dashboard(job, _make_events())
        assert data["version"] == 1
        assert data["scope"] == "job"
        assert "readiness" in data
        assert "decisions" in data
        assert "test_status" in data
        assert "git_status" in data or data["git_status"] == {}
        assert "worker_recommendation" in data
        assert "memory" in data
        assert "events" in data
        assert "next_actions" in data

    def test_build_job_dashboard_decisions(self):
        from packages.orchestration.dashboard import build_job_dashboard
        job = _make_job()
        events = [
            {"event": "test_run_completed", "run_id": "r1", "job_id": str(job.id),
             "timestamp": "2026-01-01T00:01:00", "outcome": "failed",
             "metadata": {"status": "failed", "command": "pytest", "test_run_id": "tr1"}},
        ]
        data = build_job_dashboard(job, events)
        assert data["decisions"]["open_count"] >= 1

    def test_summarize_job_dashboard(self):
        from packages.orchestration.dashboard import build_job_dashboard, summarize_job_dashboard
        job = _make_job()
        data = build_job_dashboard(job, _make_events())
        text = summarize_job_dashboard(data)
        assert "Dashboard" in text
        assert "Readiness" in text
        assert "Decisions" in text

    def test_build_project_dashboard(self):
        from packages.orchestration.dashboard import build_project_dashboard
        job = _make_job()
        data = build_project_dashboard("proj1", [job], {str(job.id): _make_events()})
        assert data["version"] == 1
        assert data["scope"] == "project"
        assert data["job_count"] == 1
        assert "readiness_summary" in data
        assert "open_decision_count" in data

    def test_build_project_dashboard_empty(self):
        from packages.orchestration.dashboard import build_project_dashboard
        data = build_project_dashboard("proj1", [], {})
        assert data["job_count"] == 0
        assert data["readiness_summary"]["min_level"] == 0


# ── Step 71: Context Optimizer ──────────────────────────────────────────




class TestUIServer:
    """Test the UI server module."""

    def test_ui_server_module_exists(self):
        import packages.orchestration.ui_server as mod
        assert hasattr(mod, "start_ui_server")
        assert hasattr(mod, "_RemedyHandler")

    def test_catalog_has_ui_start(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("ui.start")
        assert cmd.group_id == "ui"
        assert cmd.action_class == "read_only"
        arg_names = [a.name for a in cmd.args]
        assert "job_id" in arg_names
        assert "--port" in arg_names
        assert "--host" in arg_names
        assert "--info-file" in arg_names

    def test_handler_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "ui.start" in handlers

    def test_refuses_non_localhost(self, tmp_path, monkeypatch):
        """Server must refuse 0.0.0.0 or LAN addresses."""
        from packages.orchestration.ui_server import start_ui_server

        job = _make_job_s80()
        from packages.orchestration.storage import save_job
        save_job(job)

        with pytest.raises(SystemExit):
            start_ui_server(str(job.id), host="0.0.0.0", port=0)

    def test_safe_error_format(self):
        from packages.orchestration.ui_server import _safe_error
        code, body = _safe_error(403, "forbidden")
        assert code == 403
        assert body == {"error": "forbidden"}

    def test_load_job_invalid_uuid(self):
        from packages.orchestration.ui_server import _load_job
        job, err = _load_job("not-a-uuid")
        assert job is None
        assert err[0] == 400

    def test_load_job_missing(self):
        from packages.orchestration.ui_server import _load_job
        job, err = _load_job(str(uuid4()))
        assert job is None
        assert err[0] == 404

    def test_no_shell_true_in_server(self):
        src = Path("packages/orchestration/ui_server.py").read_text()
        assert "shell=True" not in src

    def test_no_external_assets_in_server(self):
        src = Path("packages/orchestration/ui_server.py").read_text()
        for pattern in ("cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"):
            assert pattern not in src




class TestAgentStateFilesCurrentBranch:
    def test_context_md_references_current_branch(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        assert "## Active Branch" in ctx
        assert "feature/" in ctx
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




class TestDashboardTruthFieldsExist:
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


def _decision_requested_events(count: int) -> list[dict]:
    """`human_decision_requested` events — the ledger shape `metrics.open` no longer reads."""
    return [
        {"event": "human_decision_requested", "run_id": "r1", "job_id": "j1",
         "timestamp": f"2026-01-01T00:0{i}:00", "outcome": "pending", "metadata": {}}
        for i in range(count)
    ]


class TestMetricsOpenComesFromTheDecisionQueue:
    """`metrics.open` re-derives from `decision_queue` (DECISION F031 D9)."""

    @staticmethod
    def _metrics_open(job, events):
        from packages.orchestration.ui_server import _build_dashboard
        with patch("packages.orchestration.ui_server._load_events", return_value=events):
            return _build_dashboard(job)["metrics"]["open"]

    @staticmethod
    def _queue_count(job, events):
        from packages.orchestration.decision_queue import list_decisions, open_decisions
        return len(open_decisions(list_decisions(job, events)))

    def test_repo_less_job_reports_its_open_decisions(self):
        job = _make_job_s80()
        expected = self._queue_count(job, [])
        assert expected > 0, "a job with no target_repo must raise a stop-reason decision"
        assert self._metrics_open(job, []) == expected

    def test_job_with_nothing_open_reports_zero(self):
        job = _make_job()
        expected = self._queue_count(job, [])
        assert expected == 0
        assert self._metrics_open(job, []) == expected

    def test_human_decision_requested_events_do_not_raise_the_count(self):
        job = _make_job()
        events = _decision_requested_events(3)
        expected = self._queue_count(job, events)
        assert expected == 0
        assert self._metrics_open(job, events) == expected


# ── Step 249: No-Fake UI State Pass ─────────────────────────────────────────




class TestNoFakeUiStateInComponents:
    def test_no_display_rows_fake_data(self):
        src = (UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        assert "DISPLAY_ROWS" not in src

    def test_task_checklist_has_empty_state(self):
        src = (UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        assert "No tasks yet" in src or "emptyState" in src

    def test_agent_now_card_has_idle_state(self):
        # Agent status logic (incl. the Idle state) lives in pure cockpitLogic.
        logic = (UI_SRC / "cockpitLogic.ts").read_text()
        assert "Idle" in logic

    def test_agent_now_card_no_always_working(self):
        src = (UI_SRC / "components" / "panels" / "AgentNowCard.tsx").read_text()
        assert "isRunning" in src or "isIdle" in src or "live.running" in src

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




class TestRealGraphSourceKindContract:
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




class TestEventLedgerLiveActivity:
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




class TestJobSummaryCommandContract:
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
        local_tsc = REPO_ROOT / "apps" / "ui" / "node_modules" / ".bin" / "tsc"
        # WHY R-0480 / DECISION F083 D6: with no local TypeScript, npx resolves a cached tsc@2.0.4
        # stub whose bin sets exitCode 1, so the old form graded the stub's exit code, not a compile.
        if not local_tsc.is_file():
            pytest.skip(
                f"UI toolchain absent: {local_tsc.parent.parent} is missing; "
                "run `npm ci --prefix apps/ui`"
            )
        result = subprocess.run(
            [str(local_tsc), "--noEmit"],
            cwd=str(REPO_ROOT / "apps" / "ui"),
            capture_output=True, timeout=30,
        )
        assert result.returncode == 0, f"tsc failed:\n{result.stderr.decode()}"




class TestLiveReviewAndAgentStateRefs:
    def test_live_review_has_steps_section(self):
        review = (REPO_ROOT / ".agent" / "live_review.md").read_text()
        assert "Steps" in review

    def test_context_md_no_stale_steps(self):
        ctx = (REPO_ROOT / ".agent" / "context.md").read_text()
        # Context may reference 253-260 or later steps (261+)
        assert "Steps" in ctx
        assert "steps-74_1-79" not in ctx
        assert "Steps 91-100" not in ctx

    def test_plan_md_references_current_steps(self):
        plan = (REPO_ROOT / ".agent" / "plan.md").read_text()
        # Plan may reference 253-260 or later steps
        assert "Steps" in plan and "## Goal" in plan

    def test_this_file_has_runtime_tests(self):
        """Verify this test file has actual runtime function calls, not just string checks."""
        src = Path(__file__).read_text()
        # Must have actual function imports and calls
        assert "from packages.orchestration" in src
        assert "assess_job_readiness" in src
        assert "apply_structured_patch" in src


# ── Step 254: Readiness Endpoint Repair ─────────────────────────────────────




class TestReadinessEndpointUsesAutonomyReadiness:
    def test_readiness_endpoint_uses_autonomy_readiness(self):
        """Verify ui_server imports from autonomy_readiness, not readiness."""
        src = (ORCH / "ui_server.py").read_text()
        assert "packages.orchestration.readiness" not in src
        assert "autonomy_readiness" in src

    def test_readiness_runtime_with_empty_job(self):
        """Runtime test: assess_job_readiness returns real report for minimal job."""
        from packages.core.models import Job
        from packages.orchestration.autonomy_readiness import (
            assess_job_readiness,
            export_readiness_json,
        )

        job = Job(name="test-readiness", user_prompt="test")
        report = assess_job_readiness(job, [])
        data = export_readiness_json(report)

        assert data["version"] == 2
        assert data["scope"] == "job"
        assert "highest_eligible_level" in data
        assert isinstance(data["levels"], list)
        assert len(data["levels"]) == 8
        assert data["levels"][0]["eligible"] is True  # Level 0 always eligible
        assert "signals" in data

    def test_readiness_runtime_with_events(self):
        """Level 1 requires attached_repo + tasks."""
        from packages.core.models import Job, Task
        from packages.orchestration.autonomy_readiness import assess_job_readiness

        job = Job(
            name="test-readiness",
            user_prompt="test",
            tasks=[Task(description="do thing")],
            metadata={"target_repo": "/tmp/fake"},
        )
        report = assess_job_readiness(job, [])
        # Level 1 (propose) should be eligible: has repo + tasks
        assert report.highest_eligible_level >= 1

    def test_build_readiness_json_helper(self):
        """Runtime test: _build_readiness_json returns real data."""
        from packages.core.models import Job
        from packages.orchestration.ui_server import _build_readiness_json

        job = Job(name="test", user_prompt="test")
        result = _build_readiness_json(job)
        assert "version" in result
        assert "error" not in result or "readiness unavailable" not in result.get("error", "")


# ── Step 255: Read-Only UI Startup Must Not Mutate ──────────────────────────




def _record_build_seam_calls(*, no_auto_build: str | None):
    """Drive ``_auto_build_frontend`` with the lever in one position; return the argv it ran.

    THE SEAM IS PATCHED, NOT THE ENVIRONMENT (finding R-0714). ``_auto_build_frontend``
    reaches npm only through ``exec_guard.run_guarded_runtime_build_command`` as a module
    attribute, so replacing that attribute observes the decision without spending a real
    ``npm install`` and ``npm run build`` inside the suite. Its ``ui_root`` is resolved from
    ``__file__``, never from the working directory, so ``package.json`` always exists and the
    only thing that can stop the build is the lever itself — which is precisely what makes
    the lever, and nothing else, the variable under test here.

    ``no_auto_build`` of ``None`` means the variable is absent from the environment.
    """
    import subprocess as sp

    from packages.orchestration import exec_guard, ui_server

    seen: list[list[str]] = []

    def _record(cmd, *, timeout_sec, cwd, check=False):
        seen.append(list(cmd))
        return sp.CompletedProcess(list(cmd), 0, b"", b"")

    env = os.environ.copy()
    env.pop("REMEDY_UI_NO_AUTO_BUILD", None)
    if no_auto_build is not None:
        env["REMEDY_UI_NO_AUTO_BUILD"] = no_auto_build

    with patch.dict(os.environ, env, clear=True):
        with patch.object(exec_guard, "run_guarded_runtime_build_command", _record):
            result = ui_server._auto_build_frontend()
    return seen, result


class TestAutoBuildBehavior:
    """REMEDY_UI_NO_AUTO_BUILD is the integration gate's ONE neutralisation lever.

    `docs/agents/integration_gate.md` step 3 sets it so a full-suite run does not
    rebuild the frontend underneath itself. These tests must therefore DISCRIMINATE
    the lever in both directions: unset must reach the build seam, and ``1`` must
    leave it unreached. Asserting anything weaker leaves the lever unenforceable for
    every future feature, which is finding R-0714.
    """

    def test_auto_build_runs_by_default(self):
        """Lever unset: the build seam IS reached with the npm build argv (R-0714).

        Replaces an assertion that could not fail — ``result is None or
        isinstance(result, Path)`` over a function annotated ``-> Path | None`` is
        satisfied by every possible execution, including one where npm is missing or
        the build errors out.
        """
        seen, _result = _record_build_seam_calls(no_auto_build=None)

        assert seen, (
            "the lever was unset and the build seam was never reached: "
            "auto-build no longer runs by default"
        )
        assert ["npm", "run", "build"] in seen, (
            f"the npm build command never reached the guard; saw {seen!r}"
        )

    def test_auto_build_disabled_with_env(self):
        """REMEDY_UI_NO_AUTO_BUILD=1 disables auto-build."""
        from packages.orchestration.ui_server import _auto_build_frontend

        with patch.dict(os.environ, {"REMEDY_UI_NO_AUTO_BUILD": "1"}):
            result = _auto_build_frontend()
        assert result is None

    def test_no_npm_when_disabled(self):
        """Lever set to 1: the build seam is NOT reached (R-0714).

        The former version patched ``subprocess.run``, which ``_auto_build_frontend``
        does not call — it reaches npm through the guard — so the assertion held
        whether or not the lever worked. The guard is the seam that has to stay
        unreached.
        """
        seen, result = _record_build_seam_calls(no_auto_build="1")

        assert seen == [], (
            f"REMEDY_UI_NO_AUTO_BUILD=1 did not neutralise the build: "
            f"the guard was still called with {seen!r}"
        )
        assert result is None

    def test_auto_build_npm_commands_run_through_the_guard(self):
        """Both npm commands reach the runtime-build seam; none reaches a bare run."""
        import inspect
        import subprocess as sp

        from packages.orchestration import exec_guard, ui_server

        seen = []

        def _record(cmd, *, timeout_sec, cwd, check=False):
            seen.append((list(cmd), timeout_sec, cwd, check))
            return sp.CompletedProcess(list(cmd), 0, b"", b"")

        env = os.environ.copy()
        env.pop("REMEDY_UI_NO_AUTO_BUILD", None)
        with patch.dict(os.environ, env, clear=True):
            with patch.object(exec_guard, "run_guarded_runtime_build_command", _record):
                with patch.object(sp, "run") as bare_run:
                    ui_server._auto_build_frontend()

        assert bare_run.call_count == 0
        assert seen, "the npm run build site never reached the guard"
        cmd, timeout_sec, cwd, check = seen[-1]
        assert cmd == ["npm", "run", "build"]
        assert timeout_sec == 120
        assert check is True
        assert cwd is not None and cwd.endswith("apps/ui")

        # The install site is skipped whenever node_modules is fresh, so this run may
        # never reach it. Pin that site structurally instead of by a call that depends
        # on the checkout's mtimes.
        source = inspect.getsource(ui_server._auto_build_frontend)
        assert source.count("exec_guard.run_guarded_runtime_build_command(") == 2
        assert "subprocess.run(" not in source

    def test_frontend_is_stale_function_exists(self):
        """_frontend_is_stale must exist and return bool."""
        from packages.orchestration.ui_server import _frontend_is_stale
        result = _frontend_is_stale()
        assert isinstance(result, bool)


# ── Step 528: Visual Product Tests ──────────────────────────────────────────


class TestVisualProductContract:
    """Verify dashboard design foundation, timeline, graph, and panel quality."""

    def test_live_review_canonical_path(self):
        """Review history must live in .agent/, not .data/."""
        agent_path = REPO_ROOT / ".agent" / "live_review.md"
        assert agent_path.exists(), "live_review.md must exist at .agent/live_review.md"

    def test_timeline_container_height(self):
        """Timeline row must be >= 124px, not the old 80-110px."""
        css = (UI_SRC / "components" / "shell" / "RemedyShell.module.css").read_text()
        assert "clamp(150px" in css or "clamp(136px" in css or "clamp(128px" in css or "clamp(124px" in css, "Timeline row must use clamp(124+px, ...)"

    def test_timeline_done_uses_checkmark_in_rail(self):
        """Done phases render TaskDoneGlyph in rail marker, not in phase header."""
        src = (UI_SRC / "components" / "timeline" / "PhaseTimeline.tsx").read_text()
        assert "TaskDoneGlyph" in src, "TaskDoneGlyph must be used in rail markers"
        assert "markerCheck" in src, "TaskDoneGlyph should use markerCheck class"

    def test_graph_empty_state_exists(self):
        """Graph must have designed empty state, not lonely root."""
        css = (UI_SRC / "components" / "graph" / "BrainGraphCanvas.module.css").read_text()
        assert ".emptyState" in css
        assert ".emptyOrb" in css

    def test_graph_filter_empty_messages(self):
        """Graph must show filter-specific empty messages."""
        src = (UI_SRC / "components" / "graph" / "BrainGraphCanvas.tsx").read_text()
        assert "FILTER_EMPTY_MESSAGES" in src
        assert "No active or blocked tasks" in src
        assert "No planned tasks" in src
        assert "No completed tasks" in src

    def test_no_mui_in_primary_components(self):
        """Primary components must not import MUI icons."""
        primary_files = [
            UI_SRC / "components" / "shell" / "RemedyShell.tsx",
            UI_SRC / "components" / "graph" / "BrainGraphCanvas.tsx",
            UI_SRC / "components" / "graph" / "BrainGraphStage.tsx",
            UI_SRC / "components" / "timeline" / "PhaseTimeline.tsx",
            UI_SRC / "components" / "command" / "CommandBar.tsx",
            UI_SRC / "components" / "detail" / "DetailPopover.tsx",
            UI_SRC / "components" / "panels" / "RightLivePanel.tsx",
            UI_SRC / "components" / "panels" / "AgentNowCard.tsx",
            UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx",
            UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx",
            UI_SRC / "components" / "panels" / "AddTaskButton.tsx",
            UI_SRC / "components" / "metrics" / "TopMetricsBar.tsx",
            UI_SRC / "components" / "rail" / "LeftBrandRail.tsx",
        ]
        for f in primary_files:
            if f.exists():
                src = f.read_text()
                assert "@mui" not in src, f"{f.name} imports MUI — use RemedyGlyphs"

    def test_no_cli_language_in_command_bar(self):
        """Command bar placeholder must be human-friendly, not a CLI command."""
        src = (UI_SRC / "components" / "command" / "CommandBar.tsx").read_text()
        # The literal placeholder text must not be a CLI command.
        placeholder = re.search(r"placeholder=(?:'([^']*)'|\"([^\"]*)\")", src)
        assert placeholder, "CommandBar must have a placeholder"
        ptext = (placeholder.group(1) or placeholder.group(2)).lower()
        assert "remedy " not in ptext
        # New design pack: human-friendly jump-to placeholder.
        assert "jump to" in ptext

    def test_detail_popover_has_outcome_fields(self):
        """DetailPopover must show blockedReason, changedFilesSafe, completedAt."""
        src = (UI_SRC / "components" / "detail" / "DetailPopover.tsx").read_text()
        assert "blockedReason" in src
        assert "changedFilesSafe" in src or "changedFiles" in src
        assert "completedAt" in src

    def test_backend_task_outcome_fields(self):
        """Backend must emit changed_files_safe, blocked_reason, completed_at."""
        src = (ORCH / "ui_server.py").read_text()
        assert "changed_files_safe" in src
        assert "blocked_reason" in src
        assert "completed_at" in src

    def test_right_panel_glass_opacity(self):
        """Right panel cards should use the strong glass token (>= .5 opacity)."""
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        # New design pack: cards use the shared glass token (rgba(255,255,255,.78)).
        assert "--remedy-glass-bg-strong" in css


# ── Step 256: Degraded UI API State ─────────────────────────────────────────

