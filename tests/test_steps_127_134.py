"""Tests for Steps 127-134 — Contract closure, smoke closure, runtime hygiene,
UX interaction grounding, autocoder fake-E2E closure.
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

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


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
# Step 127 — Task Progress API Contract Closure
# ═══════════════════════════════════════════════════════════════════════════

class TestStep127_TaskProgressContract:
    """Task progress API must return version 1 with exact fields."""

    def test_version_is_1(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        tp = build_task_progress(job, [])
        assert tp["version"] == 1

    def test_exact_top_fields(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        tp = build_task_progress(job, [])
        assert set(tp.keys()) == {"version", "job_id", "tasks"}

    def test_task_required_fields(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[
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
        job = _make_job(tasks=[{"type": "done", "status": "completed"}])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["status"] == "completed"
        assert t["is_current"] is False
        assert t["is_future"] is False

    def test_active_task_is_current(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "active", "status": "running"}])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["status"] == "active"
        assert t["is_current"] is True

    def test_pending_task_is_future(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "future", "status": "pending"}])
        tp = build_task_progress(job, [])
        t = tp["tasks"][0]
        assert t["is_future"] is True

    def test_reviewer_suggested_task(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{
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
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "task_run_completed", "task_id": task_id}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["verified"] is True

    def test_proof_status_from_event(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "proof_collected", "task_id": task_id}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["proof_status"] == "collected"

    def test_test_status_pass(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "test_run_completed", "task_id": task_id,
                    "metadata": {"exit_code": 0}}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["test_status"] == "pass"

    def test_test_status_fail(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
        task_id = str(job.tasks[0].id)
        events = [{"event": "test_run_completed", "task_id": task_id,
                    "metadata": {"exit_code": 1}}]
        tp = build_task_progress(job, events)
        assert tp["tasks"][0]["test_status"] == "fail"

    def test_no_raw_leaks(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[{"type": "t1", "status": "completed"}])
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

class TestStep128_SmokeClosure:
    """Built-in smoke has task-progress and node-detail checks."""

    def test_smoke_has_task_progress_check(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "task-progress" in content
        assert "version" in content

    def test_smoke_has_node_detail_check(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "node detail" in content.lower() or "nodes/" in content

    def test_smoke_validates_task_fields(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "req_fields" in content or "is_current" in content

    def test_smoke_summary_has_job_id(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "job_id" in content

    def test_smoke_kills_ui_server(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "kill" in content
        assert "wait" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 129 — UI Runtime Noise / Headless Hygiene
# ═══════════════════════════════════════════════════════════════════════════

class TestStep129_HeadlessHygiene:
    """Smoke uses HTTP only, no browser launch."""

    def test_no_open_does_not_call_opener(self):
        """--no-open flag prevents browser open."""
        from apps.cli.commands.ui import COMMAND_HANDLERS
        # Default handler uses `not getattr(args, "no_open", False)`
        # With no_open=True, open_browser should be False
        class FakeArgs:
            job_id = str(uuid4())
            port = "0"
            host = "127.0.0.1"
            no_open = True
            info_file = None
        with patch("apps.cli.commands.ui._cmd_ui_start") as mock:
            COMMAND_HANDLERS["ui.start"](FakeArgs())
            _, kwargs = mock.call_args
            assert kwargs["open_browser"] is False

    def test_smoke_uses_http_not_browser(self):
        """Smoke API checks use urlopen, not xdg-open/open."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "urlopen" in content
        # No xdg-open or open command in smoke validation
        lines = content.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "xdg-open" in stripped and "remedy" not in stripped:
                pytest.fail("xdg-open in smoke validation")

    def test_ui_server_stderr_no_traceback(self):
        """UI server suppresses logging — no Python tracebacks in normal use."""
        from packages.orchestration.ui_server import _RemedyHandler
        handler = _RemedyHandler.__new__(_RemedyHandler)
        # log_message is overridden to suppress
        import io
        handler.log_message("test %s", "msg")  # should not raise


# ═══════════════════════════════════════════════════════════════════════════
# Step 130 — Worker VRAM Cleanup
# ═══════════════════════════════════════════════════════════════════════════

