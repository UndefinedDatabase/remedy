"""Tests: the worker guide, docs/system/worker.md.

The local queue, the worker loop and `worker status` it described were deleted (findings
R-0927 and R-0928); the guide stays as their record and must keep its two stances.
"""

from __future__ import annotations

from pathlib import Path


class TestWorkerDocs:
    def test_docs_exist(self):
        assert (Path(__file__).resolve().parents[2] / "docs" / "system" / "worker.md").exists()

    def test_docs_no_overnight_autonomy(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "system" / "worker.md").read_text()
        assert "not overnight" in text.lower() or "not autonomy" in text.lower()

    def test_docs_no_browser_actions(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "system" / "worker.md").read_text()
        assert "read-only" in text.lower()
