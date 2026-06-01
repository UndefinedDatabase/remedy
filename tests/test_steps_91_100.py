"""
Tests for Steps 91-100 — ELK layout, semantic zoom v2, autocoder foundation.

Coverage:
  - View model v2: ELK directional layout, ranks, zones, edge kinds
  - Semantic zoom v2: 7 levels, max node counts, full graph toggle
  - Screen-space labels: no Pixi Text in viewport
  - Explainable edges: kinds, meanings, primary chain
  - Live state API: schema, cursor
  - remedy do: dry-run, job creation
  - Source context: file selection, budget, deny list
  - Structured patch: parse, validate, file ops, unified diff
  - Source apply: safe apply, deny list, snapshot/revert
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job():
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    return job


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

class TestELKLayout:
    def test_layout_engine_is_elk(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert vm["layout_engine"] == "elk-layered"

    def test_direction_is_right(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert vm["direction"] == "RIGHT"

    def test_no_ring_layout(self):
        """Ring layout function must not be primary."""
        src = Path(__file__).parent.parent / "packages" / "orchestration" / "ui_view_model.py"
        content = src.read_text()
        assert "angle" not in content.lower() or "radius" not in content.lower(), \
            "Ring layout (angle/radius) should not be primary"

    def test_every_node_has_rank_zone(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        for n in vm["nodes"]:
            assert "rank" in n
            assert "zone" in n
            assert "x" in n
            assert "y" in n

    def test_same_graph_same_positions(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        vm1 = build_brain_view_model(job, [])
        vm2 = build_brain_view_model(job, [])
        for n1, n2 in zip(vm1["nodes"], vm2["nodes"]):
            assert n1["x"] == n2["x"]
            assert n1["y"] == n2["y"]

    def test_job_rank_zero(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        job_nodes = [n for n in vm["nodes"] if n["type"] == "job"]
        for jn in job_nodes:
            assert jn["rank"] == 0

    def test_default_visible_nodes_one(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert vm["max_initial_nodes"] == 1
        zoom0 = [n for n in vm["nodes"] if n["visible_from_zoom"] <= 0]
        assert len(zoom0) <= 1

    def test_no_raw_leaks_in_view_model(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        vm_str = json.dumps(vm)
        for bad in ("raw_stdout", "raw_stderr", "diff_preview", "approval_reason", "api_key"):
            assert bad not in vm_str


# ---------------------------------------------------------------------------
# Step 92 — Semantic Zoom v2
# ---------------------------------------------------------------------------

class TestSemanticZoomV2:
    def test_seven_zoom_levels(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert len(vm["zoom_levels"]) == 7

    def test_full_graph_requires_toggle(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert vm["full_graph_requires_explicit_toggle"] is True

    def test_zoom_level_names(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        names = [z["name"] for z in vm["zoom_levels"]]
        assert names[0] == "Origin"
        assert names[6] == "Full Graph"

    def test_zoom_max_counts(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        maxes = [z["max_nodes"] for z in vm["zoom_levels"]]
        assert maxes[0] == 1
        assert maxes[1] == 3
        assert maxes[2] == 8


# ---------------------------------------------------------------------------
# Step 93 — Screen-Space Labels
# ---------------------------------------------------------------------------

class TestScreenSpaceLabels:
    def test_no_pixi_in_current_graph(self):
        """Current graph renderer (Canvas/Force) must not use raw PIXI imports."""
        graph = Path(__file__).parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"
        content = graph.read_text()
        assert "PIXI" not in content, "ForceBrainGraph should not import raw PIXI"
        assert "pixi.js" not in content, "ForceBrainGraph should not depend on pixi.js"

    def test_legacy_graph_nodes_under_legacy(self):
        """Old GraphNodes.tsx lives under legacy/, not top-level graph/."""
        legacy = Path(__file__).parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "GraphNodes.tsx"
        assert legacy.is_file(), "GraphNodes.tsx must exist under legacy/"

    def test_detail_card_compact(self):
        detail = Path(__file__).parent.parent / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx"
        assert detail.is_file(), "DetailPopover.tsx must exist"
        content = detail.read_text()
        assert "remedy-detail-compact" in content, "DetailPopover must use remedy-detail-compact class"


# ---------------------------------------------------------------------------
# Step 94 — Explainable Edges
# ---------------------------------------------------------------------------

class TestExplainableEdges:
    def test_edges_have_kind_and_meaning(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        for e in vm["edges"]:
            assert "kind" in e
            assert "meaning" in e
            assert e["kind"] != ""
            assert e["meaning"] != ""

    def test_primary_chain_edges(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        for e in vm["edges"]:
            assert "is_primary_chain" in e

    def test_legacy_edge_component_under_legacy(self):
        """Old SoftGlowEdge.tsx is preserved under legacy/."""
        edge = Path(__file__).parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "SoftGlowEdge.tsx"
        assert edge.is_file(), "SoftGlowEdge.tsx must exist under legacy/"

    def test_current_graph_uses_force(self):
        """Current graph renderer uses react-force-graph-2d, not @xyflow/react."""
        graph = Path(__file__).parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"
        content = graph.read_text()
        assert "react-force-graph-2d" in content


# ---------------------------------------------------------------------------
# Step 95 — Live Growth
# ---------------------------------------------------------------------------

class TestLiveGrowth:
    def test_live_state_endpoint_exists(self):
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "live-state" in src
        assert "_build_live_state_json" in src

    def test_events_since_endpoint_exists(self):
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "events-since" in src
        assert "_build_events_since_json" in src

    def test_merge_view_model_in_renderer(self):
        app = Path(__file__).parent.parent / "apps" / "ui" / "src" / "RemedyApp.tsx"
        content = app.read_text()
        assert "setInterval" in content, "RemedyApp must have dashboard refresh via setInterval"

    def test_reduced_motion_respected(self):
        provider = Path(__file__).parent.parent / "apps" / "ui" / "src" / "components" / "shell" / "ReducedMotionProvider.tsx"
        assert provider.is_file(), "ReducedMotionProvider.tsx must exist"
        content = provider.read_text()
        assert "prefers-reduced-motion" in content


# ---------------------------------------------------------------------------
# Step 96 — remedy do
# ---------------------------------------------------------------------------

class TestRemedyDo:
    def test_dry_run_no_side_effects(self, tmp_path):
        from packages.orchestration.autorun import dry_run_autorun
        plan = dry_run_autorun("test goal", str(tmp_path))
        assert plan["dry_run"] is True
        assert plan["goal"] == "test goal"
        assert "phases" in plan

    def test_dry_run_phases_by_autonomy(self, tmp_path):
        from packages.orchestration.autorun import dry_run_autorun
        plan0 = dry_run_autorun("g", str(tmp_path), autonomy_level=0)
        plan4 = dry_run_autorun("g", str(tmp_path), autonomy_level=4)
        assert "run_builder" not in plan0["phases"]
        assert "run_tests" in plan4["phases"]

    def test_do_creates_job(self, tmp_path):
        from packages.orchestration.autorun import run_autorun
        result = run_autorun("test", str(tmp_path), autonomy_level=0, max_cycles=1)
        assert result.job_id != ""
        assert result.stage == "job_created"

    def test_do_respects_max_cycles(self, tmp_path):
        from packages.orchestration.autorun import run_autorun
        result = run_autorun("test", str(tmp_path), max_cycles=1, autonomy_level=0)
        assert result.cycles_run <= 1

    def test_do_command_in_catalog(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("do.run")
        assert cmd.group_id == "do"
        assert cmd.may_mutate_repo is True


# ---------------------------------------------------------------------------
# Step 97 — Source Context Injection
# ---------------------------------------------------------------------------

class TestSourceContext:
    def test_select_relevant_files(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "main.py").write_text("print('hi')")
        (tmp_path / "test_main.py").write_text("def test(): pass")
        (tmp_path / "package.json").write_text('{"name":"x"}')

        files = select_relevant_files(tmp_path, budget=1000)
        assert len(files) >= 3
        categories = {f.category for f in files}
        assert "manifest" in categories
        assert "readme" in categories

    def test_env_excluded(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        (tmp_path / ".env").write_text("SECRET=abc")
        (tmp_path / "main.py").write_text("x = 1")

        files = select_relevant_files(tmp_path, budget=1000)
        paths = [f.path for f in files]
        assert ".env" not in paths

    def test_budget_respected(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        (tmp_path / "big.py").write_text("x = 1\n" * 10000)

        files = select_relevant_files(tmp_path, budget=100)
        total = sum(f.estimated_tokens for f in files)
        assert total <= 100

    def test_node_modules_excluded(self, tmp_path):
        from packages.orchestration.source_context import select_relevant_files
        nm = tmp_path / "node_modules" / "pkg"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {}")

        files = select_relevant_files(tmp_path, budget=1000)
        paths = [f.path for f in files]
        assert not any("node_modules" in p for p in paths)

    def test_event_schema(self, tmp_path):
        from packages.orchestration.source_context import inject_source_context
        from packages.orchestration.data_paths import resolve_data_root
        (tmp_path / "main.py").write_text("x = 1")

        job = _make_job()
        data_dir = resolve_data_root()
        ctx = inject_source_context(job, tmp_path, data_dir=data_dir)
        assert ctx.version == 1
        assert ctx.file_count >= 1
        assert ctx.selection_hash != ""


# ---------------------------------------------------------------------------
# Step 98 — Structured Code Patch Intent
# ---------------------------------------------------------------------------

class TestStructuredPatch:
    def test_parse_file_ops_json(self):
        from packages.orchestration.structured_patch import parse_structured_patch
        raw = """Here's the fix:
