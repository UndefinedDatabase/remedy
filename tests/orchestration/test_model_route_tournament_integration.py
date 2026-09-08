"""Model/Route Tournament integration tests (Steps 1814).

Builder-routing hint, progress ledger items, feature suggestions, review-bundle section, cockpit
section. All read-only; nothing executes a worker.
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


class TestRoutingIntegration:
    def test_decision_carries_tournament(self, env):
        from packages.core.models import Job, RunState, Task
        from packages.orchestration.builder_routing import (
            BuilderRoutingRequest,
            export_builder_routing_json,
            select_builder_routing_decision,
        )
        from packages.orchestration.storage import save_job
        job = Job(id=uuid4(), name="t", user_prompt="x", state=RunState.RUNNING,
                  tasks=[Task(description="t")], artifacts=[], metadata={"target_repo": "."})
        save_job(job, root=env)
        d = select_builder_routing_decision(BuilderRoutingRequest(job_id=str(job.id)), data_dir=env)
        ex = export_builder_routing_json(d)
        assert "tournament" in ex
        t = ex["tournament"]
        assert "tournament_score_band" in t and t.get("estimated") is True
        assert " run" not in str(t.get("next_safe_action", ""))


class TestSafeSurfaces:
    def _job(self):
        return SimpleNamespace(id=uuid4())
