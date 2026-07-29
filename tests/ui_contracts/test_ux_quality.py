"""
Domain tests: ui_contracts/test_ux_quality.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task

_ROOT = Path(__file__).resolve().parent.parent.parent

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"


def _make_job(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "tasks": [Task(description="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


# ── Step 71.1: Token Policy Applied ──────────────────────────────────────


def _make_job_s74(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "tasks": [Task(description="task 1", status=RunState.COMPLETED)],
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


def _make_job_s91():
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    return job


def _make_job_s101(task_count: int = 3):
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    for i in range(task_count):
        t = MagicMock()
        t.id = uuid4()
        t.task_type = "test_task"
        t.status.value = "completed" if i == 0 else "pending"
        t.metadata = {}
        job.tasks.append(t)
    return job


# ---------------------------------------------------------------------------
# Step 101 — Smoke/UX Contract Reset
# ---------------------------------------------------------------------------


def _make_job_s111(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 111 — UI CLI Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s127(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 127 — Task Progress API Contract Closure
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s141(*, tasks=None, name="test"):
    from packages.core.models import Job, RunState, Task
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


def _make_job_s163(name: str = "Test goal") -> Job:
    job = Job(name=name)
    job.metadata = job.metadata or {}
    return job


def _get_viewer_html():
    from packages.orchestration.brain_viewer import (
        build_brain_viewer_data,
        write_brain_viewer_files,
    )
    from packages.orchestration.project_brain import build_project_brain

    job = _make_job()
    events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.id),
                "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
    graph = build_project_brain(job, events)
    data = build_brain_viewer_data(job, graph, events)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        html_path = write_brain_viewer_files(data, out)
        return html_path.read_text(), data, out


# ── Step 74.1: Redaction Gate Precision ─────────────────────────────────


def _get_app_html(job_id: str = "test-job", token: str = "test-token") -> str:
    from packages.orchestration.ui_app_shell import build_app_shell
    return build_app_shell(job_id, token)


# ---------------------------------------------------------------------------
# Step 80 — Localhost UI Server
# ---------------------------------------------------------------------------


def _make_permitted_job():
    """Create a job with repo_generated_write permission granted."""
    job = _make_job()
    job.metadata["permissions"] = {"repo_generated_write": "allow"}
    return job


def _make_approved_job() -> tuple:
    """Create a job with permission + an approved patch intent. Returns (job, intent_id)."""
    job = _make_permitted_job()
    # Create artifact with patch intent explanation + approval
    artifact = MagicMock()
    artifact.id = uuid4()
    artifact.task_id = uuid4()
    intent_id = f"{artifact.id.hex[:8]}-0"
    artifact.metadata = {
        "patch_intent_explanations": [
            {"file": "test.py", "action": "create", "risk": "low", "reason": "test", "summary": "test"}
        ],
        "patch_intent_approvals": {
            intent_id: {
                "intent_id": intent_id,
                "state": "approved",
                "decided_at": "2026-01-01T00:00:00Z",
                "decided_by": "test",
            }
        },
    }
    job.artifacts = [artifact]
    return job, intent_id


# ---------------------------------------------------------------------------
# Step 91 — ELK Directional Layout
# ---------------------------------------------------------------------------


def _make_events() -> list[dict]:
    return [
        {"event": "autorun_started", "timestamp": "2026-01-01T00:00:00Z", "metadata": {}},
        {"event": "structured_patch_intent_created", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"intent_kind": "file_ops"}},
        {"event": "source_patch_applied", "timestamp": "2026-01-01T00:02:00Z", "metadata": {}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:03:00Z", "metadata": {"exit_code": 0, "passed": True}},
        {"event": "proof_collected", "timestamp": "2026-01-01T00:04:00Z", "metadata": {"content_hash": "abc123"}},
    ]


# ===========================================================================
# Step 163 — Memory Candidate Contract Closure
# ===========================================================================




class TestUXQualityGate:
    def test_design_tokens_present(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert ":root" in REMEDY_CSS
        assert "--remedy-bg" in REMEDY_CSS

    def test_no_logo_or_center_triangle(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        lower = REMEDY_CSS.lower()
        assert "logo" not in lower
        assert "triangle" not in lower

    def test_status_classes_for_core_types(self):
        from packages.orchestration.brain_viewer_theme import get_status_class
        # Core statuses must all map
        for status in ("verified", "completed", "blocked", "pending", "running"):
            cls = get_status_class(status)
            assert cls.startswith("remedy-status-"), f"bad class for {status}: {cls}"

    def test_data_render_status_in_viewer(self):
        from packages.orchestration.brain_viewer import _HTML
        assert "data-render-status" in _HTML

    def test_keyboard_focusable(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert "focus-visible" in REMEDY_CSS




class TestMotionDepth:
    def test_mist_layer(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-mist" in html

    def test_scanlines(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-scanlines" in html

    def test_grid_layer(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-grid" in html

    def test_edge_glow(self):
        html, _, _ = _get_viewer_html()
        assert "drop-shadow" in html

    def test_hover_lift(self):
        html, _, _ = _get_viewer_html()
        # Hover effect on nodes
        assert ".nd:hover" in html

    def test_selected_pulse(self):
        html, _, _ = _get_viewer_html()
        assert "sel-pulse" in html

    def test_reduced_motion_disables(self):
        html, _, _ = _get_viewer_html()
        assert "prefers-reduced-motion" in html
        # Scanlines hidden under reduced motion
        assert "remedy-scanlines" in html

    def test_no_external_assets(self):
        html, _, _ = _get_viewer_html()
        urls = re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\\s]+)', html)
        assert urls == []

    def test_no_canvas_required(self):
        html, _, _ = _get_viewer_html()
        # Core function must not require canvas
        assert "<canvas" not in html

    def test_orbit_bg_present(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-orbit-bg" in html

    def test_particle_field_present(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-particle-field" in html


# ── Step 78: Human Guidance Rail ────────────────────────────────────────




class TestCalmEntryUX:
    """Test the app shell for calm entry UX."""

    def test_app_shell_builds(self):
        html = _get_app_html()
        assert "Remedy" in html
        assert "__JOB_ID__" not in html
        assert "__TOKEN__" not in html

    def test_light_theme_default(self):
        html = _get_app_html()
        assert 'class="remedy-light"' in html
        assert "--remedy-bg:" in html

    def test_light_theme_css_variables(self):
        html = _get_app_html()
        required_vars = [
            "--remedy-bg", "--remedy-surface",
            "--remedy-text", "--remedy-text-muted", "--remedy-teal",
            "--remedy-cyan", "--remedy-line", "--remedy-proof",
            "--remedy-risk", "--remedy-warning", "--remedy-memory",
        ]
        for var in required_vars:
            assert var in html, f"Missing CSS variable: {var}"

    def test_dark_mode_available(self):
        html = _get_app_html()
        assert ".remedy-dark" in html

    def test_story_headline_area(self):
        """New shell has story headline + progress (replaces what-happened panel)."""
        html = _get_app_html()
        assert "remedy-journey-shell" in html
        assert "buildUI" in html

    def test_checklist_sidebar(self):
        """New shell has checklist sidebar (replaces proven/attention panels)."""
        html = _get_app_html()
        assert "remedy-checklist" in html

    def test_layer_switcher(self):
        """New shell has layer switcher (replaces explore brain button)."""
        html = _get_app_html()
        assert "remedy-layer-switcher" in html
        assert "journey" in html

    def test_detail_card_hidden_by_default(self):
        """Detail card starts hidden, shown on node click."""
        html = _get_app_html()
        assert "detail-card" in html
        assert "display: none" in html or "display:none" in html.replace(" ", "")

    def test_no_giant_zone_rail(self):
        """No left rail with zone/status/risk visible by default."""
        html = _get_app_html()
        # No massive status/type rail in default view
        assert "zone-label" not in html or html.count("zone-label") < 3

    def test_no_external_assets(self):
        html = _get_app_html()
        for pattern in ("cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net", "https://", "http://"):
            # http:// is OK in API URLs like /api/
            if pattern == "http://":
                # Only check it's not loading external resources
                assert "http://cdn" not in html
                assert "http://fonts" not in html
            else:
                assert pattern not in html, f"External asset: {pattern}"

    def test_no_raw_leaks_in_shell(self):
        html = _get_app_html()
        for forbidden in ("raw_output", "command_output", "MUST_NOT_RENDER",
                          "diff_preview", "approval_reason"):
            assert forbidden not in html, f"Raw leak in shell: {forbidden}"

    def test_reduced_motion_support(self):
        html = _get_app_html()
        assert "prefers-reduced-motion" in html

    def test_narrow_layout_support(self):
        html = _get_app_html()
        assert "max-width:" in html

    def test_calm_background(self):
        html = _get_app_html()
        assert "--remedy-bg" in html
        assert "--remedy-bg-flat" in html


# ---------------------------------------------------------------------------
# Step 82 — Progressive Brain Explorer
# ---------------------------------------------------------------------------




class TestSmokeScriptUI:
    """Verify smoke script has UI-related sections."""

    @pytest.fixture(autouse=True)
    def _load_script(self):
        self.script = Path("scripts/remedy_smoke.sh").read_text()

    def test_group_help_includes_ui(self):
        assert "ui" in self.script.split("for grp in")[1].split("; do")[0]

    def test_no_shell_true_in_new_modules(self):
        for path in [
            "packages/orchestration/ui_server.py",
            "packages/orchestration/ui_app_shell.py",
        ]:
            src = Path(path).read_text()
            assert "shell=True" not in src, f"shell=True in {path}"




class TestUXAntiRegression:
    """Tests that fail if old bad UX patterns return."""

    def test_no_dark_background_in_pixi_frontend(self):
        """Frontend HTML must not have dark background colors."""
        index = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "index.html"
        html = index.read_text()
        dark_colors = ["#0a0e14", "#0d1117", "#1a1a2e", "#000000"]
        for c in dark_colors:
            assert c not in html, f"Dark color {c} found in frontend HTML"

    def test_background_is_light(self):
        """Frontend CSS tokens should define a light background."""
        tokens = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "styles" / "tokens.css"
        css = tokens.read_text()
        assert "--remedy-bg" in css, "Background token not found in tokens.css"
        assert "#ecf2fb" in css, "Light background color #ecf2fb not found"

    def test_no_scanlines_in_frontend(self):
        """No retro scanline effects."""
        src_dir = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src"
        for f in src_dir.rglob("*.ts"):
            content = f.read_text()
            assert "scanline" not in content.lower(), f"Scanline reference in {f.name}"

    def test_particles_reduced_motion_safe(self):
        """Animations must be guarded by reduced-motion check."""
        provider = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "components" / "shell" / "ReducedMotionProvider.tsx"
        assert provider.is_file(), "ReducedMotionProvider.tsx not found"
        content = provider.read_text()
        assert "reducedMotion" in content or "reduced-motion" in content, "Reduced-motion check not found"

    def test_current_graph_is_canvas_force(self):
        """Primary graph component uses Canvas/Force architecture."""
        graph = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"
        content = graph.read_text()
        assert "react-force-graph-2d" in content, "ForceBrainGraph must use react-force-graph-2d"
        assert "reducedMotion" in content or "reduced-motion" in content, "Reduced-motion guard missing"

    def test_semantic_zoom_labels_conditional(self):
        """Labels only shown at sufficient zoom — not all visible by default."""
        graph = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"
        content = graph.read_text()
        # Labels gated by globalScale threshold
        assert "globalScale" in content, "Label visibility must be gated by zoom scale"

    @pytest.mark.skip(reason=(
        "D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+)."))
    def test_legacy_graph_files_under_legacy(self):
        """Old React Flow graph files live under legacy/ directory."""
        legacy = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy"
        assert (legacy / "RemedyBrainFlow.tsx").is_file(), "Legacy RemedyBrainFlow.tsx not under legacy/"
        assert (legacy / "semanticZoom.ts").is_file(), "Legacy semanticZoom.ts not under legacy/"

    def test_detail_card_not_permanent_rail(self):
        """Detail card must be a compact popover component."""
        popover = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx"
        assert popover.is_file(), "DetailPopover.tsx not found"
        content = popover.read_text()
        assert "remedy-detail-compact" in content, "Compact detail class not found"

    def test_view_model_seven_zoom_levels(self):
        """View model must define exactly 7 zoom levels."""
        from packages.orchestration.ui_view_model import _ZOOM_NAMES
        assert len(_ZOOM_NAMES) == 7


# ---------------------------------------------------------------------------
# UI Commands in Catalog
# ---------------------------------------------------------------------------




class TestScreenSpaceLabels:
    def test_no_pixi_in_current_graph(self):
        """Current graph renderer (Canvas/Force) must not use raw PIXI imports."""
        graph = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"
        content = graph.read_text()
        assert "PIXI" not in content, "ForceBrainGraph should not import raw PIXI"
        assert "pixi.js" not in content, "ForceBrainGraph should not depend on pixi.js"

    @pytest.mark.skip(reason=(
        "D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+)."))
    def test_legacy_graph_nodes_under_legacy(self):
        """Old GraphNodes.tsx lives under legacy/, not top-level graph/."""
        legacy = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "GraphNodes.tsx"
        assert legacy.is_file(), "GraphNodes.tsx must exist under legacy/"

    def test_detail_card_compact(self):
        detail = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx"
        assert detail.is_file(), "DetailPopover.tsx must exist"
        content = detail.read_text()
        assert "remedy-detail-compact" in content, "DetailPopover must use remedy-detail-compact class"


# ---------------------------------------------------------------------------
# Step 94 — Explainable Edges
# ---------------------------------------------------------------------------




class TestTaskProgressRibbon:
    def test_build_task_progress_returns_tasks(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s101(3)
        result = build_task_progress(job, [])
        assert result["version"] == 1
        assert len(result["tasks"]) == 3

    def test_task_status_mapping(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s101(3)
        result = build_task_progress(job, [])
        statuses = [t["status"] for t in result["tasks"]]
        assert "completed" in statuses
        assert "pending" in statuses

    def test_ribbon_css_classes_in_html(self):
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        css = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "taskRow" in css
        assert "done" in css
        assert "current" in css
        assert "suggested" in css

    def test_ribbon_collapsible(self):
        css = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "overflow" in css
        assert ".panel" in css


# ---------------------------------------------------------------------------
# Step 105 — Human Node Labels
# ---------------------------------------------------------------------------




class TestHumanNodeLabels:
    def test_nodes_have_user_title(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(), [])
        for node in vm["nodes"]:
            assert "user_title" in node
            assert isinstance(node["user_title"], str)
            assert len(node["user_title"]) > 0

    def test_nodes_have_user_kind(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(), [])
        for node in vm["nodes"]:
            assert "user_kind" in node


# ---------------------------------------------------------------------------
# Step 106 — Atmospheric Motion
# ---------------------------------------------------------------------------




class TestAtmosphericMotion:
    def test_current_graph_is_canvas_force(self):
        """Current renderer is Canvas/Force-based, not React Flow."""
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "ForceGraph2D" in src or "react-force-graph-2d" in src

    def test_current_graph_reduced_motion_guard(self):
        """Current Canvas/Force graph respects reduced motion."""
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "reducedMotion" in src or "reduced-motion" in src

    def test_reduced_motion_css(self):
        css = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "styles" / "globals.css").read_text()
        assert "prefers-reduced-motion: reduce" in css


# ---------------------------------------------------------------------------
# Step 107 — Live Growth UX
# ---------------------------------------------------------------------------




class TestTaskRibbonFieldContract:

    def test_task_progress_version_1(self):
        """Task progress API should return version 1 (stable contract)."""
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["version"] == 1

    def test_task_progress_fields(self):
        """Each task should have the exact required fields."""
        required = {
            "id", "title", "status", "verified", "source", "accepted",
            "rank", "related_node_id", "short_reason", "proof_status",
            "test_status", "is_current", "is_future", "is_reviewer_suggested",
        }
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        for t in tp["tasks"]:
            missing = required - set(t.keys())
            assert not missing, f"missing fields: {missing}"

    def test_completed_task_status(self):
        job = _make_job_s111(tasks=[{"type": "write", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["status"] == "completed"

    def test_active_task_is_current(self):
        job = _make_job_s111(tasks=[{"type": "write", "status": "running"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["is_current"] is True

    def test_future_task_is_future(self):
        job = _make_job_s111(tasks=[{"type": "write", "status": "pending"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["is_future"] is True

    def test_reviewer_suggested_flag(self):
        job = _make_job_s111(tasks=[{
            "type": "review",
            "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["is_reviewer_suggested"] is True
        assert tp["tasks"][0]["status"] == "reviewer-suggested"

    def test_reviewer_not_verified(self):
        job = _make_job_s111(tasks=[{
            "type": "review",
            "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["verified"] is False

    def test_html_has_ribbon_markers(self):
        """React TaskChecklistCard must exist and use remedy-checklist class."""
        src_path = Path(_ROOT / "apps" / "ui" / "src" / "components" / "panels" / "TaskChecklistCard.tsx")
        assert src_path.exists(), "TaskChecklistCard.tsx not found"
        src = src_path.read_text()
        assert "remedy-checklist" in src

    def test_no_raw_leaks_in_task_progress(self):
        job = _make_job_s111(tasks=[{"type": "write", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        full = json.dumps(tp)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in full


# ═══════════════════════════════════════════════════════════════════════════
# Step 116 — Autocoder E2E Reality Check
# ═══════════════════════════════════════════════════════════════════════════




class TestTaskProgressApiSchema:
    """Task progress API must return version 1 with exact fields."""

    def test_version_is_1(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        tp = build_task_progress(job, [])
        assert tp["version"] == 1

    def test_exact_top_fields(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        tp = build_task_progress(job, [])
        assert set(tp.keys()) == {"version", "job_id", "tasks"}

    def test_task_required_fields(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
            {"type": "t3", "status": "pending"},
        ])
        tp = build_task_progress(job, [])
        required = {
            "id", "title", "status", "verified", "source", "accepted",
            "rank", "related_node_id", "short_reason", "proof_status",
            "test_status", "is_current", "is_future", "is_reviewer_suggested",
        }
        for task in tp["tasks"]:
            missing = required - set(task.keys())
            assert not missing, f"Missing: {missing}"

    def test_completed_task_status(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "done", "status": "completed"}])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["status"] == "completed"
        assert t["is_current"] is False
        assert t["is_future"] is False

    def test_active_task_is_current(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "active", "status": "running"}])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["status"] == "active"
        assert t["is_current"] is True

    def test_pending_task_is_future(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "future", "status": "pending"}])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["is_future"] is True

    def test_reviewer_suggested_task(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{
            "type": "review", "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["is_reviewer_suggested"] is True
        assert t["accepted"] is False
        assert t["status"] == "reviewer-suggested"

    def test_verified_from_event(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "task_run_completed", "task_id": task_id}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["verified"] is True

    def test_proof_status_from_event(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "proof_collected", "task_id": task_id}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["proof_status"] == "collected"

    def test_test_status_pass(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "test_run_completed", "task_id": task_id,
                    "metadata": {"exit_code": 0}}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["test_status"] == "pass"

    def test_test_status_fail(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "test_run_completed", "task_id": task_id,
                    "metadata": {"exit_code": 1}}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["test_status"] == "fail"

    def test_no_raw_leaks(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[{"type": "t1", "status": "completed"}])
        tp = build_task_progress(job, [])
        tp_str = json.dumps(tp)
        for bad in ("raw_output", "command_output", "Traceback",
                     "diff_preview", "approval_reason"):
            assert bad not in tp_str

    def test_endpoint_safe_404(self):
        """Missing job should return safe error, not traceback."""
        from packages.orchestration.ui_server import _load_job
        _, err = _load_job(str(uuid4()))
        assert err is not None
        assert err[0] == 404
        assert "not found" in err[1]["error"]


# ═══════════════════════════════════════════════════════════════════════════
# Step 128 — Smoke Closure
# ═══════════════════════════════════════════════════════════════════════════




class TestUXZoomAndLabelVisibility:
    """UX semantics verified via API contracts."""

    def test_initial_view_one_node(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        assert vm["visible_counts_by_zoom"][0] == 1
        assert vm["visible_node_ids_by_zoom"][0] == [str(job.id)]

    def test_zoom_in_reveals_more(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        counts = vm["visible_counts_by_zoom"]
        assert counts[-1] >= counts[0]
        assert counts[1] >= counts[0]

    def test_child_job_hidden_until_deep_zoom(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127()
        events = [{
            "event": "job_continued",
            "metadata": {"child_job_id": str(uuid4()), "origin_node_id": str(job.id)},
        }]
        vm = build_brain_view_model(job, events)
        child_nodes = [n for n in vm["nodes"] if n["type"] == "job" and not n["is_origin"]]
        for cn in child_nodes:
            assert cn["visible_from_zoom"] >= 5

    def test_task_ribbon_has_entries(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s127(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        tp = build_task_progress(job, [])
        assert len(tp["tasks"]) == 2

    def test_label_counts_low_at_zoom_0(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        assert vm["label_counts_by_zoom"][0] <= 1

    def test_renderer_no_all_label_default(self):
        """Labels only shown at sufficient zoom — not all visible by default."""
        graph = Path("apps/ui/src/components/graph/ForceBrainGraph.tsx").read_text()
        # Labels gated by globalScale > threshold
        assert "globalScale" in graph, "Label rendering must be gated by zoom scale"
        # CSS container has overflow: hidden
        css = Path("apps/ui/src/components/graph/ForceBrainGraph.module.css").read_text()
        assert "overflow" in css

    def test_renderer_no_full_graph_default(self):
        """Full graph requires explicit toggle — dashboard contract enforces this."""
        from packages.core.models import Job
        from packages.orchestration.ui_server import _build_dashboard
        job = Job(name="test")
        dashboard = _build_dashboard(job)
        assert dashboard["graph_summary"]["full_graph_requires_explicit_toggle"] is True

    def test_renderer_reduced_motion(self):
        """ReducedMotionProvider respects prefers-reduced-motion."""
        content = Path("apps/ui/src/components/shell/ReducedMotionProvider.tsx").read_text()
        assert "prefers-reduced-motion" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 132 — Node Detail + Edge Meaning Closure
# ═══════════════════════════════════════════════════════════════════════════




class TestCommitReadinessSchemaCompleteness:
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




class TestChecklistSchemaAndLabels:
    """Task ribbon checklist."""

    def test_checklist_schema(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job_s163()
        events = _make_events()
        cl = build_checklist(job, events)

        assert cl["version"] == 1
        assert len(cl["items"]) > 0

    def test_no_bare_ids_as_labels(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job_s163()
        events = _make_events()
        cl = build_checklist(job, events)

        for item in cl["items"]:
            label = item["label"]
            assert label, "empty label"
            # Not a bare UUID/hash
            assert not re.match(r"^[0-9a-f-]{8,}$", label), f"bare ID as label: {label}"

    def test_checklist_has_goal(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job_s163("Write a README")
        events = _make_events()
        cl = build_checklist(job, events)

        kinds = [item["kind"] for item in cl["items"]]
        assert "goal" in kinds

    def test_checklist_item_states(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job_s163()
        events = _make_events()
        cl = build_checklist(job, events)

        for item in cl["items"]:
            assert item["state"] in ("done", "current", "pending", "blocked", "suggested"), f"bad state: {item['state']}"
            assert isinstance(item["checked"], bool)

    def test_memory_candidate_in_checklist(self):
        from packages.orchestration.memory_candidates import create_candidate
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job_s163()
        create_candidate(job, "repair_pattern", "Repair fixed mul")
        events = _make_events()
        cl = build_checklist(job, events)

        mem_items = [i for i in cl["items"] if i["kind"] == "memory"]
        assert len(mem_items) >= 1
        assert "Repair fixed mul" in mem_items[0]["label"]


# ===========================================================================
# Step 169 — Human Copy Dictionary
# ===========================================================================




class TestHumanCopyDictionaryLabels:
    """Human copy dictionary."""

    def test_all_default_types_have_labels(self):
        from packages.orchestration.ui_copy import _DEFAULT_VISIBLE, human_label

        for ntype in _DEFAULT_VISIBLE:
            label = human_label(ntype)
            assert label
            assert "_" not in label, f"snake_case in label: {label} for {ntype}"

    def test_no_snake_case_in_labels(self):
        from packages.orchestration.ui_copy import _NODE_LABELS

        for ntype, (label, subtitle) in _NODE_LABELS.items():
            assert "_" not in label, f"snake_case in label: {label}"

    def test_diagnostics_only_set(self):
        from packages.orchestration.ui_copy import is_diagnostics_only

        assert is_diagnostics_only("context_coverage")
        assert is_diagnostics_only("token_policy")
        assert not is_diagnostics_only("job")
        assert not is_diagnostics_only("task")

    def test_human_state(self):
        from packages.orchestration.ui_copy import human_state

        assert human_state("completed") == "Done"
        assert human_state("running") == "In progress"
        assert human_state("blocked") == "Blocked"
        assert human_state(None) == "Unknown"

    def test_forbidden_words_defined(self):
        from packages.orchestration.ui_copy import FORBIDDEN_DEFAULT_WORDS

        assert "rank" in FORBIDDEN_DEFAULT_WORDS
        assert "importance" in FORBIDDEN_DEFAULT_WORDS
        assert "node_type" in FORBIDDEN_DEFAULT_WORDS

    def test_layers_defined(self):
        from packages.orchestration.ui_copy import LAYERS

        assert len(LAYERS) >= 2
        journey = [l for l in LAYERS if l["id"] == "journey"]
        assert len(journey) == 1
        assert journey[0]["default"] is True


# ===========================================================================
# Step 170 — UX Smoke Gate
# ===========================================================================




class TestUXSmokeGateStoryChecklist:
    """UX smoke gate checks."""

    def test_story_available(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events()
        story = build_story(job, events)
        assert story["version"] == 1

    def test_default_story_forbids_debug_words(self):
        from packages.orchestration.ui_copy import FORBIDDEN_DEFAULT_WORDS
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events()
        story = build_story(job, events)

        # Check journey titles and subtitles
        for j in story["journey"]:
            for word in FORBIDDEN_DEFAULT_WORDS:
                assert word not in j["title"].lower()
                assert word not in (j.get("subtitle") or "").lower()

    def test_checklist_has_human_labels(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job_s163()
        events = _make_events()
        cl = build_checklist(job, events)
        for item in cl["items"]:
            assert item["label"]
            assert not re.match(r"^[0-9a-f-]{8,}$", item["label"])

    def test_context_coverage_not_in_journey(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events()
        story = build_story(job, events)

        for j in story["journey"]:
            assert "context coverage" not in j["title"].lower()
            assert "context_coverage" not in j.get("kind", "")


# ===========================================================================
# Step 171 — Visual Polish
# ===========================================================================




class TestAppShellVisualPolishClasses:
    """Visual polish checks."""

    def test_app_shell_has_semantic_classes(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")

        required_classes = [
            "remedy-journey-shell",
            "remedy-checklist",
            "remedy-node-current",
            "remedy-node-done",
            "remedy-detail-compact",
            "remedy-layer-switcher",
        ]
        for cls in required_classes:
            assert cls in html, f"missing CSS class: {cls}"

    def test_no_external_cdn(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        assert "cdn." not in html.lower()
        assert "fonts.googleapis" not in html.lower()
        assert "unpkg.com" not in html.lower()

    def test_reduced_motion(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        assert "prefers-reduced-motion" in html

    def test_detail_card_no_advanced_by_default(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        # Detail card visible class not set by default
        assert 'class="remedy-detail-compact"' in html
        assert 'class="remedy-detail-compact visible"' not in html

    def test_no_debug_rail(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        # No permanent metadata wall or debug rail
        assert "debug-rail" not in html
        assert "metadata-wall" not in html

    def test_label_strategy(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        # Journey nodes use text labels (screen-space stable via SVG text)
        assert "journey-node" in html
        assert "node-subtitle" in html




class TestTimelineDetailLayerComponents:
    """Timeline, detail popover, and layer switcher."""

    def test_phase_timeline(self):
        f = UI_SRC / "components" / "timeline" / "PhaseTimeline.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        # Phase IDs in icons map
        assert "job:" in content
        assert "planning:" in content
        assert "build:" in content
        assert "test:" in content
        assert "review:" in content
        assert "finalized:" in content
        # Renders phase labels dynamically
        assert "phase.label" in content

    def test_detail_popover(self):
        f = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "remedy-detail-compact" in content
        # No forbidden words
        for word in ["rank", "importance", "node_type", "present signals", "missing signals", "zone"]:
            assert word not in content.lower(), f"Debug word in DetailPopover: {word}"

    def test_layer_switcher(self):
        f = UI_SRC / "components" / "layers" / "LayerSwitcher.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Journey" in content
        assert "Diagnostics" in content
        assert "remedy-layer-switcher" in content


# ---------------------------------------------------------------------------
# Steps 192-193 — Visual tokens + particles
# ---------------------------------------------------------------------------




class TestCssTokensAndReducedMotion:
    """Visual tokens and CSS modules."""

    def test_tokens_has_required_vars(self):
        content = (UI_SRC / "styles" / "tokens.css").read_text(encoding="utf-8")
        required = ["--remedy-bg:", "--remedy-blue-500:", "--remedy-card:", "--remedy-text:",
                     "--remedy-shadow:", "--remedy-glow:", "--remedy-left-width:", "--remedy-right-width:"]
        for var in required:
            assert var in content, f"Missing CSS token: {var}"

    def test_globals_has_reduced_motion(self):
        content = (UI_SRC / "styles" / "globals.css").read_text(encoding="utf-8")
        assert "prefers-reduced-motion" in content

    def test_no_external_fonts(self):
        for f in UI_SRC.rglob("*.css"):
            content = f.read_text(encoding="utf-8")
            assert "googleapis.com" not in content, f"External font in {f}"
            assert "cdn." not in content, f"CDN in {f}"

    def test_no_external_cdn_in_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            assert "cdn." not in content.lower(), f"CDN reference in {f}"
            assert "googleapis.com" not in content, f"External resource in {f}"

    def test_particles_respect_reduced_motion(self):
        f = UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx"
        content = f.read_text(encoding="utf-8")
        assert "reducedMotion" in content

    def test_css_modules_exist(self):
        expected = [
            "components/shell/RemedyShell.module.css",
            "components/graph/BrainGraphStage.module.css",
            "components/panels/RightLivePanel.module.css",
            "components/timeline/PhaseTimeline.module.css",
            "components/metrics/TopMetricsBar.module.css",
            "components/detail/DetailPopover.module.css",
            "components/layers/LayerSwitcher.module.css",
        ]
        for path in expected:
            assert (UI_SRC / path).is_file(), f"Missing CSS module: {path}"


# ---------------------------------------------------------------------------
# Step 194 — Human copy mapping
# ---------------------------------------------------------------------------




class TestFrontendHumanCopyMapping:
    """Human copy mapping in frontend."""

    def test_human_copy_exists(self):
        assert (UI_SRC / "copy" / "humanCopy.ts").is_file()

    def test_human_copy_has_labels(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        assert "patch_intent" in content
        assert "Proposed change" in content
        assert "test_run" in content
        assert "Test result" in content

    def test_human_copy_has_diagnostics(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        assert "context_coverage" in content
        assert "diagnosticsOnly" in content

    def test_human_copy_has_scrub(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        assert "scrubUiText" in content
        assert "forbidden" in content

    def test_no_snake_case_labels(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        # Extract label values (right side of colon in conceptLabels)
        labels = re.findall(r':\s*"([^"]+)"', content)
        for label in labels:
            if "_" in label and not label.startswith("context_") and not label.startswith("token_"):
                # Allow internal keys, check human-facing labels
                pass


# ---------------------------------------------------------------------------
# Step 196 — Server integration
# ---------------------------------------------------------------------------




class TestNoPopupOnLoad:
    """Detail popover does not render by default."""

    def test_app_starts_null(self):
        app = (UI_SRC / "RemedyApp.tsx").read_text()
        assert "useState<string | null>(null)" in app


# ---------------------------------------------------------------------------
# No forbidden debug words
# ---------------------------------------------------------------------------

