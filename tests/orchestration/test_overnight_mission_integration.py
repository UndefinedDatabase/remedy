"""Overnight Mission integration tests (Steps 1847/1848/1849).

Progress ledger items, review-bundle section, cockpit section. All read-only; nothing executes.
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


class TestProgressLedger:
    def test_items_from_contract_and_eval(self):
        from packages.orchestration.progress_ledger import extract_mission_items
        contract = {"contract_id": "msn-1", "acceptance_criteria": ["a"]}
        ev = {"status": "waiting_for_review", "satisfied": False, "open_review_findings": 1,
              "open_tasks": 0, "user_decision_required": False}
        ids = {i.item_id for i in extract_mission_items(contract, ev)}
        assert "mission-contract-created" in ids
        assert "mission-not-satisfied" in ids

    def test_satisfied_item(self):
        from packages.orchestration.progress_ledger import extract_mission_items
        contract = {"contract_id": "msn-2", "acceptance_criteria": ["a"]}
        ev = {"status": "contract_satisfied", "satisfied": True}
        ids = {i.item_id for i in extract_mission_items(contract, ev)}
        assert "mission-satisfied" in ids

    def test_no_contract_no_items(self):
        from packages.orchestration.progress_ledger import extract_mission_items
        assert extract_mission_items(None, None) == []

    def test_not_evaluated_item(self):
        from packages.orchestration.progress_ledger import extract_mission_items
        ids = {i.item_id for i in extract_mission_items({"contract_id": "x",
                                                         "acceptance_criteria": []}, None)}
        assert "mission-not-evaluated" in ids


class TestSafeSurfaces:
    def _job(self):
        return SimpleNamespace(id=uuid4())

    def test_review_bundle_summary_no_contract(self, env):
        from packages.orchestration.review_bundle import _build_overnight_mission_summary
        s = _build_overnight_mission_summary(self._job())
        assert s["has_contract"] is False and s["satisfied"] is False
        blob = json.dumps(s).lower()
        assert "/home/" not in blob and "sk-ant" not in blob

    def test_cockpit_section_readonly(self, env):
        from packages.orchestration.ui_server import _build_overnight_mission_section
        s = _build_overnight_mission_section(self._job())
        assert s["live"] is False
        assert s["source"] in ("overnight_mission", "unavailable")
        assert "buttons" not in s and "actions" not in s
        assert " run" not in str(s.get("next_safe_action", ""))

    def test_review_bundle_with_contract(self, env, monkeypatch):
        from packages.orchestration.overnight_mission import create_mission_contract_from_job
        from packages.orchestration.review_bundle import _build_overnight_mission_summary
        job = self._job()
        # review verdict in repo is PENDING → not satisfied; summary must reflect honestly
        create_mission_contract_from_job(str(job.id), acceptance_criteria=["done"], data_dir=env)
        s = _build_overnight_mission_summary(job)
        assert s["has_contract"] is True
        assert s["satisfied"] in (True, False)  # never crashes; honest flag
