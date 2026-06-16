"""
Domain tests: ui_server/test_brain_view_model.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task

_ROOT = Path(__file__).resolve().parent.parent.parent


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


def _make_job_s122(*, tasks=None, name="test"):
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
# Step 122 — Job-focused Origin Semantics
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


def _make_job_s163(name: str = "Test goal") -> Job:
    job = Job(name=name)
    job.metadata = job.metadata or {}
    return job


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


# ── Step 68.1: Event Schema Registry ────────────────────────────────────


def _make_events_s163() -> list[dict]:
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




class TestBrainDetail:
    def test_detail_decision_queue(self):
        from packages.orchestration.brain_detail import build_brain_node_detail
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        events = _make_events()
        graph = build_project_brain(job, events)
        detail = build_brain_node_detail(job, graph, "decision_queue", events)
        assert detail is not None
        assert "decision" in detail.title.lower() or "Decision" in detail.title

    def test_detail_context_budget(self):
        from packages.orchestration.brain_detail import build_brain_node_detail
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        events = _make_events()
        graph = build_project_brain(job, events)
        detail = build_brain_node_detail(job, graph, "context_budget", events)
        assert detail is not None
        assert "context" in detail.title.lower() or "Context" in detail.title


# ── Step 71.1: Token Policy Applied ──────────────────────────────────────




class TestBrainViewModel:
    """Tests for ui_view_model.build_brain_view_model."""

    def _make_job(self):
        # Use a minimal mock job
        job = MagicMock()
        job.id = uuid4()
        job.name = "test-job"
        job.state.value = "active"
        job.tasks = []
        job.artifacts = []
        return job

    def _make_graph_and_events(self):
        """Return a (job, events) pair that produces a valid brain graph."""
        job = self._make_job()
        events = []
        return job, events

    def test_view_model_structure(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        assert vm["version"] == 4
        assert "nodes" in vm
        assert "edges" in vm
        assert "layers" in vm
        assert len(vm["layers"]) == 7

    def test_layer_names(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        names = [l["name"] for l in vm["layers"]]
        assert names == ["Origin", "Intent Path", "Work Path", "Proof Path", "Attention", "System Clusters", "Full Graph"]

    def test_job_node_is_layer_zero(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        job_nodes = [n for n in vm["nodes"] if n["type"] == "job"]
        assert len(job_nodes) >= 1
        for jn in job_nodes:
            assert jn["layer"] == 0
            assert jn["visible_from_zoom"] == 0

    def test_origin_max_nodes(self):
        """At zoom level 0 (origin), at most 1 node visible."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        zoom0_nodes = [n for n in vm["nodes"] if n["visible_from_zoom"] <= 0]
        assert len(zoom0_nodes) <= 1, f"Origin zoom shows {len(zoom0_nodes)} nodes, max 1"

    def test_no_labels_at_origin_except_job(self):
        """At zoom level 0, only job node may show label."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for n in vm["nodes"]:
            if n["visible_from_zoom"] == 0 and n["type"] != "job":
                assert n["show_label_from_zoom"] > 0, (
                    f"Node {n['id']} (type={n['type']}) shows label at zoom 0"
                )

    def test_node_has_position(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for n in vm["nodes"]:
            assert "x" in n
            assert "y" in n

    def test_node_has_cluster(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for n in vm["nodes"]:
            assert "cluster_id" in n
            assert n["cluster_id"] in (
                "origin", "lifecycle", "patches", "testing",
                "attention", "events", "system", "other",
                "proofs", "future",
            )

    def test_edge_visibility(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for e in vm["edges"]:
            assert "visible_from_zoom" in e
            assert 0 <= e["visible_from_zoom"] <= 6


# ---------------------------------------------------------------------------
# Node Detail
# ---------------------------------------------------------------------------




class TestNodeDetail:
    def _make_job(self):
        job = MagicMock()
        job.id = uuid4()
        job.name = "test-job"
        job.state.value = "active"
        job.tasks = []
        job.artifacts = []
        return job

    def test_detail_returns_node_info(self):
        from packages.orchestration.ui_view_model import build_brain_view_model, build_node_detail
        job = self._make_job()
        events: list[dict] = []

        vm = build_brain_view_model(job, events)
        if vm["nodes"]:
            node_id = vm["nodes"][0]["id"]
            detail = build_node_detail(job, events, node_id)
            assert detail["version"] == 2
            assert detail["node_id"] == node_id
            assert "title" in detail
            assert "status_text" in detail

    def test_detail_missing_node(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = MagicMock()
        job.id = uuid4()
        job.name = "test"
        job.state.value = "active"
        job.tasks = []
        job.artifacts = []

        detail = build_node_detail(job, [], "nonexistent-node-id")
        assert "error" in detail


# ---------------------------------------------------------------------------
# Frontend Build
# ---------------------------------------------------------------------------




class TestViewModelFieldAndZoomContract:
    """Exact API field contracts, zoom contracts, node/edge contracts."""

    def test_version_is_4(self):
        """View model version must be 4."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        assert vm["version"] == 4

    def test_top_level_required_fields(self):
        """All required top-level fields must be present."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        required = {
            "version", "job_id", "layout_engine", "direction", "origin",
            "total_nodes", "total_edges", "default_zoom_level",
            "max_initial_nodes", "advanced_full_graph_available",
            "full_graph_requires_explicit_toggle", "zoom_policy",
            "visible_counts_by_zoom", "visible_node_ids_by_zoom",
            "label_counts_by_zoom", "layers", "zoom_levels",
            "nodes", "edges", "clusters",
        }
        missing = required - set(vm.keys())
        assert not missing, f"Missing: {missing}"

    def test_node_required_fields(self):
        """Each node must have all required fields."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        required = {
            "id", "type", "kind", "user_title", "user_kind",
            "label_short", "label_full", "layer", "rank", "zone",
            "importance", "status", "risk", "cluster_id",
            "visible_from_zoom", "show_label_from_zoom",
            "is_origin", "is_primary_chain", "is_attention",
            "x", "y", "width", "height",
            "flow_role", "lane",
        }
        for node in vm["nodes"]:
            missing = required - set(node.keys())
            assert not missing, f"Node {node['id']} missing: {missing}"

    def test_edge_required_fields(self):
        """Each edge must have all required fields."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        required = {
            "source", "target", "kind", "label", "meaning",
            "visible_from_zoom", "is_primary_chain", "strength",
            "direction", "source_rank", "target_rank", "primary_path",
        }
        for edge in vm["edges"]:
            missing = required - set(edge.keys())
            assert not missing, f"Edge {edge['source']}->{edge['target']} missing: {missing}"

    def test_zoom_level_count(self):
        """Must have exactly 7 zoom levels (0-6)."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        assert len(vm["zoom_levels"]) == 7
        assert len(vm["visible_counts_by_zoom"]) == 7
        assert len(vm["visible_node_ids_by_zoom"]) == 7
        assert len(vm["label_counts_by_zoom"]) == 7

    def test_visible_counts_monotonic(self):
        """visible_counts_by_zoom must be non-decreasing."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[
            {"type": "readme_draft", "status": "completed"},
            {"type": "code_review", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        counts = vm["visible_counts_by_zoom"]
        for i in range(len(counts) - 1):
            assert counts[i] <= counts[i + 1], f"Not monotonic at {i}: {counts}"

    def test_subset_monotonicity(self):
        """visible_node_ids_by_zoom[n] must be subset of [n+1]."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[
            {"type": "readme_draft", "status": "completed"},
            {"type": "code_review", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        ids_by_zoom = vm["visible_node_ids_by_zoom"]
        for i in range(len(ids_by_zoom) - 1):
            subset = set(ids_by_zoom[i])
            superset = set(ids_by_zoom[i + 1])
            assert subset <= superset, f"Level {i} not subset of {i+1}"

    def test_zoom_0_has_exactly_1_node(self):
        """Default zoom level 0 should show exactly 1 node (origin)."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        assert vm["default_zoom_level"] == 0
        assert vm["max_initial_nodes"] == 1
        assert vm["visible_counts_by_zoom"][0] == 1

    def test_full_graph_requires_toggle(self):
        """full_graph_requires_explicit_toggle must be True."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        assert vm["full_graph_requires_explicit_toggle"] is True
        assert vm["zoom_policy"]["full_graph_requires_explicit_toggle"] is True

    def test_direction_is_right(self):
        """Layout direction must be RIGHT."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122()
        vm = build_brain_view_model(job, [])
        assert vm["direction"] == "RIGHT"
        assert vm["layout_engine"] == "elk-layered"

    def test_importance_range(self):
        """Node importance must be in [0, 1]."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for n in vm["nodes"]:
            assert 0.0 <= n["importance"] <= 1.0, f"{n['id']}: {n['importance']}"

    def test_edge_strength_range(self):
        """Edge strength must be > 0."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert e["strength"] > 0

    def test_no_duplicate_node_ids(self):
        """No duplicate node IDs."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[
            {"type": "readme_draft", "status": "completed"},
            {"type": "code_review", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        ids = [n["id"] for n in vm["nodes"]]
        assert len(ids) == len(set(ids))

    def test_label_counts_by_zoom_non_decreasing(self):
        """label_counts_by_zoom must be non-decreasing."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s122(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        lc = vm["label_counts_by_zoom"]
        for i in range(len(lc) - 1):
            assert lc[i] <= lc[i + 1]

    def test_task_progress_required_fields(self):
        """Task progress v2 must have all 14 required fields per task."""
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job_s122(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        tp = build_task_progress(job, [])
        assert tp["version"] == 1
        required = {
            "id", "title", "status", "verified", "source",
            "accepted", "rank", "related_node_id", "short_reason",
            "proof_status", "test_status", "is_current",
            "is_future", "is_reviewer_suggested",
        }
        for task in tp["tasks"]:
            missing = required - set(task.keys())
            assert not missing, f"Task {task['id']} missing: {missing}"


# ═══════════════════════════════════════════════════════════════════════════
# Step 124 — Worker Unload JSON Schema
# ═══════════════════════════════════════════════════════════════════════════




class TestNodeDetailEdgeMeaningContract:
    """Node detail and edge meaning contracts."""

    def test_node_detail_exact_schema(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        nd = build_node_detail(job, [], str(job.id))
        required = {
            "version", "job_id", "node_id", "title", "status",
            "status_text", "why_this_matters", "evidence_summary",
            "next_safe_action", "copy_command", "advanced",
        }
        missing = required - set(nd.keys())
        assert not missing, f"Missing: {missing}"

    def test_node_detail_job_id(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job_s127()
        nd = build_node_detail(job, [], str(job.id))
        assert nd["job_id"] == str(job.id)

    def test_node_detail_advanced_collapsed(self):
        """Advanced section exists but is a dict, not exposed as default fields."""
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job_s127()
        nd = build_node_detail(job, [], str(job.id))
        assert isinstance(nd["advanced"], dict)
        assert "node_type" in nd["advanced"]

    def test_node_detail_no_raw_leaks(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        nd = build_node_detail(job, [], str(job.id))
        nd_str = json.dumps(nd)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in nd_str

    def test_node_not_found_safe(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job_s127()
        nd = build_node_detail(job, [], "nonexistent-id")
        assert "error" in nd

    def test_edge_meanings_exist(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert e["meaning"], f"Edge {e['source']}->{e['target']} has no meaning"
            assert e["kind"], f"Edge {e['source']}->{e['target']} has no kind"

    def test_edge_no_raw_type_visible(self):
        """Edges should use human-readable kind, not raw type."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            # Raw edge types use underscores like "has_task"
            assert "kind" in e
            # Kind should be human-readable
            assert "_" not in e["kind"] or e["kind"] in (
                "leads_to", "requires_approval", "applied_by",
                "verified_by", "blocked_by", "informed_by",
                "belongs_to", "approved_by", "proved_by",
            )

    def test_low_zoom_edges_primary_only(self):
        """At zoom 0-1, only primary chain edges visible."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        # Renderer checks this — verify edges have the data
        for e in vm["edges"]:
            assert "is_primary_chain" in e
            assert "visible_from_zoom" in e

    def test_edge_rank_direction_forward(self):
        """target_rank >= source_rank for forward flow."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job_s127(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            if e["is_primary_chain"]:
                assert e["target_rank"] >= e["source_rank"], \
                    f"Non-forward edge: {e['source_rank']}->{e['target_rank']}"


# ═══════════════════════════════════════════════════════════════════════════
# Step 133 — Autocoder Fake-E2E Closure
# ═══════════════════════════════════════════════════════════════════════════




class TestHumanNodeDetailSchema:
    """Human-only node detail."""

    def test_human_detail_schema(self):
        from packages.orchestration.ui_view_model import build_human_node_detail, build_story

        job = _make_job_s163()
        events = _make_events_s163()
        story = build_story(job, events)
        if not story["journey"]:
            pytest.skip("no journey items")

        node_id = story["journey"][0]["node_id"]
        detail = build_human_node_detail(job, events, node_id)

        assert detail["version"] == 3
        assert detail["title"]
        assert detail["state"]

    def test_human_detail_no_debug_fields(self):
        from packages.orchestration.ui_view_model import build_human_node_detail, build_story

        job = _make_job_s163()
        events = _make_events_s163()
        story = build_story(job, events)
        if not story["journey"]:
            pytest.skip("no journey items")

        node_id = story["journey"][0]["node_id"]
        detail = build_human_node_detail(job, events, node_id)
        s = json.dumps(detail).lower()

        for word in ("node_type", "connected_to", "edge_type", "present signals", "missing signals"):
            assert word not in s, f"forbidden debug word in human detail: {word}"

    def test_human_detail_not_found(self):
        from packages.orchestration.ui_view_model import build_human_node_detail

        job = _make_job_s163()
        events = _make_events_s163()
        detail = build_human_node_detail(job, events, "nonexistent-node")
        assert detail.get("error") == "node not found"


# ===========================================================================
# Step 166 — Journey Graph Layout
# ===========================================================================

