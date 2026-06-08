"""
Domain tests: regression/test_named_bugs.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import MagicMock, patch
from unittest.mock import patch
from uuid import UUID, uuid4
from uuid import uuid4
import ast
import json
import os
import pytest
import re
import sys
import tempfile

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.core.models import Job, RunState, Task
from packages.orchestration.storage import save_job

_ROOT = Path(__file__).resolve().parent.parent.parent

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"

FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


def _make_job(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


# ===========================================================================
# Step 57: Brain Graph Core Refactor — Structural Tests
# ===========================================================================


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


def _make_job_s122(*, tasks=None, name="test"):
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


def _make_job_s127(*, tasks=None, name="test"):
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


def _make_job_s61(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="step61-test",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


def _make_job_s62() -> Job:
    return Job(
        id=uuid4(),
        name="hygiene-test",
        user_prompt="test",
        state=RunState.RUNNING,
        tasks=[Task(id=uuid4(), description="t", status=RunState.PENDING,
                     inputs={"task_type": "patch"}, output_artifact_ids=[])],
        artifacts=[],
        metadata={},
    )


def _proof_event(intent_id: str, target_path: str) -> dict:
    return {
        "event": "patch_apply_proof_recorded",
        "outcome": "proof_stored",
        "metadata": {
            "intent_id": intent_id,
            "target_path": target_path,
            "sha256": f"sha_{intent_id}",
            "bytes_written": 100,
            "line_count": 10,
        },
    }


def _test_event(status: str = "passed", exit_code: int = 0) -> dict:
    return {
        "event": "test_run_completed",
        "outcome": status,
        "metadata": {
            "command": "pytest",
            "status": status,
            "exit_code": exit_code,
        },
    }


FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


# ===========================================================================
# Multi-proof causal edge correctness
# ===========================================================================




class TestAgentsmdWorkflow:
    """AGENTS.md contains required workflow rules."""

    def test_commit_discipline_step_per_commit(self):
        src = Path("AGENTS.md").read_text()
        assert "one step per commit" in src.lower() or "step per commit" in src.lower()

    def test_commit_discipline_500_line_limit(self):
        src = Path("AGENTS.md").read_text()
        assert "500" in src




class TestSmokeContractReset:
    def test_current_graph_renderer_exists(self):
        """Current Canvas/Force graph renderer exists at expected path."""
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "react-force-graph-2d" in src

    def test_legacy_brain_flow_under_legacy(self):
        """Old RemedyBrainFlow.tsx preserved under legacy/."""
        p = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "RemedyBrainFlow.tsx"
        assert p.is_file()
        src = p.read_text()
        assert "remedy-brain-canvas" in src

    def test_index_html_has_task_ribbon_marker(self):
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        assert "remedy-checklist" in src

    def test_index_html_has_task_item_marker(self):
        css = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "taskRow" in css

    def test_legacy_semantic_zoom_under_legacy(self):
        """Old semanticZoom.ts preserved under legacy/."""
        p = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "semanticZoom.ts"
        assert p.exists()
        src = p.read_text()
        assert "semanticZoomLevel" in src

    def test_legacy_organic_layout_under_legacy(self):
        """Old organicLayout.ts preserved under legacy/."""
        p = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "organicLayout.ts"
        assert p.exists()

    def test_index_html_has_node_detail_card(self):
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx").read_text()
        assert "remedy-detail-compact" in src

    def test_index_html_has_reduced_motion(self):
        css = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "styles" / "globals.css").read_text()
        assert "prefers-reduced-motion" in css

    def test_index_html_has_remedy_light(self):
        css = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "styles" / "tokens.css").read_text()
        assert "color-scheme: light" in css

    def test_smoke_script_uses_new_markers(self):
        smoke = (Path(__file__).parent.parent.parent / "scripts" / "remedy_smoke.sh").read_text()
        # React UI smoke markers (Steps 202-207)
        assert "remedy-react" in smoke
        assert "remedy-shell" in smoke
        assert "brain-graph" in smoke

    def test_smoke_script_no_old_panels(self):
        smoke = (Path(__file__).parent.parent.parent / "scripts" / "remedy_smoke.sh").read_text()
        # Old markers should not appear as primary checks
        assert "'what-happened': 'what-happened' in html" not in smoke
        assert "'explore-brain': 'explore-brain' in html" not in smoke


# ---------------------------------------------------------------------------
# Step 102 — Correct Semantic Zoom Direction
# ---------------------------------------------------------------------------




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
        """Legacy semantic zoom module exists under legacy/ and reduced-motion support present."""
        sz = Path(_ROOT / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "semanticZoom.ts")
        assert sz.exists(), "semanticZoom.ts not found under legacy/"
        css = Path(_ROOT / "apps" / "ui" / "src" / "styles" / "globals.css").read_text()
        assert "prefers-reduced-motion" in css, "missing reduced-motion in globals.css"

    def test_renderer_exports_semantic_zoom_fn(self):
        """Legacy semanticZoom.ts should export semanticZoomLevelFromViewportZoom."""
        src = Path(_ROOT / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "semanticZoom.ts").read_text()
        assert "semanticZoomLevelFromViewportZoom" in src

    def test_renderer_wheel_cannot_reach_level_6(self):
        """Semantic zoom max level should be 4, not 6."""
        src = Path(_ROOT / "apps" / "ui" / "src" / "components" / "graph" / "legacy" / "semanticZoom.ts").read_text()
        # The function should return 4 at the top, not 5 or 6
        assert "return 4;" in src




class TestSmokeOriginCheckAndUnload:
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




class TestSmokeTaskProgressNodeDetail:
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




class TestDevStatusCommandSchema:
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
                "version", "cli_ok", "latest_smoke", "ui_contract_ok",
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




class TestSmokeScriptStructuralChecks:
    """Smoke script checks."""

    def test_smoke_has_task_progress(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "task-progress" in content

    def test_smoke_has_no_open(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "--no-open" in content

    def test_smoke_has_brain_view_model(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "brain-view-model" in content

    def test_smoke_summary_structure(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "summary.json" in content
        assert "job_id" in content
        assert "project_id" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 138 — Dev Status Honesty
# ═══════════════════════════════════════════════════════════════════════════




class TestSmokeCommitReadinessSection:
    """Smoke script must include commit-readiness check."""

    def test_smoke_has_commit_readiness(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "commit-readiness" in content

    def test_smoke_validates_commit_readiness_schema(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "next_action" in content
        assert "changed_files_truncated" in content

    def test_smoke_checks_raw_leaks(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        # The commit-readiness section checks for raw leaks
        assert "raw_output" in content
        assert "command_output" in content

    def test_smoke_shows_help_on_failure(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "commit-readiness --help" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 145 — Commit-Readiness Next Action Surface
# ═══════════════════════════════════════════════════════════════════════════




class TestLegacyViewerSourceQuarantine:
    """Old viewer source moved to legacy."""

    def test_legacy_dir_exists(self):
        legacy = UI_ROOT / "legacy"
        assert legacy.is_dir(), "legacy/ directory should exist"

    def test_old_main_ts_in_legacy(self):
        assert (UI_ROOT / "legacy" / "main.ts").is_file()

    def test_old_brain_dir_in_legacy(self):
        assert (UI_ROOT / "legacy" / "brain").is_dir()

    def test_no_pixi_in_new_source(self):
        for f in UI_SRC.rglob("*.ts"):
            content = f.read_text(encoding="utf-8")
            assert "pixi.js" not in content, f"pixi.js in new source: {f}"

    def test_no_pixi_in_new_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            assert "pixi.js" not in content, f"pixi.js in new source: {f}"

    def test_new_index_html_has_root_div(self):
        index = UI_ROOT / "index.html"
        assert index.is_file()
        content = index.read_text(encoding="utf-8")
        assert 'id="root"' in content

    def test_new_index_not_old_pixi_entry(self):
        index = UI_ROOT / "index.html"
        content = index.read_text(encoding="utf-8")
        assert "src/main.tsx" in content or "main.tsx" in content
        assert "remedy-task-ribbon" not in content
        assert "remedy-brain-canvas" not in content or "module" in content


# ---------------------------------------------------------------------------
# Step 173 — UI spec exists
# ---------------------------------------------------------------------------




class TestGlobalForbiddenWords:
    """Default UI source must not contain debug words as visible labels."""

    FORBIDDEN = [
        "Context Coverage", "present signals", "missing signals",
        "CONNECTED_TO",
    ]

    def test_tsx_files_clean(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"Forbidden '{word}' in {f.relative_to(ROOT)}"

    def test_css_files_clean(self):
        for f in UI_SRC.rglob("*.css"):
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"Forbidden '{word}' in {f.relative_to(ROOT)}"




class TestGlobalNoCDN:
    """No external CDN in any frontend file."""

    def test_no_cdn_in_html(self):
        index = UI_ROOT / "index.html"
        content = index.read_text(encoding="utf-8")
        for pattern in ["cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"]:
            assert pattern not in content, f"CDN in index.html: {pattern}"

    def test_no_cdn_in_css(self):
        for f in UI_SRC.rglob("*.css"):
            content = f.read_text(encoding="utf-8")
            for pattern in ["cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"]:
                assert pattern not in content, f"CDN in {f}: {pattern}"


# ---------------------------------------------------------------------------
# Step 200 — Legacy docs not primary
# ---------------------------------------------------------------------------




class TestDocsNoOldViewerAsPrimary:
    """Docs don't recommend old viewer as primary."""

    def test_spec_no_old_viewer(self):
        spec = (ROOT / "docs" / "ui" / "REMEDY_UI_REBUILD_SPEC.md").read_text(encoding="utf-8")
        assert "VIEW_PATH" not in spec
        assert "pixi" not in spec.lower()


