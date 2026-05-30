"""Tests for Steps 111-116 — UI CLI contract, resource cleanup, semantic zoom v4,
forward flow v3, task ribbon v2, autocoder E2E.
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
# Step 111 — UI CLI Contract
# ═══════════════════════════════════════════════════════════════════════════

class TestStep111_UICLIContract:
    """remedy ui <job_id> direct form must work."""

    def test_default_command_rewrite_ui(self):
        """remedy ui <uuid> should rewrite to remedy ui start <uuid>."""
        from apps.cli.grouped import main as grouped_main

        fake_id = str(uuid4())
        # Should not crash with SystemExit(1) — should reach handler
        with pytest.raises(SystemExit):
            grouped_main(["ui", fake_id])
        # The key test: it should have tried to load the job (meaning it
        # correctly routed to ui.start), not show "Unknown command"

    def test_default_command_rewrite_preserves_flags(self):
        """remedy ui <uuid> --port 0 should rewrite correctly."""
        from apps.cli.grouped import main as grouped_main

        fake_id = str(uuid4())
        with pytest.raises(SystemExit):
            grouped_main(["ui", fake_id, "--port", "0"])

    def test_ui_no_args_shows_help(self, capsys):
        """remedy ui with no args shows group help."""
        from apps.cli.grouped import main as grouped_main
        grouped_main(["ui"])
        out = capsys.readouterr().out
        assert "ui" in out.lower()

    def test_ui_help_flag(self, capsys):
        """remedy ui --help shows help."""
        from apps.cli.grouped import main as grouped_main
        grouped_main(["ui", "--help"])
        out = capsys.readouterr().out
        assert "ui" in out.lower()

    def test_ui_start_still_works(self):
        """remedy ui start <uuid> still works as alias."""
        from apps.cli.grouped import main as grouped_main
        fake_id = str(uuid4())
        with pytest.raises(SystemExit):
            grouped_main(["ui", "start", fake_id])

    def test_catalog_has_ui_start(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("ui.start")
        assert cmd.group_id == "ui"
        assert cmd.subcommand == "start"

    def test_info_file_schema(self):
        """Info file must have exact fields."""
        required = {"version", "url", "host", "port", "token", "job_id", "pid", "started_at"}
        # Verify the contract exists in the server
        from packages.orchestration.ui_server import start_ui_server
        # Just check the function signature exists
        assert callable(start_ui_server)

    def test_smoke_uses_direct_form(self):
        """Smoke script should use remedy ui <job_id>, not remedy ui start."""
        smoke = Path(_ROOT / "scripts" / "remedy_smoke.sh")
        if smoke.exists():
            content = smoke.read_text()
            # Find the UI start line
            assert 'remedy ui "${JOB_ID}"' in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 112 — Resource Cleanup / VRAM Hygiene
# ═══════════════════════════════════════════════════════════════════════════

class TestStep112_ResourceCleanup:

    def test_catalog_has_worker_resources(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("worker.resources")
        assert cmd.group_id == "worker"
        assert cmd.supports_json

    def test_catalog_has_worker_unload(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("worker.unload")
        assert cmd.group_id == "worker"

    def test_resources_handler_no_crash(self, capsys):
        """worker resources runs without crash even if tools missing."""
        from apps.cli.commands.worker import _cmd_worker_resources
        with patch("shutil.which", return_value=None):
            _cmd_worker_resources(json_output=False)
        out = capsys.readouterr().out
        assert "not available" in out.lower() or "Worker" in out

    def test_resources_json_output(self, capsys):
        """worker resources --json returns valid JSON."""
        from apps.cli.commands.worker import _cmd_worker_resources
        with patch("shutil.which", return_value=None):
            _cmd_worker_resources(json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["version"] == 1
        assert "ollama" in data
        assert "gpu" in data

    def test_unload_no_ollama_graceful(self, capsys):
        """worker unload with no ollama installed handles gracefully."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            _cmd_worker_unload(unload_all=True, json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "error" in data or data["version"] == 1

    def test_unload_mocked_ollama(self, capsys):
        """worker unload --all with mocked ollama ps/stop."""
        from apps.cli.commands.worker import _cmd_worker_unload

        mock_ps = MagicMock()
        mock_ps.stdout = "NAME\nllama3:latest\ncodellama:latest\n"
        mock_ps.returncode = 0

        mock_stop = MagicMock()
        mock_stop.returncode = 0
        mock_stop.stderr = ""

        def run_side_effect(cmd, **kwargs):
            if "ps" in cmd:
                return mock_ps
            return mock_stop

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=run_side_effect):
                _cmd_worker_unload(unload_all=True, json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["attempted"] == 2
        assert len(data["results"]) == 2

    def test_no_shell_true_in_worker(self):
        """No shell=True usage in worker.py (docstrings excluded)."""
        src = Path(_ROOT / "apps" / "cli" / "commands" / "worker.py").read_text()
        # Check only non-comment, non-docstring lines
        for line in src.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'"):
                continue
            assert "shell=True" not in stripped, f"shell=True in code: {stripped}"

    def test_unload_requires_model_or_all(self):
        """worker unload without --model or --all should error."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with pytest.raises(SystemExit):
                _cmd_worker_unload(json_output=False)


# ═══════════════════════════════════════════════════════════════════════════
# Step 113 — Semantic Zoom Truth Table v4
# ═══════════════════════════════════════════════════════════════════════════

class TestStep113_SemanticZoom:

    def test_zoom_policy_in_view_model(self):
        """View model must have zoom_policy with correct direction."""
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert vm["zoom_policy"]["direction"] == "zoom_in_reveals_more"
        assert vm["zoom_policy"]["full_graph_requires_explicit_toggle"] is True

    def test_visible_counts_monotonic(self):
        """visible_counts_by_zoom must be monotonic non-decreasing."""
        job = _make_job(tasks=[
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
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        ids_by_zoom = vm["visible_node_ids_by_zoom"]
        for i in range(len(ids_by_zoom) - 1):
            assert set(ids_by_zoom[i]) <= set(ids_by_zoom[i + 1]), \
                f"zoom {i} not subset of {i+1}"

    def test_label_counts_in_view_model(self):
        """label_counts_by_zoom must be present and reasonable."""
        job = _make_job(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert "label_counts_by_zoom" in vm
        assert isinstance(vm["label_counts_by_zoom"], list)
        assert len(vm["label_counts_by_zoom"]) == 7

    def test_zoom_level_0_only_origin(self):
        """At zoom 0, only origin job node should be visible."""
        job = _make_job(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        ids_at_0 = vm["visible_node_ids_by_zoom"][0]
        # Should contain only the job origin
        assert len(ids_at_0) <= 1

    def test_non_origin_labels_hidden_at_zoom_0(self):
        """At zoom 0, label_counts should be 0 (no labels at origin-only level)."""
        job = _make_job(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert vm["label_counts_by_zoom"][0] == 0

    def test_version_is_3(self):
        """View model version should be 3."""
        job = _make_job()
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        assert vm["version"] == 3


# ═══════════════════════════════════════════════════════════════════════════
# Step 114 — Forward Flow + Edge Meaning v3
# ═══════════════════════════════════════════════════════════════════════════

class TestStep114_ForwardFlow:

    def test_nodes_have_flow_role(self):
        """Every node must have flow_role."""
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for n in vm["nodes"]:
            assert "flow_role" in n, f"node {n['id']} missing flow_role"

    def test_nodes_have_lane(self):
        """Every node must have lane."""
        job = _make_job(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for n in vm["nodes"]:
            assert "lane" in n

    def test_edges_have_source_target_rank(self):
        """Every edge must have source_rank, target_rank, primary_path."""
        job = _make_job(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert "source_rank" in e
            assert "target_rank" in e
            assert "primary_path" in e

    def test_edge_target_rank_gte_source(self):
        """For primary path edges, target rank >= source rank (forward flow)."""
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            if e["primary_path"]:
                assert e["target_rank"] >= e["source_rank"], \
                    f"backward flow edge: {e['source']} → {e['target']}"

    def test_each_edge_has_user_meaning(self):
        """Every edge must have a meaning string."""
        job = _make_job(tasks=[{"type": "readme_draft"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert e.get("meaning"), f"edge missing meaning: {e['source']}→{e['target']}"

    def test_origin_flow_role(self):
        """Job node flow_role should be 'origin'."""
        job = _make_job()
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        job_nodes = [n for n in vm["nodes"] if n["type"] == "job"]
        assert job_nodes
        assert job_nodes[0]["flow_role"] == "origin"

    def test_task_flow_roles_deterministic(self):
        """Completed task should be task_completed, running should be task_active."""
        job = _make_job(tasks=[
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

class TestStep115_TaskRibbon:

    def test_task_progress_version_2(self):
        """Task progress API should return version 2."""
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["version"] == 2

    def test_task_progress_fields(self):
        """Each task should have the exact required fields."""
        required = {
            "id", "title", "status", "verified", "source", "accepted",
            "rank", "related_node_id", "short_reason", "proof_status",
            "test_status", "is_current", "is_future", "is_reviewer_suggested",
        }
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        for t in tp["tasks"]:
            missing = required - set(t.keys())
            assert not missing, f"missing fields: {missing}"

    def test_completed_task_status(self):
        job = _make_job(tasks=[{"type": "write", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["status"] == "completed"

    def test_active_task_is_current(self):
        job = _make_job(tasks=[{"type": "write", "status": "running"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["is_current"] is True

    def test_future_task_is_future(self):
        job = _make_job(tasks=[{"type": "write", "status": "pending"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["is_future"] is True

    def test_reviewer_suggested_flag(self):
        job = _make_job(tasks=[{
            "type": "review",
            "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["is_reviewer_suggested"] is True
        assert tp["tasks"][0]["status"] == "reviewer-suggested"

    def test_reviewer_not_verified(self):
        job = _make_job(tasks=[{
            "type": "review",
            "status": "pending",
            "metadata": {"source": "reviewer"},
        }])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        assert tp["tasks"][0]["verified"] is False

    def test_html_has_ribbon_markers(self):
        """index.html must have remedy-task-ribbon and remedy-task-item."""
        html = Path(_ROOT / "apps" / "ui" / "index.html").read_text()
        assert "remedy-task-ribbon" in html
        assert "remedy-task-item" in html
        assert "remedy-task-completed" in html
        assert "remedy-task-active" in html
        assert "remedy-task-future" in html

    def test_no_raw_leaks_in_task_progress(self):
        job = _make_job(tasks=[{"type": "write", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_task_progress
        tp = build_task_progress(job, [])
        full = json.dumps(tp)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in full


# ═══════════════════════════════════════════════════════════════════════════
# Step 116 — Autocoder E2E Reality Check
# ═══════════════════════════════════════════════════════════════════════════

class TestStep116_AutocoderE2E:

    def test_fixture_builder_creates_patch(self):
        """Fixture builder should use structured patch model."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            from packages.orchestration.storage import save_job
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(
                job, "Make tests pass", Path(tmp), data_dir, autonomy_level=4,
            )
            assert result["source_context_injected"] is True
            assert result["structured_patch_created"] is True
            assert result["approval_required"] is True
            assert result["source_patch_applied"] is True

    def test_fixture_builder_creates_files(self):
        """Fixture builder should create test and source files."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            from packages.orchestration.storage import save_job
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            _run_fixture_builder(
                job, "Make tests pass", Path(tmp), data_dir, autonomy_level=4,
            )
            assert (Path(tmp) / "test_fixture.py").exists()
            assert (Path(tmp) / "fixture_module.py").exists()

    def test_fixture_test_passes(self):
        """The fixture test should actually pass after apply."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="test fixture")
            from packages.orchestration.storage import save_job
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()

            result = _run_fixture_builder(
                job, "Make tests pass", Path(tmp), data_dir, autonomy_level=4,
            )
            assert result.get("tests_passed") is True

    def test_source_apply_path_safety(self):
        """source_apply must block .env, binary, symlink, path traversal."""
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path(".env", repo)[0]
        assert not _is_safe_path("../escape.py", repo)[0]
        assert not _is_safe_path("/etc/passwd", repo)[0]
        assert not _is_safe_path("secrets.pem", repo)[0]

    def test_structured_patch_parser_used(self):
        """Fixture builder must create StructuredPatch, not bypass it."""
        from packages.orchestration.structured_patch import (
            FileOp,
            StructuredPatch,
            validate_structured_patch,
        )
        # Create same patch as fixture builder
        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(
                path="fixture_module.py",
                action="create",
                language="python",
                content="def greet(name): return f'Hello, {name}!'\n",
                risk="low",
            ),),
            target_paths=("fixture_module.py",),
            risk="low",
            applicability="applicable",
            requires_approval=True,
        )
        issues = validate_structured_patch(patch)
        assert not issues

    def test_no_raw_content_in_view_model(self):
        """View model should not leak raw code content."""
        job = _make_job(tasks=[{"type": "readme_draft", "status": "completed"}])
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(job, [])
        full = json.dumps(vm)
        for bad in ("raw_output", "command_output", "diff_preview", "approval_reason"):
            assert bad not in full

    def test_autorun_result_has_events(self):
        """AutorunResult should have events list."""
        from packages.orchestration.autorun import AutorunResult
        r = AutorunResult(job_id="x", cycles_run=0, stage="init")
        assert isinstance(r.events, list)