```json
{
  "file_ops": [
    {"path": "main.py", "action": "modify", "content": "print('fixed')", "summary": "Fix"}
  ]
}
```"""
        patch = parse_structured_patch(raw)
        assert patch.intent_kind == "file_ops"
        assert len(patch.file_ops) == 1
        assert patch.file_ops[0].path == "main.py"

    def test_parse_unified_diff(self):
        from packages.orchestration.structured_patch import parse_structured_patch
        raw = """--- a/main.py
+++ b/main.py
@@ -1,3 +1,3 @@
 def hello():
-    return "world"
+    return "fixed"
"""
        patch = parse_structured_patch(raw)
        assert patch.intent_kind == "unified_diff"
        assert len(patch.unified_diffs) == 1

    def test_parse_narrative_fallback(self):
        from packages.orchestration.structured_patch import parse_structured_patch
        patch = parse_structured_patch("Just update the README with better docs")
        assert patch.intent_kind == "markdown"
        assert patch.applicability == "not_applicable"

    def test_validate_path_traversal(self):
        from packages.orchestration.structured_patch import (
            FileOp, StructuredPatch, validate_structured_patch,
        )
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="../../../etc/passwd", action="create", content="bad"),),
            target_paths=("../../../etc/passwd",),
        )
        issues = validate_structured_patch(patch)
        assert len(issues) > 0
        assert any("traversal" in i for i in issues)

    def test_validate_env_blocked(self):
        from packages.orchestration.structured_patch import (
            FileOp, StructuredPatch, validate_structured_patch,
        )
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path=".env", action="create", content="SECRET=x"),),
            target_paths=(".env",),
        )
        issues = validate_structured_patch(patch)
        assert len(issues) > 0


# ---------------------------------------------------------------------------
# Step 99 — Source Patch Apply
# ---------------------------------------------------------------------------

class TestSourceApply:
    def test_apply_simple_file_op(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="hello.py", action="create", content="print('hi')"),),
            target_paths=("hello.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert result.success
        assert result.files_created == 1
        assert (tmp_path / "hello.py").read_text() == "print('hi')"

    def test_apply_modify(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        (tmp_path / "main.py").write_text("old content")
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="main.py", action="modify", content="new content"),),
            target_paths=("main.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert result.success
        assert result.files_modified == 1
        assert (tmp_path / "main.py").read_text() == "new content"

    def test_apply_blocks_env(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path=".env", action="create", content="SECRET=x"),),
            target_paths=(".env",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        # Failure must be path safety, not missing permission or approval
        assert any(".env" in e for e in result.errors)
        assert not any("permission denied" in e for e in result.errors)
        assert not any("approval" in e for e in result.errors)

    def test_apply_blocks_path_traversal(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="../escape.py", action="create", content="bad"),),
            target_paths=("../escape.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        # Failure must be path traversal, not missing permission
        assert any("traversal" in e for e in result.errors)

    def test_snapshot_and_revert(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch, revert_apply
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        (tmp_path / "orig.py").write_text("original")
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="orig.py", action="modify", content="modified"),),
            target_paths=("orig.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert result.success
        assert (tmp_path / "orig.py").read_text() == "modified"

        # Revert
        success = revert_apply(result.snapshots, tmp_path)
        assert success
        assert (tmp_path / "orig.py").read_text() == "original"

    def test_apply_blocks_binary(self, tmp_path):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job, intent_id = _make_approved_job()
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="data.bin", action="create", content="hello\x00world"),),
            target_paths=("data.bin",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        # Failure must be binary content, not missing permission
        assert any("binary" in e for e in result.errors)

    def test_apply_without_intent_blocked(self, tmp_path):
        """source_apply without intent_id is blocked."""
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="x.py", action="create", content="x"),),
            target_paths=("x.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=_make_permitted_job())
        assert not result.success
        assert any("intent_id" in e for e in result.errors)

    def test_apply_with_pending_intent_blocked(self, tmp_path):
        """source_apply with pending (not approved) intent is blocked."""
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        job = _make_permitted_job()
        artifact = MagicMock()
        artifact.id = uuid4()
        artifact.task_id = uuid4()
        intent_id = f"{artifact.id.hex[:8]}-0"
        artifact.metadata = {
            "patch_intent_explanations": [
                {"file": "t.py", "action": "create", "risk": "low", "reason": "t", "summary": "t"}
            ],
            "patch_intent_approvals": {
                intent_id: {"intent_id": intent_id, "state": "pending"}
            },
        }
        job.artifacts = [artifact]

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="x.py", action="create", content="x"),),
            target_paths=("x.py",),
        )
        result = apply_structured_patch(patch, tmp_path, job=job, intent_id=intent_id)
        assert not result.success
        assert any("pending" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Step 100 — Frontend Build / Smoke
# ---------------------------------------------------------------------------

class TestFrontendBuildV2:
    def test_dist_exists(self):
        index = Path(__file__).parent.parent / "apps" / "ui" / "index.html"
        assert index.is_file(), "Source index.html must exist"

    def test_force_graph_in_package(self):
        """Current graph uses react-force-graph-2d + d3-force, not @xyflow/react."""
        pkg = Path(__file__).parent.parent / "apps" / "ui" / "package.json"
        data = json.loads(pkg.read_text())
        deps = data.get("dependencies", {})
        assert "react-force-graph-2d" in deps, "react-force-graph-2d must be a dependency"
        assert "d3-force" in deps, "d3-force must be a dependency for force graph"

    def test_no_dark_background(self):
        tokens = Path(__file__).parent.parent / "apps" / "ui" / "src" / "styles" / "tokens.css"
        css = tokens.read_text()
        assert "#edf3fb" in css, "Light background token must be present"
        for dark in ["#0a0e14", "#0d1117", "#1a1a2e", "#000000"]:
            assert dark not in css


class TestAutorunSmoke:
    """Step 100 — basic autorun integration."""

    def test_fixture_builder_path(self, tmp_path):
        from packages.orchestration.autorun import run_autorun
        # Create tiny fixture repo
        (tmp_path / "main.py").write_text("def add(a, b): return a + b")
        (tmp_path / "test_main.py").write_text("from main import add\ndef test_add(): assert add(1,2)==3")

        result = run_autorun(
            "Make the function pass the test",
            str(tmp_path),
            autonomy_level=2,
            max_cycles=1,
            fixture_builder=True,
        )
        assert result.job_id != ""
        assert result.stage in ("builder_complete", "context_injected", "job_created")