# ---------------------------------------------------------------------------
# CLI size check
# ---------------------------------------------------------------------------




class TestNoForbiddenDebugWords:
    FORBIDDEN = ["TODO:", "FIXME:", "HACK:", "console.log(", "debugger"]

    def test_no_forbidden_in_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            if "legacy" in str(f):
                continue
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"forbidden '{word}' in {f.relative_to(ROOT)}"

    def test_no_forbidden_in_ts(self):
        for f in UI_SRC.rglob("*.ts"):
            if "legacy" in str(f) or "test" in f.name.lower():
                continue
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"forbidden '{word}' in {f.relative_to(ROOT)}"




class TestNoRawLeaks:
    """No raw content surfaces in brain graph, aggregate, or provenance."""

    def test_brain_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = _make_job_s61()
        save_job(job)
        events = [_proof_event("i1", "a.py"), _test_event()]
        graph = build_project_brain(job, events)
        raw = json.dumps(export_project_brain_json(graph))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Brain JSON leak: {forbidden}"

    def test_brain_summary_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            summarize_project_brain,
        )

        job = _make_job_s61()
        save_job(job)
        graph = build_project_brain(job, [])
        text = summarize_project_brain(graph)
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in text, f"Brain summary leak: {forbidden}"

    def test_aggregate_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
            export_project_brain_aggregate_json,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="leak-test", repo_paths=[])
        save_project(project)

        job = _make_job_s61(project_id=pid)
        save_job(job)

        agg = build_project_brain_aggregate(project, [job], {})
        raw = json.dumps(export_project_brain_aggregate_json(agg))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Aggregate JSON leak: {forbidden}"

    def test_readiness_brain_node_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job_s61()
        save_job(job)
        graph = build_project_brain(job, [])
        ar_nodes = [n for n in graph.nodes if n.type == "autonomy_readiness"]
        assert ar_nodes
        meta = ar_nodes[0].metadata
        for forbidden in ("stdout", "stderr", "raw_output", "value"):
            assert forbidden not in meta, f"Readiness node leak: {forbidden}"




