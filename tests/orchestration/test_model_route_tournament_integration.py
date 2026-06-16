"""Model/Route Tournament integration tests (Steps 1814).

Builder-routing hint, progress ledger items, feature suggestions, review-bundle section, cockpit
section. All read-only; nothing executes a worker.
"""
from __future__ import annotations

import json
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


class TestProgressLedger:
    def test_items_from_report(self):
        from packages.orchestration.progress_ledger import extract_tournament_items
        rep = {"competitors": [{"competitor_id": "c1", "worker_id": "w1"}],
               "status": "insufficient_evidence", "winner_competitor_id": "", "confidence": "low"}
        items = {i.item_id for i in extract_tournament_items(rep)}
        assert "tournament-report-exists" in items
        assert "tournament-insufficient-evidence" in items

    def test_winner_item(self):
        from packages.orchestration.progress_ledger import extract_tournament_items
        rep = {"competitors": [{"competitor_id": "c1", "worker_id": "local.candidate_generator"}],
               "status": "complete", "winner_competitor_id": "c1", "confidence": "high"}
        items = {i.item_id for i in extract_tournament_items(rep)}
        assert "tournament-winner" in items

    def test_no_items_without_report(self):
        from packages.orchestration.progress_ledger import extract_tournament_items
        assert extract_tournament_items(None) == []


class TestFeatureSuggestions:
    def test_insufficient_evidence_suggestion(self):
        from packages.orchestration.feature_planner import build_feature_plan
        from packages.orchestration.progress_ledger import ProgressLedger, extract_tournament_items
        rep = {"competitors": [{"competitor_id": "c1", "worker_id": "w1"}],
               "status": "insufficient_evidence", "winner_competitor_id": "", "confidence": "low"}
        ledger = ProgressLedger(); ledger.items.extend(extract_tournament_items(rep))
        plan = build_feature_plan(ledger)
        titles = " ".join(s.title for s in plan.suggestions).lower()
        assert "evidence" in titles or "external builder" in titles
        for s in plan.suggestions:
            if s.source_refs and str(s.source_refs[0]).startswith("tournament-"):
                assert s.creates_proposed_task is False
                assert s.suggested_steps and s.priority

    def test_no_tournament_suggestions_without_items(self):
        from packages.orchestration.feature_planner import build_feature_plan
        from packages.orchestration.progress_ledger import ProgressLedger
        plan = build_feature_plan(ProgressLedger())
        for s in plan.suggestions:
            assert not (s.source_refs and str(s.source_refs[0]).startswith("tournament-"))


class TestSafeSurfaces:
    def _job(self):
        return SimpleNamespace(id=uuid4())

    def test_review_bundle_summary_safe(self, env):
        from packages.orchestration.review_bundle import _build_model_route_tournament_summary
        s = _build_model_route_tournament_summary(self._job())
        assert "latest_status" in s and "competitor_count" in s
        blob = json.dumps(s).lower()
        for marker in ("/home/", "sk-ant", "api_key", "-----begin"):
            assert marker not in blob

    def test_cockpit_section_readonly(self, env):
        from packages.orchestration.ui_server import _build_model_route_tournament_section
        s = _build_model_route_tournament_section(self._job())
        assert s["live"] is False
        assert s["source"] in ("model_route_tournament", "unavailable")
        assert "buttons" not in s and "actions" not in s
        assert " run" not in str(s.get("next_safe_action", ""))

    def test_cockpit_no_fake_winner(self, env):
        # Empty job → insufficient evidence → no recommended route claimed.
        from packages.orchestration.ui_server import _build_model_route_tournament_section
        s = _build_model_route_tournament_section(self._job())
        if s["source"] == "model_route_tournament":
            assert s["recommended_route"] == ""
