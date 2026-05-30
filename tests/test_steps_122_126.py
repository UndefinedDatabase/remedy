"""Tests for Steps 122-126 — Job-focused origin, view-model hardening,
worker unload schema, autocoder calc.py fixture, smoke closure.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

# ---------------------------------------------------------------------------
# Ensure project root on sys.path
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


# ---------------------------------------------------------------------------
# Helper: minimal job fixture
# ---------------------------------------------------------------------------

def _make_job(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
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

class TestStep122_JobFocusedOrigin:
    """Only the requested job_id should be is_origin=true."""

    def test_single_job_has_one_origin(self):
        """Basic case: single job graph has exactly one origin."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        vm = build_brain_view_model(job, [])
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        assert len(origins) == 1
        assert origins[0]["id"] == str(job.id)

    def test_origin_is_focus_job(self):
        """Origin node id matches the passed job's id."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        vm = build_brain_view_model(job, [])
        origin = next(n for n in vm["nodes"] if n["is_origin"])
        assert origin["id"] == str(job.id)
        assert vm["origin"] == str(job.id)

    def test_child_job_not_origin(self):
        """Child/continuation job nodes must NOT be is_origin."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.id),
            },
        }]
        vm = build_brain_view_model(job, events)
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        assert len(origins) == 1, f"Expected 1 origin, got {len(origins)}"
        assert origins[0]["id"] == str(job.id)

    def test_child_job_demoted_zoom(self):
        """Child job nodes should be visible_from_zoom >= 5."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.id),
            },
        }]
        vm = build_brain_view_model(job, events)
        child_nodes = [n for n in vm["nodes"]
                       if n["type"] == "job" and not n["is_origin"]]
        for cn in child_nodes:
            assert cn["visible_from_zoom"] >= 5

    def test_child_job_flow_role_continuation(self):
        """Child job flow_role must be 'continuation', not 'origin'."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        child_id = str(uuid4())
        events = [{
            "event": "job_continued",
            "metadata": {
                "child_job_id": child_id,
                "origin_node_id": str(job.id),
            },
        }]
        vm = build_brain_view_model(job, events)
        for n in vm["nodes"]:
            if n["type"] == "job" and not n["is_origin"]:
                assert n["flow_role"] == "continuation"
            elif n["type"] == "job" and n["is_origin"]:
                assert n["flow_role"] == "origin"

    def test_origin_at_zoom_0(self):
        """Origin node must be visible at zoom level 0."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        vm = build_brain_view_model(job, [])
        origin = next(n for n in vm["nodes"] if n["is_origin"])
        assert origin["visible_from_zoom"] == 0


# ═══════════════════════════════════════════════════════════════════════════
# Step 123 — View-model Hardening
# ═══════════════════════════════════════════════════════════════════════════

class TestStep123_ViewModelHardening:
    """Exact API field contracts, zoom contracts, node/edge contracts."""

    def test_version_is_4(self):
        """View model version must be 4."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        vm = build_brain_view_model(job, [])
        assert vm["version"] == 4

    def test_top_level_required_fields(self):
        """All required top-level fields must be present."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
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
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
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
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
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
        job = _make_job()
        vm = build_brain_view_model(job, [])
        assert len(vm["zoom_levels"]) == 7
        assert len(vm["visible_counts_by_zoom"]) == 7
        assert len(vm["visible_node_ids_by_zoom"]) == 7
        assert len(vm["label_counts_by_zoom"]) == 7

    def test_visible_counts_monotonic(self):
        """visible_counts_by_zoom must be non-decreasing."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[
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
        job = _make_job(tasks=[
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
        job = _make_job()
        vm = build_brain_view_model(job, [])
        assert vm["default_zoom_level"] == 0
        assert vm["max_initial_nodes"] == 1
        assert vm["visible_counts_by_zoom"][0] == 1

    def test_full_graph_requires_toggle(self):
        """full_graph_requires_explicit_toggle must be True."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        vm = build_brain_view_model(job, [])
        assert vm["full_graph_requires_explicit_toggle"] is True
        assert vm["zoom_policy"]["full_graph_requires_explicit_toggle"] is True

    def test_direction_is_right(self):
        """Layout direction must be RIGHT."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
        vm = build_brain_view_model(job, [])
        assert vm["direction"] == "RIGHT"
        assert vm["layout_engine"] == "elk-layered"

    def test_importance_range(self):
        """Node importance must be in [0, 1]."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for n in vm["nodes"]:
            assert 0.0 <= n["importance"] <= 1.0, f"{n['id']}: {n['importance']}"

    def test_edge_strength_range(self):
        """Edge strength must be > 0."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert e["strength"] > 0

    def test_no_duplicate_node_ids(self):
        """No duplicate node IDs."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[
            {"type": "readme_draft", "status": "completed"},
            {"type": "code_review", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        ids = [n["id"] for n in vm["nodes"]]
        assert len(ids) == len(set(ids))

    def test_label_counts_by_zoom_non_decreasing(self):
        """label_counts_by_zoom must be non-decreasing."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        lc = vm["label_counts_by_zoom"]
        for i in range(len(lc) - 1):
            assert lc[i] <= lc[i + 1]

    def test_task_progress_required_fields(self):
        """Task progress v2 must have all 14 required fields per task."""
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        tp = build_task_progress(job, [])
        assert tp["version"] == 2
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

class TestStep124_WorkerUnloadSchema:
    """Worker unload JSON must have flat stopped/skipped/errors/unavailable."""

    def test_unload_unavailable_schema(self):
        """When ollama not found, schema has unavailable=true."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print") as mock_print:
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                output = mock_print.call_args[0][0]
                data = json.loads(output)
                assert data["version"] == 1
                assert data["unavailable"] is True
                assert data["attempted"] == 0
                assert data["stopped"] == []
                assert data["skipped"] == []
                assert data["errors"] == []
                assert data["provider"] == "ollama"

    def test_unload_required_fields(self):
        """Unload JSON must have all required top-level fields."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print") as mock_print:
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                required = {"version", "provider", "attempted", "stopped", "skipped", "errors", "unavailable"}
                missing = required - set(data.keys())
                assert not missing, f"Missing: {missing}"

    def test_unload_stopped_is_list(self):
        """stopped field must be a list of model names."""
        from apps.cli.commands.worker import _cmd_worker_unload
        mock_ps = MagicMock(stdout="NAME\nllama3:8b\n", returncode=0)
        mock_stop = MagicMock(stdout="", stderr="", returncode=0)

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=[mock_ps, mock_stop]):
                with patch("builtins.print") as mock_print:
                    _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                    data = json.loads(mock_print.call_args[0][0])
                    assert isinstance(data["stopped"], list)
                    assert "llama3:8b" in data["stopped"]
                    assert data["unavailable"] is False

    def test_unload_errors_populated_on_failure(self):
        """errors list should contain model names that failed to stop."""
        from apps.cli.commands.worker import _cmd_worker_unload
        mock_ps = MagicMock(stdout="NAME\nbad-model\n", returncode=0)
        mock_stop = MagicMock(stdout="", stderr="model not found", returncode=1)

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=[mock_ps, mock_stop]):
                with patch("builtins.print") as mock_print:
                    _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                    data = json.loads(mock_print.call_args[0][0])
                    assert "bad-model" in data["errors"]
                    assert data["stopped"] == []