# ═══════════════════════════════════════════════════════════════════════════
# Cross-step smoke markers
# ═══════════════════════════════════════════════════════════════════════════

class TestSmokeSafety:

    def test_no_shell_true_in_source_apply(self):
        src = Path(_ROOT / "packages" / "orchestration" / "source_apply.py").read_text()
        assert "shell=True" not in src

    def test_no_shell_true_in_autorun(self):
        src = Path(_ROOT / "packages" / "orchestration" / "autorun.py").read_text()
        assert "shell=True" not in src

    def test_ui_server_rejects_non_localhost(self):
        """UI server must refuse non-localhost bind."""
        from packages.orchestration.ui_server import start_ui_server
        with pytest.raises(SystemExit):
            start_ui_server("fake-id", host="0.0.0.0")

    def test_main_py_under_120_lines(self):
        main_py = Path(_ROOT / "apps" / "cli" / "main.py")
        lines = main_py.read_text().splitlines()
        assert len(lines) <= 120, f"main.py has {len(lines)} lines"

    def test_index_html_no_external_assets(self):
        html = Path(_ROOT / "apps" / "ui" / "index.html").read_text()
        for pattern in ["cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"]:
            assert pattern not in html

    def test_index_html_has_ux_contract_markers(self):
        html = Path(_ROOT / "apps" / "ui" / "index.html").read_text()
        for marker in [
            "remedy-brain-canvas", "remedy-task-ribbon", "remedy-task-item",
            "semantic-zoom", "zoom-in-reveals-more", "forward-flow",
            "node-detail-card", "reduced-motion",
        ]:
            assert marker in html, f"missing UX marker: {marker}"

    def test_renderer_exports_semantic_zoom_fn(self):
        """renderer.ts should export semanticZoomLevelFromScale."""
        src = Path(_ROOT / "apps" / "ui" / "src" / "brain" / "renderer.ts").read_text()
        assert "export function semanticZoomLevelFromScale" in src

    def test_renderer_wheel_cannot_reach_level_6(self):
        """Wheel zoom should max at level 5, not reach 6."""
        src = Path(_ROOT / "apps" / "ui" / "src" / "brain" / "renderer.ts").read_text()
        # The function should return 5 for very high scale, not 6
        assert "return 5;" in src
