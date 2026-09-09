"""Worker Registry route-policy integration tests (Steps 1734/1736).

What still lives here after the prototype-cluster deletion: the read-only worker-registry
cockpit section. Remedy deliberately does not test a builder-routing policy constraint any
more — that module and its route-policy consultation were deleted by F275.
"""
from __future__ import annotations

from types import SimpleNamespace

# ---------------------------------------------------------------------------
# Review bundle + cockpit sections (Step 1729/1730)
# ---------------------------------------------------------------------------


class TestSafeSurfaces:
    def _job(self):
        from uuid import uuid4
        return SimpleNamespace(id=uuid4())

    def test_cockpit_section_is_readonly(self):
        from packages.orchestration.ui_server import _build_worker_registry_section
        s = _build_worker_registry_section(self._job())
        assert s["live"] is False
        assert s["source"] in ("worker_registry", "unavailable")
        # No mutation/run affordances.
        assert "run" not in {k.lower() for k in s.keys()}