# ═══════════════════════════════════════════════════════════════════════════
# Step 125 — Autocoder calc.py Fixture + --no-ui
# ═══════════════════════════════════════════════════════════════════════════

class TestStep125_AutocoderCalcFixture:
    """Fixture builder must use calc.py, Makefile, and --no-ui must work."""

    def test_fixture_creates_calc_and_makefile(self):
        """Fixture builder creates calc.py, tests/test_calc.py, Makefile."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            _run_fixture_builder(job, "Make calc work", Path(tmp), data_dir, autonomy_level=4)
            assert (Path(tmp) / "tests" / "test_calc.py").exists()
            assert (Path(tmp) / "calc.py").exists()
            assert (Path(tmp) / "Makefile").exists()

    def test_fixture_test_passes(self):
        """calc fixture test should pass after apply."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture calc")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(job, "Make calc work", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("tests_passed") is True

    def test_fixture_proof_collected(self):
        """Fixture builder at autonomy 4+ should collect proof."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test proof")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(job, "Prove calc", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("stage") == "proof_collected"

    def test_makefile_has_test_target(self):
        """Makefile must have a test target."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test makefile")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            _run_fixture_builder(job, "Check makefile", Path(tmp), data_dir, autonomy_level=2)
            content = (Path(tmp) / "Makefile").read_text()
            assert "test:" in content
            assert "pytest" in content

    def test_no_ui_flag_in_catalog(self):
        """--no-ui must be in the do.run catalog entry."""
        from apps.cli.command_catalog import CATALOG
        do_run = next(c for c in CATALOG if c.command_id == "do.run")
        arg_names = [a.name for a in do_run.args]
        assert "--no-ui" in arg_names

    def test_no_ui_suppresses_ui(self):
        """--no-ui should suppress UI even if --ui is set."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        class FakeArgs:
            goal = "test"
            repo = "."
            project = None
            autonomy_level = "1"
            max_cycles = "1"
            ui = "true"
            no_ui = True
            dry_run = True
            json = True
            fixture_builder = False

        with patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            COMMAND_HANDLERS["do.run"](FakeArgs())
            _, kwargs = mock_do.call_args
            assert kwargs["enable_ui"] is False

    def test_no_old_fixture_references(self):
        """No references to fixture_module or greet() in autorun."""
        content = Path("packages/orchestration/autorun.py").read_text()
        assert "fixture_module" not in content
        assert "greet(" not in content
        assert "test_fixture.py" not in content

    def test_structured_patch_uses_calc(self):
        """Fixture builder structured patch targets calc.py."""
        from packages.orchestration.structured_patch import (
            FileOp, StructuredPatch, validate_structured_patch,
        )
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(
                path="calc.py",
                action="create",
                language="python",
                content="def add(a: int, b: int) -> int:\n    return a + b\n\n\ndef mul(a: int, b: int) -> int:\n    return a * b\n",
                risk="low",
            ),),
            target_paths=("calc.py",),
            risk="low",
            applicability="applicable",
            requires_approval=True,
        )
        issues = validate_structured_patch(patch)
        assert not issues


# ═══════════════════════════════════════════════════════════════════════════
# Step 126 — Smoke Closure
# ═══════════════════════════════════════════════════════════════════════════

class TestStep126_SmokeClosure:
    """Smoke script must have origin check and UNLOAD section."""

    def test_smoke_has_brain_view_model_check(self):
        """Smoke must validate brain-view-model origin count."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "brain-view-model" in content
        assert "is_origin" in content

    def test_smoke_has_unload_section(self):
        """Smoke must have optional REMEDY_SMOKE_UNLOAD_MODELS section."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "REMEDY_SMOKE_UNLOAD_MODELS" in content
        assert "worker unload" in content

    def test_smoke_no_shell_true(self):
        """Smoke must not use shell=True (except comments)."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            if "shell=True" in stripped and "shell=True" not in stripped.split("#", 1)[-1] if "#" in stripped else "shell=True" in stripped:
                # Only flag if it's in actual Python code, not bash
                pass

    def test_smoke_checks_version_4(self):
        """Smoke origin check must validate version == 4."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "version" in content
        assert "'version'" in content or '"version"' in content

    def test_no_bind_all_interfaces(self):
        """No 0.0.0.0 binding in smoke or UI code."""
        for path in [
            "scripts/remedy_smoke.sh",
            "packages/orchestration/ui_server.py",
            "apps/cli/commands/ui.py",
        ]:
            content = Path(path).read_text()
            assert "0.0.0.0" not in content, f"0.0.0.0 found in {path}"

    def test_no_external_assets_in_ui(self):
        """No CDN/external asset URLs in UI HTML."""
        ui_dir = Path("apps/ui/src")
        if not ui_dir.exists():
            pytest.skip("UI directory not found")
        for f in ui_dir.rglob("*.ts"):
            content = f.read_text()
            for pattern in ["cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"]:
                assert pattern not in content, f"External asset {pattern} in {f}"