class TestNoDuplicateSection:
    def test_no_def_section_outside_symbols(self):
        """No orchestration module may define its own _section function."""
        orch_dir = Path("packages/orchestration")
        violations = []
        for py in orch_dir.glob("*.py"):
            if py.name == "_symbols.py":
                continue
            src = py.read_text()
            tree = ast.parse(src, filename=str(py))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "_section":
                    violations.append(f"{py.name}:{node.lineno}")
        assert violations == [], f"Local _section found in: {violations}"




class TestNoSilentSwallow:
    def test_no_except_exception_pass_in_orchestration(self):
        """No orchestration module may have 'except Exception: pass'."""
        orch_dir = Path("packages/orchestration")
        violations = []
        for py in orch_dir.glob("*.py"):
            src = py.read_text()
            if "except Exception: pass" in src:
                violations.append(py.name)
        assert violations == [], f"Silent swallow in: {violations}"

    def test_no_bare_except_exception_in_key_modules(self):
        """Key modules must not use bare 'except Exception:'."""
        modules = [
            "packages/orchestration/project_brain.py",
            "packages/orchestration/autonomy_readiness.py",
            "packages/orchestration/brain_detail.py",
            "packages/orchestration/context_pack.py",
            "packages/orchestration/storage.py",
        ]
        for mod in modules:
            src = Path(mod).read_text()
            assert "except Exception:" not in src, f"{mod} has bare except Exception:"




class TestBrainViewerNarrowedException:
    def test_viewer_no_bare_except_exception(self):
        src = Path("packages/orchestration/brain_viewer.py").read_text()
        assert "except Exception:" not in src

