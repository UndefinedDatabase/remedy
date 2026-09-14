"""Overnight Mission integration tests (Steps 1847/1848/1849).

Progress ledger items, review-bundle section, cockpit section. All read-only; nothing executes.
"""
from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


class TestSafeSurfaces:
    def _job(self):
        return SimpleNamespace(id=uuid4())
