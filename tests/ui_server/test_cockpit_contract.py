"""Operator Cockpit truth + read-only contract (Step 1190).

Guards that the read-only UI stays read-only (POST/PUT/DELETE -> 405) and that
the dashboard payload carries the cockpit truth sections with safe content only
(no paths, diffs, or tracebacks).
"""
from __future__ import annotations

import json

from packages.core.models import Job
from packages.orchestration.ui_server import _RemedyHandler, _build_dashboard


class TestReadOnlyMethods:
    def _capture(self):
        handler = _RemedyHandler.__new__(_RemedyHandler)
        captured: dict = {}
        handler._send_json = lambda code, data: captured.update(code=code, data=data)  # type: ignore[method-assign]
        return handler, captured

    def test_post_returns_405(self):
        handler, captured = self._capture()
        handler.do_POST()
        assert captured["code"] == 405

    def test_put_returns_405(self):
        handler, captured = self._capture()
        handler.do_PUT()
        assert captured["code"] == 405

    def test_delete_returns_405(self):
        handler, captured = self._capture()
        handler.do_DELETE()
        assert captured["code"] == 405


class TestDashboardCockpitContract:
    def test_has_cockpit_sections(self):
        dash = _build_dashboard(Job(name="contract"))
        assert "tests" in dash["metrics"]
        assert "proof" in dash["metrics"]
        assert "snapshot" in dash
        assert "continuation" in dash

    def test_snapshot_section_has_source(self):
        dash = _build_dashboard(Job(name="contract"))
        assert "source" in dash["snapshot"]

    def test_continuation_section_shape(self):
        dash = _build_dashboard(Job(name="contract"))
        for key in ("available", "last_result", "last_stop_reason"):
            assert key in dash["continuation"]

    def test_redaction_no_raw_content(self):
        payload = json.dumps(_build_dashboard(Job(name="contract")), default=str)
        assert "/home/" not in payload
        assert "Traceback" not in payload
        assert "diff --git" not in payload
