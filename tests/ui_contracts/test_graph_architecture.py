"""
Domain tests: ui_contracts/test_graph_architecture.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

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




class TestVisualSystem:
    def test_design_tokens_present(self):
        from packages.orchestration.brain_viewer_theme import DESIGN_TOKENS
        required_vars = [
            "--remedy-bg", "--remedy-fg", "--remedy-teal", "--remedy-cyan",
            "--remedy-panel", "--remedy-muted", "--remedy-risk", "--remedy-warning",
            "--remedy-proof", "--remedy-memory",
        ]
        for var in required_vars:
            assert var in DESIGN_TOKENS, f"missing token: {var}"

    def test_css_variables_in_css(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        for var in ["--remedy-bg", "--remedy-fg", "--remedy-teal", "--remedy-cyan",
                     "--remedy-panel", "--remedy-muted", "--remedy-risk",
                     "--remedy-warning", "--remedy-proof", "--remedy-memory"]:
            assert var in REMEDY_CSS, f"missing CSS var: {var}"

    def test_required_classes(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        required_classes = [
            "remedy-shell", "remedy-orbit-bg", "remedy-particle-field",
            "remedy-glass-panel", "remedy-proof-chain", "remedy-node-card",
            "remedy-node-status", "remedy-timeline", "remedy-decision-panel",
            "remedy-readiness-panel",
        ]
        for cls in required_classes:
            assert cls in REMEDY_CSS, f"missing class: {cls}"

    def test_no_external_urls(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert "http://" not in REMEDY_CSS
        assert "https://" not in REMEDY_CSS
        assert "cdn." not in REMEDY_CSS.lower()

    def test_no_trademark_assets(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        lower = REMEDY_CSS.lower()
        assert "assassin" not in lower
        assert "abstergo" not in lower
        assert "ubisoft" not in lower

    def test_reduced_motion(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert "prefers-reduced-motion" in REMEDY_CSS

    def test_status_classes_exist(self):
        from packages.orchestration.brain_viewer_theme import STATUS_CLASSES
        assert "verified" in STATUS_CLASSES
        assert "blocked" in STATUS_CLASSES
        assert "pending" in STATUS_CLASSES
        assert "running" in STATUS_CLASSES
        assert "memory" in STATUS_CLASSES
        assert "future" in STATUS_CLASSES

    def test_get_status_class(self):
        from packages.orchestration.brain_viewer_theme import get_status_class
        assert "verified" in get_status_class("completed")
        assert "risk" in get_status_class("blocked")
        assert "decision" in get_status_class("pending")
        assert "memory" in get_status_class("anything", "memory_placeholder")

    def test_layer_classes(self):
        from packages.orchestration.brain_viewer_theme import LAYER_CLASSES
        assert "job" in LAYER_CLASSES
        assert "patch_intent" in LAYER_CLASSES
        assert "test_run" in LAYER_CLASSES
        assert "decision_queue" in LAYER_CLASSES

    def test_no_raw_leaks_in_css(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        for forbidden in ("stdout", "stderr", "raw_output", "Traceback",
                          "diff_preview", "approval_reason", "command_output"):
            assert forbidden not in REMEDY_CSS


# ── Step 73: Brain Viewer Shell ─────────────────────────────────────────




class TestSpatialLayout:
    def test_nodes_have_zone(self):
        _, data, _ = _get_viewer_html()
        for node in data.graph["nodes"]:
            assert "zone" in node, f"node {node['id']} missing zone"

    def test_layout_deterministic(self):
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
        )
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job_s74()
        events = []
        graph = build_project_brain(job, events)
        d1 = build_brain_viewer_data(job, graph, events)
        d2 = build_brain_viewer_data(job, graph, events)
        assert d1.positions == d2.positions

    def test_zone_labels_in_viewer(self):
        html, _, _ = _get_viewer_html()
        assert "zone-label" in html

    def test_zone_map_covers_types(self):
        from packages.orchestration.brain_viewer import _ZONE_MAP
        required = ["job", "task", "artifact", "patch_intent", "memory_placeholder",
                     "mcp_placeholder", "decision_queue", "test_run"]
        for t in required:
            assert t in _ZONE_MAP, f"missing zone for {t}"

    def test_future_nodes_muted(self):
        html, _, _ = _get_viewer_html()
        assert "future-edge" in html or "future" in html

    def test_edge_types_distinguished(self):
        html, _, _ = _get_viewer_html()
        assert "proof-edge" in html
        assert "blocked-edge" in html
        assert "future-edge" in html

    def test_no_raw_leaks_in_viewer(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        html, _, _ = _get_viewer_html()
        findings = find_forbidden_surface_tokens(html)
        assert findings == []


# ── Step 77: Motion & Depth System ──────────────────────────────────────




class TestELKLayout:
    def test_layout_engine_is_elk(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        assert vm["layout_engine"] == "elk-layered"

    def test_direction_is_right(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        assert vm["direction"] == "RIGHT"

    def test_no_ring_layout(self):
        """Ring layout function must not be primary."""
        src = Path(__file__).parent.parent.parent / "packages" / "orchestration" / "ui_view_model.py"
        content = src.read_text()
        assert "angle" not in content.lower() or "radius" not in content.lower(), \
            "Ring layout (angle/radius) should not be primary"

    def test_every_node_has_rank_zone(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        for n in vm["nodes"]:
            assert "rank" in n
            assert "zone" in n
            assert "x" in n
            assert "y" in n

    def test_same_graph_same_positions(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s91()
        vm1 = build_brain_view_model(job, [])
        vm2 = build_brain_view_model(job, [])
        for n1, n2 in zip(vm1["nodes"], vm2["nodes"]):
            assert n1["x"] == n2["x"]
            assert n1["y"] == n2["y"]

    def test_job_rank_zero(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        job_nodes = [n for n in vm["nodes"] if n["type"] == "job"]
        for jn in job_nodes:
            assert jn["rank"] == 0

    def test_default_visible_nodes_one(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        assert vm["max_initial_nodes"] == 1
        zoom0 = [n for n in vm["nodes"] if n["visible_from_zoom"] <= 0]
        assert len(zoom0) <= 1

    def test_no_raw_leaks_in_view_model(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        vm_str = json.dumps(vm)
        for bad in ("raw_stdout", "raw_stderr", "diff_preview", "approval_reason", "api_key"):
            assert bad not in vm_str


# ---------------------------------------------------------------------------
# Step 92 — Semantic Zoom v2
# ---------------------------------------------------------------------------




class TestSemanticZoomV2:
    def test_seven_zoom_levels(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        assert len(vm["zoom_levels"]) == 7

    def test_full_graph_requires_toggle(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        assert vm["full_graph_requires_explicit_toggle"] is True

    def test_zoom_level_names(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        names = [z["name"] for z in vm["zoom_levels"]]
        assert names[0] == "Origin"
        assert names[6] == "Full Graph"

    def test_zoom_max_counts(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        maxes = [z["max_nodes"] for z in vm["zoom_levels"]]
        assert maxes[0] == 1
        assert maxes[1] == 3
        assert maxes[2] == 8


# ---------------------------------------------------------------------------
# Step 93 — Screen-Space Labels
# ---------------------------------------------------------------------------




class TestExplainableEdges:
    def test_edges_have_kind_and_meaning(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        for e in vm["edges"]:
            assert "kind" in e
            assert "meaning" in e
            assert e["kind"] != ""
            assert e["meaning"] != ""

    def test_primary_chain_edges(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s91(), [])
        for e in vm["edges"]:
            assert "is_primary_chain" in e

    @pytest.mark.skip(reason=(
        "D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+)."))
    def test_legacy_edge_component_under_legacy(self):
        """Old SoftGlowEdge.tsx is preserved under legacy/."""
        edge = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "SoftGlowEdge.tsx"
        assert edge.is_file(), "SoftGlowEdge.tsx must exist under legacy/"

    def test_current_graph_uses_force(self):
        """Current graph renderer uses react-force-graph-2d, not @xyflow/react."""
        graph = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx"
        content = graph.read_text()
        assert "react-force-graph-2d" in content


# ---------------------------------------------------------------------------
# Step 95 — Live Growth
# ---------------------------------------------------------------------------




class TestSemanticZoomDirection:
    def test_zoom_policy_direction(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(), [])
        assert vm["zoom_policy"]["direction"] == "zoom_in_reveals_more"

    def test_zoom_policy_fields(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(), [])
        policy = vm["zoom_policy"]
        assert policy["zoom_out_reduces_complexity"] is True
        assert policy["full_graph_requires_explicit_toggle"] is True

    def test_visible_counts_monotonic_non_decreasing(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(5), [])
        counts = vm["visible_counts_by_zoom"]
        assert isinstance(counts, list)
        assert len(counts) > 0
        for i in range(1, len(counts)):
            assert counts[i] >= counts[i - 1], f"counts[{i}]={counts[i]} < counts[{i-1}]={counts[i-1]}"

    @pytest.mark.skip(reason=(
        "D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+)."))
    def test_renderer_zoom_direction_in_legacy_source(self):
        """Verify legacy semanticZoom.ts maps lower viewport zoom to lower level."""
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "semanticZoom.ts").read_text()
        assert "return 0;" in src
        assert "return 4;" in src


# ---------------------------------------------------------------------------
# Step 103 — Forward Flow Layout
# ---------------------------------------------------------------------------




class TestForwardFlowLayout:
    def test_layout_direction_right(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(), [])
        assert vm["direction"] == "RIGHT"

    def test_node_ranks_non_negative(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job_s101(3), [])
        for node in vm["nodes"]:
            assert node["rank"] >= 0


# ---------------------------------------------------------------------------
# Step 104 — Task Progress Ribbon
# ---------------------------------------------------------------------------




class TestSemanticZoomMonotonicVisibility:

    def test_zoom_policy_in_view_model(self):
        """View model must have zoom_policy with correct direction."""
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert vm["zoom_policy"]["direction"] == "zoom_in_reveals_more"
        assert vm["zoom_policy"]["full_graph_requires_explicit_toggle"] is True

    def test_visible_counts_monotonic(self):
        """visible_counts_by_zoom must be monotonic non-decreasing."""
        job = _make_job_s111(tasks=[
            {"type": "readme_draft", "status": "completed"},
            {"type": "code_review", "status": "running"},
            {"type": "testing", "status": "pending"},
        ])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        counts = vm["visible_counts_by_zoom"]
        for i in range(len(counts) - 1):
            assert counts[i] <= counts[i + 1], f"not monotonic at {i}: {counts}"

    def test_visible_node_ids_subset_monotonicity(self):
        """visible_node_ids_by_zoom[n] must be subset of [n+1]."""
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        ids_by_zoom = vm["visible_node_ids_by_zoom"]
        for i in range(len(ids_by_zoom) - 1):
            assert set(ids_by_zoom[i]) <= set(ids_by_zoom[i + 1]), \
                f"zoom {i} not subset of {i+1}"

    def test_label_counts_in_view_model(self):
        """label_counts_by_zoom must be present and reasonable."""
        job = _make_job_s111(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert "label_counts_by_zoom" in vm
        assert isinstance(vm["label_counts_by_zoom"], list)
        assert len(vm["label_counts_by_zoom"]) == 7

    def test_zoom_level_0_only_origin(self):
        """At zoom 0, only origin job node should be visible."""
        job = _make_job_s111(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        ids_at_0 = vm["visible_node_ids_by_zoom"][0]
        # Should contain only the job origin
        assert len(ids_at_0) <= 1

    def test_non_origin_labels_hidden_at_zoom_0(self):
        """At zoom 0, label_counts should be 0 (no labels at origin-only level)."""
        job = _make_job_s111(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert vm["label_counts_by_zoom"][0] == 0

    def test_version_is_4(self):
        """View model version should be 4."""
        job = _make_job_s111()
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert vm["version"] == 4


# ═══════════════════════════════════════════════════════════════════════════
# Step 114 — Forward Flow + Edge Meaning v3
# ═══════════════════════════════════════════════════════════════════════════




class TestForwardFlowEdgeRankContract:

    def test_nodes_have_flow_role(self):
        """Every node must have flow_role."""
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for n in vm["nodes"]:
            assert "flow_role" in n, f"node {n['id']} missing flow_role"

    def test_nodes_have_lane(self):
        """Every node must have lane."""
        job = _make_job_s111(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for n in vm["nodes"]:
            assert "lane" in n

    def test_edges_have_source_target_rank(self):
        """Every edge must have source_rank, target_rank, primary_path."""
        job = _make_job_s111(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert "source_rank" in e
            assert "target_rank" in e
            assert "primary_path" in e

    def test_edge_target_rank_gte_source(self):
        """For primary path edges, target rank >= source rank (forward flow)."""
        job = _make_job_s111(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            if e["primary_path"]:
                assert e["target_rank"] >= e["source_rank"], \
                    f"backward flow edge: {e['source']} → {e['target']}"

    def test_each_edge_has_user_meaning(self):
        """Every edge must have a meaning string."""
        job = _make_job_s111(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert e.get("meaning"), f"edge missing meaning: {e['source']}→{e['target']}"

    def test_origin_flow_role(self):
        """Job node flow_role should be 'origin'."""
        job = _make_job_s111()
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        job_nodes = [n for n in vm["nodes"] if n["type"] == "job"]
        assert job_nodes
        assert job_nodes[0]["flow_role"] == "origin"

    def test_task_flow_roles_deterministic(self):
        """Completed task should be task_completed, running should be task_active."""
        job = _make_job_s111(tasks=[
            {"type": "write", "status": "completed"},
            {"type": "review", "status": "running"},
        ])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        task_nodes = [n for n in vm["nodes"] if n["type"] == "task"]
        roles = {n["flow_role"] for n in task_nodes}
        assert "task_completed" in roles
        assert "task_active" in roles


# ═══════════════════════════════════════════════════════════════════════════
# Step 115 — Task Ribbon as Product Navigation v2
# ═══════════════════════════════════════════════════════════════════════════




class TestJourneyLeftToRightLayout:
    """Journey graph layout."""

    def test_journey_left_to_right(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events()
        story = build_story(job, events)

        # Journey items should have increasing kind order (goal → task → ... → proof)
        kind_order = {"goal": 0, "task": 1, "change": 2, "approval": 3,
                      "apply": 4, "test": 5, "proof": 6, "review": 7, "memory": 8, "decision": 9}
        journey = story["journey"]
        if len(journey) >= 2:
            orders = [kind_order.get(j["kind"], 99) for j in journey]
            # Should be non-decreasing
            for i in range(1, len(orders)):
                assert orders[i] >= orders[i-1], f"journey not left-to-right at index {i}"

    def test_no_system_nodes_in_default(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job_s163()
        events = _make_events()
        story = build_story(job, events)

        # Journey should not contain diagnostics-only nodes
        for j in story["journey"]:
            # We can't directly check node_type from journey, but titles should not be system labels
            title = j["title"].lower()
            assert "context coverage" not in title
            assert "token policy" not in title
            assert "worker" not in title


# ===========================================================================
# Step 167 — Diagnostics Layers
# ===========================================================================




class TestDiagnosticsLayerSchema:
    """Diagnostics layers."""

    def test_layer_schema(self):
        from packages.orchestration.ui_view_model import build_layers

        layers = build_layers()
        assert layers["version"] == 1
        assert len(layers["layers"]) >= 2

    def test_default_layer_is_journey(self):
        from packages.orchestration.ui_view_model import build_layers

        layers = build_layers()
        defaults = [l for l in layers["layers"] if l.get("default")]
        assert len(defaults) == 1
        assert defaults[0]["id"] == "journey"

    def test_diagnostics_layer_exists(self):
        from packages.orchestration.ui_view_model import build_layers

        layers = build_layers()
        diag = [l for l in layers["layers"] if l["id"] == "diagnostics"]
        assert len(diag) == 1
        assert not diag[0].get("default")

    def test_diagnostics_nodes_separate(self):
        from packages.orchestration.ui_view_model import build_diagnostics_nodes

        job = _make_job_s163()
        events = _make_events()
        result = build_diagnostics_nodes(job, events)
        assert result["layer"] == "diagnostics"
        # Should only contain diagnostics-type nodes


# ===========================================================================
# Step 168 — Task Ribbon Checklist
# ===========================================================================




class TestForceGraphComponentIntegrity:
    """React Flow graph components."""

    def test_brain_graph_stage(self):
        assert (UI_SRC / "components" / "graph" / "BrainGraphStage.tsx").is_file()

    def test_force_brain_graph(self):
        f = UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "react-force-graph-2d" in content
        assert "nodeCanvasObject" in content

    def test_force_brain_model(self):
        f = UI_SRC / "components" / "graph" / "buildForceBrainModel.ts"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "seededRng" in content
        assert "ForceBrainNode" in content

    def test_force_brain_types(self):
        assert (UI_SRC / "components" / "graph" / "forceBrainTypes.ts").is_file()

    def test_graph_deterministic(self):
        content = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text(encoding="utf-8")
        assert "Math.random" not in content

    def test_resize_observer(self):
        content = (UI_SRC / "components" / "graph" / "useGraphSize.ts").read_text(encoding="utf-8")
        assert "ResizeObserver" in content

    def test_graph_filter_chips(self):
        f = UI_SRC / "components" / "graph" / "GraphFilterChips.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert '"All"' in content
        assert '"Needs work"' in content or '"Open"' in content
        assert '"Planned"' in content
        assert '"Done"' in content

    def test_no_default_debug_labels_in_graph(self):
        content = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text(encoding="utf-8")
        for word in ["rank", "importance", "node_type", "context coverage", "zone"]:
            assert word not in content.lower(), f"Debug word in ForceBrainGraph: {word}"


# ---------------------------------------------------------------------------
# Steps 184-188 — Right panel + cards
# ---------------------------------------------------------------------------




class TestForceGraphDependencySwap:
    """react-force-graph-2d replaces @xyflow/react."""

    def test_package_has_force_graph(self):
        pkg = (UI_ROOT / "package.json").read_text()
        assert "react-force-graph-2d" in pkg

    def test_package_has_d3_force(self):
        pkg = (UI_ROOT / "package.json").read_text()
        assert "d3-force" in pkg

    def test_no_xyflow_in_package(self):
        pkg = (UI_ROOT / "package.json").read_text()
        assert "@xyflow/react" not in pkg

    def test_no_xyflow_in_default_graph(self):
        graph_dir = UI_SRC / "components" / "graph"
        for f in graph_dir.glob("*.tsx"):
            if "legacy" in str(f):
                continue
            content = f.read_text()
            assert "@xyflow/react" not in content, f"@xyflow/react in {f.name}"

    def test_no_xyflow_in_default_ts(self):
        graph_dir = UI_SRC / "components" / "graph"
        for f in graph_dir.glob("*.ts"):
            if "legacy" in str(f):
                continue
            content = f.read_text()
            assert "@xyflow/react" not in content, f"@xyflow/react in {f.name}"


# ---------------------------------------------------------------------------
# Step 229 — Responsive shell
# ---------------------------------------------------------------------------




class TestForceGraph:
    """Canvas force graph is default."""

    def test_force_brain_graph_exists(self):
        assert (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").is_file()

    def test_force_types_exist(self):
        assert (UI_SRC / "components" / "graph" / "forceBrainTypes.ts").is_file()

    def test_build_model_exists(self):
        assert (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").is_file()

    def test_brain_stage_uses_graph(self):
        code = (UI_SRC / "components" / "graph" / "BrainGraphStage.tsx").read_text()
        assert "BrainGraphCanvas" in code or "ForceBrainGraph" in code
        assert "RemedyBrainFlow" not in code
        assert "ConstellationBackdrop" not in code

    def test_force_graph_imports_force_graph_2d(self):
        code = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "react-force-graph-2d" in code

    def test_canvas_rendering(self):
        # New design pack: links are soft (no glow/shadowBlur, no directional
        # particles). Nodes use radial gradients; links use quadratic curves.
        code = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "createRadialGradient" in code
        assert "quadraticCurveTo" in code

    def test_no_math_random_in_model(self):
        code = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        assert "Math.random" not in code

    def test_seeded_rng(self):
        code = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        assert "seededRng" in code

    def test_resize_observer_hook(self):
        code = (UI_SRC / "components" / "graph" / "useGraphSize.ts").read_text()
        assert "ResizeObserver" in code

    def test_reduced_motion_respected(self):
        code = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "reducedMotion" in code or "reduced-motion" in code


# ---------------------------------------------------------------------------
# Step 240 — Better data normalization
# ---------------------------------------------------------------------------

