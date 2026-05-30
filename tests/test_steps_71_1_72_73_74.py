"""Tests for Steps 71.1, 72, 73, 74 — Token Policy Applied, Visual System, Viewer Shell, UX Gate."""

from __future__ import annotations

import re
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


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


class TestTokenPolicyAppliedSchema:
    def test_schema_in_registry(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        assert "token_policy_applied" in EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["token_policy_applied"]
        assert len(schema) == 6
        expected = {"mode", "max_context_tokens", "estimated_context_tokens",
                    "local_first", "remote_model_requires_approval", "selected_worker"}
        assert schema == frozenset(expected)

    def test_autonomy_loop_emits(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)

        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        events = load_run_events(resolve_data_root(), job.id)
        tpa = [e for e in events if e.get("event") == "token_policy_applied"]
        assert len(tpa) >= 1
        meta = tpa[0].get("metadata", {})
        from packages.orchestration.event_schemas import validate_event_metadata
        errors = validate_event_metadata("token_policy_applied", meta)
        assert errors == [], f"Schema errors: {errors}"

    def test_event_ledger_includes_tpa(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)

        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.event_ledger import list_events
        from packages.orchestration.timeline import load_run_events

        run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        events = load_run_events(resolve_data_root(), job.id)
        ledger = list_events(str(job.id), events)
        tpa_ledger = [e for e in ledger if e.event_type == "token_policy_applied"]
        assert len(tpa_ledger) >= 1


# ── Step 72: Visual System ──────────────────────────────────────────────


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


class TestBrainViewerShell:
    def _get_html(self):
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data, write_brain_viewer_files,
        )
        from packages.orchestration.project_brain import build_project_brain
        import tempfile
        from pathlib import Path

        job = _make_job()
        events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.id),
                    "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
        graph = build_project_brain(job, events)
        data = build_brain_viewer_data(job, graph, events)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            html_path = write_brain_viewer_files(data, out)
            return html_path.read_text()

    def test_viewer_html_has_shell(self):
        html = self._get_html()
        assert "remedy-shell" in html

    def test_viewer_html_has_data_island(self):
        html = self._get_html()
        assert 'type="application/json"' in html

    def test_viewer_html_static_fallback(self):
        html = self._get_html()
        assert "static-fallback" in html

    def test_viewer_html_no_external_assets(self):
        html = self._get_html()
        # Allow data: URIs but no external
        urls = re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\s]+)', html)
        assert urls == [], f"external URLs found: {urls}"

    def test_viewer_html_no_trademark(self):
        html = self._get_html().lower()
        assert "assassin" not in html
        assert "abstergo" not in html

    def test_viewer_html_no_raw_leaks(self):
        html = self._get_html()
        for forbidden in ("stdout", "stderr", "raw_output", "Traceback",
                          "diff_preview", "approval_reason"):
            assert forbidden not in html

    def test_viewer_html_reduced_motion(self):
        html = self._get_html()
        assert "prefers-reduced-motion" in html

    def test_viewer_html_has_proof_chain(self):
        html = self._get_html()
        assert "remedy-proof-chain" in html or "proof-chain" in html

    def test_viewer_html_has_decision_panel(self):
        html = self._get_html()
        assert "remedy-decision-panel" in html or "decision-panel" in html

    def test_viewer_html_has_readiness_panel(self):
        html = self._get_html()
        assert "remedy-readiness-panel" in html or "readiness-panel" in html

    def test_viewer_html_has_timeline(self):
        html = self._get_html()
        assert "remedy-timeline" in html or "timeline" in html

    def test_viewer_html_has_node_detail(self):
        html = self._get_html()
        # Detail panel must exist
        assert "detail" in html.lower()

    def test_viewer_html_has_error_panel(self):
        html = self._get_html()
        assert "err-panel" in html or "error" in html.lower()

    def test_viewer_data_valid_json(self):
        import json
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data, export_brain_viewer_json,
        )
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        graph = build_project_brain(job, [])
        data = build_brain_viewer_data(job, graph, [])
        j = export_brain_viewer_json(data)
        s = json.dumps(j)
        parsed = json.loads(s)
        assert "graph" in parsed
        assert "node_details" in parsed


# ── Step 74: UX Quality Gate ────────────────────────────────────────────


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