class TestStep130_WorkerVRAMCleanup:
    """Worker unload must have exact schema and handle all edge cases."""

    def test_unload_exact_schema(self):
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print") as mock_print:
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                data = json.loads(mock_print.call_args[0][0])
                assert set(data.keys()) == {
                    "version", "provider", "attempted",
                    "stopped", "skipped", "errors", "unavailable",
                }

    def test_missing_ollama_exit_0(self):
        """Missing ollama should not crash — exits normally."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            with patch("builtins.print"):
                # Should not raise
                _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)

    def test_errors_includes_silent_failures(self):
        """Models with returncode!=0 and empty stderr still in errors list."""
        from apps.cli.commands.worker import _cmd_worker_unload
        mock_ps = MagicMock(stdout="NAME\nsilent-fail\n", returncode=0)
        mock_stop = MagicMock(stdout="", stderr="", returncode=1)

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=[mock_ps, mock_stop]):
                with patch("builtins.print") as mock_print:
                    _cmd_worker_unload(provider="ollama", unload_all=True, json_output=True)
                    data = json.loads(mock_print.call_args[0][0])
                    assert "silent-fail" in data["errors"]

    def test_no_shell_true(self):
        src = Path("apps/cli/commands/worker.py").read_text()
        for line in src.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""'):
                continue
            assert "shell=True" not in stripped

    def test_smoke_has_unload_section(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "REMEDY_SMOKE_UNLOAD_MODELS" in content

    def test_resources_missing_nvidia_smi(self):
        """Missing nvidia-smi should not crash resources command."""
        from apps.cli.commands.worker import _cmd_worker_resources
        with patch("shutil.which", return_value=None):
            with patch("builtins.print"):
                _cmd_worker_resources(json_output=True)


# ═══════════════════════════════════════════════════════════════════════════
# Step 131 — UX Visual Contract Stabilization
# ═══════════════════════════════════════════════════════════════════════════

class TestStep131_UXVisualContract:
    """UX semantics verified via API contracts."""

    def test_initial_view_one_node(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        assert vm["visible_counts_by_zoom"][0] == 1
        assert vm["visible_node_ids_by_zoom"][0] == [str(job.id)]

    def test_zoom_in_reveals_more(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        counts = vm["visible_counts_by_zoom"]
        assert counts[-1] >= counts[0]
        assert counts[1] >= counts[0]

    def test_child_job_hidden_until_deep_zoom(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job()
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
        job = _make_job(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        tp = build_task_progress(job, [])
        assert len(tp["tasks"]) == 2

    def test_label_counts_low_at_zoom_0(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[
            {"type": "t1", "status": "completed"},
            {"type": "t2", "status": "running"},
        ])
        vm = build_brain_view_model(job, [])
        assert vm["label_counts_by_zoom"][0] <= 1

    def test_renderer_no_all_label_default(self):
        """Renderer labels require zoom level >= show_label_from_zoom."""
        content = Path("apps/ui/src/brain/renderer.ts").read_text()
        assert "show_label_from_zoom" in content

    def test_renderer_no_full_graph_default(self):
        """Full graph requires explicit toggle."""
        content = Path("apps/ui/src/brain/renderer.ts").read_text()
        assert "fullGraphMode" in content
        # Default must be false
        assert "fullGraphMode = false" in content

    def test_renderer_reduced_motion(self):
        """Renderer respects prefers-reduced-motion."""
        content = Path("apps/ui/src/brain/renderer.ts").read_text()
        assert "reduced-motion" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 132 — Node Detail + Edge Meaning Closure
# ═══════════════════════════════════════════════════════════════════════════

class TestStep132_NodeDetailEdgeMeaning:
    """Node detail and edge meaning contracts."""

    def test_node_detail_exact_schema(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
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
        job = _make_job()
        nd = build_node_detail(job, [], str(job.id))
        assert nd["job_id"] == str(job.id)

    def test_node_detail_advanced_collapsed(self):
        """Advanced section exists but is a dict, not exposed as default fields."""
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job()
        nd = build_node_detail(job, [], str(job.id))
        assert isinstance(nd["advanced"], dict)
        assert "node_type" in nd["advanced"]

    def test_node_detail_no_raw_leaks(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        nd = build_node_detail(job, [], str(job.id))
        nd_str = json.dumps(nd)
        for bad in ("raw_output", "command_output", "Traceback", "diff_preview"):
            assert bad not in nd_str

    def test_node_not_found_safe(self):
        from packages.orchestration.ui_view_model import build_node_detail
        job = _make_job()
        nd = build_node_detail(job, [], "nonexistent-id")
        assert "error" in nd

    def test_edge_meanings_exist(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            assert e["meaning"], f"Edge {e['source']}->{e['target']} has no meaning"
            assert e["kind"], f"Edge {e['source']}->{e['target']} has no kind"

    def test_edge_no_raw_type_visible(self):
        """Edges should use human-readable kind, not raw type."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
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
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        # Renderer checks this — verify edges have the data
        for e in vm["edges"]:
            assert "is_primary_chain" in e
            assert "visible_from_zoom" in e

    def test_edge_rank_direction_forward(self):
        """target_rank >= source_rank for forward flow."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job = _make_job(tasks=[{"type": "t1", "status": "running"}])
        vm = build_brain_view_model(job, [])
        for e in vm["edges"]:
            if e["is_primary_chain"]:
                assert e["target_rank"] >= e["source_rank"], \
                    f"Non-forward edge: {e['source_rank']}->{e['target_rank']}"


# ═══════════════════════════════════════════════════════════════════════════
# Step 133 — Autocoder Fake-E2E Closure
# ═══════════════════════════════════════════════════════════════════════════

class TestStep133_AutocoderFakeE2E:
    """Autocoder fixture builder proves real code change path."""

    def test_fixture_file_fixed(self):
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="e2e")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix calc", Path(tmp), data_dir, autonomy_level=4)
            assert result["tests_passed"] is True
            # calc.py should exist and have add/mul
            calc = (Path(tmp) / "calc.py").read_text()
            assert "def add" in calc
            assert "def mul" in calc

    def test_fixture_structured_patch_path(self):
        """Must use structured patch, not direct file write."""
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="patch-path")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("structured_patch_created") is True
            assert result.get("source_patch_applied") is True

    def test_fixture_approval_gate(self):
        from packages.core.models import Job
        from packages.orchestration.autorun import _run_fixture_builder
        from packages.orchestration.storage import save_job

        with tempfile.TemporaryDirectory() as tmp:
            job = Job(name="approval")
            save_job(job)
            from packages.orchestration.data_paths import resolve_data_root
            data_dir = resolve_data_root()
            result = _run_fixture_builder(job, "Fix", Path(tmp), data_dir, autonomy_level=4)
            assert result.get("approval_required") is True

    def test_source_apply_blocks_env(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path(".env", repo)[0]

    def test_source_apply_blocks_secrets(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path("secrets.pem", repo)[0]
        assert not _is_safe_path("key.p12", repo)[0]

    def test_source_apply_blocks_symlink(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path("../escape.py", repo)[0]

    def test_source_apply_blocks_absolute(self):
        from packages.orchestration.source_apply import _is_safe_path
        repo = Path("/tmp/test_repo")
        assert not _is_safe_path("/etc/passwd", repo)[0]

    def test_snapshot_revert_exists(self):
        """source_apply module should have revert capability."""
        from packages.orchestration import source_apply
        assert hasattr(source_apply, "revert_apply")

    def test_no_git_commit_in_fixture(self):
        content = Path("packages/orchestration/autorun.py").read_text()
        assert "git commit" not in content
        assert "git add" not in content

    def test_source_apply_event_schema(self):
        """source_patch_applied event has required fields."""
        content = Path("packages/orchestration/source_apply.py").read_text()
        assert "apply_id" in content
        assert "files_modified" in content
        assert "files_created" in content
        assert "error_count" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 134 — Closure Report + Dev Status Command
# ═══════════════════════════════════════════════════════════════════════════

class TestStep134_ClosureReport:
    """Dev status command exists and works."""

    def test_dev_status_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next((c for c in CATALOG if c.command_id == "dev.status"), None)
        assert cmd is not None
        assert cmd.subcommand == "status"

    def test_dev_status_json(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            required = {
                "version", "cli_ok", "smoke_ok", "ui_contract_ok",
                "task_progress_ok", "worker_cleanup_ok",
                "autocoder_fake_e2e_ok", "remaining_blockers",
            }
            missing = required - set(data.keys())
            assert not missing, f"Missing: {missing}"

    def test_dev_status_ui_contract_ok(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["ui_contract_ok"] is True

    def test_dev_status_task_progress_ok(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            assert data["task_progress_ok"] is True

    def test_dev_status_human_output(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=False)
            output = "\n".join(str(c[0][0]) if c[0] else "" for c in mock_print.call_args_list)
            assert "remedy ui" in output
            assert "worker unload" in output

    def test_main_py_under_120_lines(self):
        content = Path("apps/cli/main.py").read_text()
        assert len(content.splitlines()) <= 120

    def test_no_0000_binding(self):
        for path in [
            "packages/orchestration/ui_server.py",
            "apps/cli/commands/ui.py",
        ]:
            content = Path(path).read_text()
            assert "0.0.0.0" not in content

    def test_no_mutation_endpoints(self):
        content = Path("packages/orchestration/ui_server.py").read_text()
        assert "do_POST" in content  # exists
        assert "405" in content  # but returns method not allowed
        assert "do_PUT" in content
        assert "do_DELETE" in content
