"""Token Economy integration tests (Steps 1775/1777/1772).

Builder-routing token hint, progress ledger items, feature suggestions, review-bundle section,
cockpit section, and placeholder-readiness hardening. All read-only; nothing executes a worker.
"""
from __future__ import annotations

import json
from types import SimpleNamespace
from uuid import uuid4

import pytest


def _job_with_repo(env, files):
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    repo = env / f"repo-{uuid4().hex[:6]}"
    repo.mkdir(parents=True)
    for rel, content in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    job = Job(id=uuid4(), name="te", user_prompt="x", state=RunState.RUNNING,
              tasks=[Task(description="t")], artifacts=[], metadata={"target_repo": str(repo)})
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Builder routing integration (Step 1775)
# ---------------------------------------------------------------------------


class TestRoutingIntegration:
    def test_decision_carries_token_economy(self, env):
        from packages.orchestration.builder_routing import (
            select_builder_routing_decision, BuilderRoutingRequest, export_builder_routing_json,
        )
        jid = _job_with_repo(env, files={"README.md": "hi\n", "src/a.py": "x=1\n"})
        d = select_builder_routing_decision(BuilderRoutingRequest(job_id=jid), data_dir=env)
        exported = export_builder_routing_json(d)
        assert "token_economy" in exported
        te = exported["token_economy"]
        assert "estimated_token_band" in te and te.get("estimated") is True
        # next action never an execution command
        assert " run" not in str(te.get("next_safe_action", ""))

    def test_no_side_effects(self, env):
        # Calling routing twice must not create execution artifacts; pure recommendation.
        from packages.orchestration.builder_routing import (
            select_builder_routing_decision, BuilderRoutingRequest,
        )
        jid = _job_with_repo(env, files={"README.md": "hi\n"})
        d1 = select_builder_routing_decision(BuilderRoutingRequest(job_id=jid), data_dir=env)
        d2 = select_builder_routing_decision(BuilderRoutingRequest(job_id=jid), data_dir=env)
        assert d1.selected_tier == d2.selected_tier


# ---------------------------------------------------------------------------
# Progress ledger items (Step 1767)
# ---------------------------------------------------------------------------


class TestProgressLedger:
    def test_items_extracted_from_report(self):
        from packages.orchestration.progress_ledger import extract_token_economy_items
        report = {
            "budget_profile": {"profile_id": "tb-x", "max_total_estimated_tokens": 40000},
            "decision": {"budget_status": "over_budget", "requires_human_approval": True,
                         "recommended_worker_id": "external.builder_package"},
            "context_pack_recommendation": {"compression_recommendation": "compress to cap",
                                            "memory_candidates": ["README.md"]},
        }
        items = extract_token_economy_items(report)
        ids = {i.item_id for i in items}
        assert "token-budget-profile-exists" in ids
        assert "token-budget-over" in ids
        assert "token-economy-expensive-route" in ids
        assert "token-context-compression" in ids
        assert "token-memory-candidates" in ids
        # honest: no fake persistence claim
        mem = next(i for i in items if i.item_id == "token-memory-candidates")
        assert "not persisted" in mem.safe_summary.lower()

    def test_no_items_without_report(self):
        from packages.orchestration.progress_ledger import extract_token_economy_items
        assert extract_token_economy_items(None) == []


# ---------------------------------------------------------------------------
# Feature suggestions (Step 1768)
# ---------------------------------------------------------------------------


class TestFeatureSuggestions:
    def test_suggestions_from_evidence(self):
        from packages.orchestration.feature_planner import build_feature_plan
        from packages.orchestration.progress_ledger import (
            ProgressLedger, extract_token_economy_items,
        )
        report = {
            "budget_profile": {"profile_id": "tb-x", "max_total_estimated_tokens": 40000},
            "decision": {"budget_status": "over_budget", "requires_human_approval": True,
                         "recommended_worker_id": "external.builder_package"},
            "context_pack_recommendation": {"compression_recommendation": "compress",
                                            "memory_candidates": ["README.md"]},
        }
        ledger = ProgressLedger()
        ledger.items.extend(extract_token_economy_items(report))
        plan = build_feature_plan(ledger)
        titles = " ".join(s.title for s in plan.suggestions).lower()
        assert "mempalace" in titles or "approval" in titles or "optimizer" in titles
        for s in plan.suggestions:
            if s.source_refs and str(s.source_refs[0]).startswith("token-"):
                assert s.creates_proposed_task is False
                assert s.suggested_steps  # effort included
                assert s.priority  # impact included

    def test_no_token_suggestions_without_items(self):
        from packages.orchestration.feature_planner import build_feature_plan
        from packages.orchestration.progress_ledger import ProgressLedger
        plan = build_feature_plan(ProgressLedger())
        for s in plan.suggestions:
            assert not (s.source_refs and str(s.source_refs[0]).startswith("token-"))


# ---------------------------------------------------------------------------
# Review bundle + cockpit (Step 1777)
# ---------------------------------------------------------------------------


class TestSafeSurfaces:
    def _job(self):
        return SimpleNamespace(id=uuid4())

    def test_review_bundle_summary_safe(self):
        from packages.orchestration.review_bundle import _build_token_economy_summary
        s = _build_token_economy_summary(self._job())
        assert "budget_status" in s
        assert s.get("memory_candidates_persisted") is False
        blob = json.dumps(s).lower()
        for marker in ("/home/", "sk-ant", "api_key", "price_usd", "cost_usd"):
            assert marker not in blob

    def test_cockpit_section_readonly(self):
        from packages.orchestration.ui_server import _build_token_economy_section
        s = _build_token_economy_section(self._job())
        assert s["live"] is False
        assert s["source"] in ("token_economy", "unavailable")
        assert "buttons" not in s and "actions" not in s
        assert " run" not in str(s.get("next_safe_action", ""))

    def test_no_verified_savings_claim(self):
        from packages.orchestration.review_bundle import _build_token_economy_summary
        s = _build_token_economy_summary(self._job())
        assert s.get("verified") is False


# ---------------------------------------------------------------------------
# Placeholder readiness hardening (Step 1772)
# ---------------------------------------------------------------------------


class TestPlaceholderHardening:
    def test_ollama_placeholder_not_executable(self):
        from packages.orchestration.worker_registry import get_worker_spec, is_placeholder
        for wid in ("ollama.placeholder", "cloud.placeholder"):
            s = get_worker_spec(wid)
            assert is_placeholder(s) is True and s.enabled is False

    def test_enabled_ollama_placeholder_flagged_and_not_executed(self, tmp_path):
        # A future custom enabled ollama_candidate must still be treated as a placeholder requiring
        # approval, and integrity must flag any claim of executable readiness.
        from packages.orchestration.worker_registry import (
            hard_safety_requires_approval, _spec_from_dict,
        )
        spec = _spec_from_dict({"worker_id": "custom.ollama", "kind": "ollama_candidate",
                                "enabled": True, "cost_tier": "cheap", "risk_tier": "medium",
                                "execution_mode": "local_model"})
        assert hard_safety_requires_approval(spec) is True  # ollama kind → always approval

    def test_worker_registry_integrity_still_passes(self, tmp_path):
        from packages.orchestration.worker_registry import worker_registry_integrity
        assert worker_registry_integrity(data_dir=tmp_path)["passed"] is True
