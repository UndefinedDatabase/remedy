"""Worker Registry route-policy integration tests (Steps 1734/1736).

Builder-routing constraint, progress ledger items, feature suggestions, review-bundle section, and
cockpit section. All read-only; nothing executes a worker.
"""
from __future__ import annotations

from types import SimpleNamespace

from packages.orchestration.builder_routing import (
    BuilderRoutingTier, _route_policy_blocks_tier,
)
from packages.orchestration.worker_registry import default_route_policy, save_route_policy


# ---------------------------------------------------------------------------
# Builder routing constraint (Step 1734)
# ---------------------------------------------------------------------------


class TestRoutingPolicyConstraint:
    def test_default_policy_is_noop(self, tmp_path):
        blocked, why = _route_policy_blocks_tier(
            "jobX", BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR, tmp_path)
        assert blocked is False and why == ""

    def test_blocked_local_worker_blocks_local_tier(self, tmp_path):
        p = default_route_policy("jobY")
        p.blocked_worker_ids = ["local.candidate_generator"]
        save_route_policy(p, data_dir=tmp_path)
        blocked, why = _route_policy_blocks_tier(
            "jobY", BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR, tmp_path)
        assert blocked is True
        assert "local.candidate_generator" in why

    def test_user_selecting_other_worker_blocks_external_tier(self, tmp_path):
        p = default_route_policy("jobZ")
        p.user_selected_worker_ids = ["human.operator"]
        save_route_policy(p, data_dir=tmp_path)
        blocked, why = _route_policy_blocks_tier(
            "jobZ", BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR, tmp_path)
        assert blocked is True

    def test_no_job_is_noop(self, tmp_path):
        blocked, why = _route_policy_blocks_tier(
            "", BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR, tmp_path)
        assert blocked is False


# ---------------------------------------------------------------------------
# Progress ledger items (Step 1727)
# ---------------------------------------------------------------------------


class TestProgressLedgerItems:
    def test_registry_items_extracted(self):
        from packages.orchestration.progress_ledger import extract_worker_registry_items
        from packages.orchestration.worker_registry import load_worker_registry, default_route_policy
        registry = load_worker_registry()
        policy = default_route_policy("j")
        items = extract_worker_registry_items(registry, policy)
        ids = {i.item_id for i in items}
        assert "worker-registry-available" in ids
        # No fake "running" state.
        for i in items:
            assert "running" not in i.safe_summary.lower() or "no worker is running" in i.safe_summary.lower()

    def test_no_items_without_registry(self):
        from packages.orchestration.progress_ledger import extract_worker_registry_items
        assert extract_worker_registry_items([], None) == []


# ---------------------------------------------------------------------------
# Feature suggestions (Step 1728)
# ---------------------------------------------------------------------------


class TestFeatureSuggestions:
    def test_suggestions_only_with_evidence(self):
        from packages.orchestration.feature_planner import build_feature_plan
        from packages.orchestration.progress_ledger import (
            ProgressLedger, extract_worker_registry_items,
        )
        from packages.orchestration.worker_registry import load_worker_registry, default_route_policy
        ledger = ProgressLedger()
        ledger.items.extend(extract_worker_registry_items(load_worker_registry(),
                                                          default_route_policy("j")))
        plan = build_feature_plan(ledger)
        titles = " ".join(s.title for s in plan.suggestions).lower()
        assert "tournament" in titles or "ollama" in titles
        # Suggestions don't auto-create execution.
        for s in plan.suggestions:
            if s.source_refs and s.source_refs[0].startswith(("worker-registry", "route-policy")):
                assert s.creates_proposed_task is False

    def test_no_registry_suggestions_without_items(self):
        from packages.orchestration.feature_planner import build_feature_plan
        from packages.orchestration.progress_ledger import ProgressLedger
        plan = build_feature_plan(ProgressLedger())
        for s in plan.suggestions:
            assert not (s.source_refs and str(s.source_refs[0]).startswith("worker-registry"))


# ---------------------------------------------------------------------------
# Review bundle + cockpit sections (Step 1729/1730)
# ---------------------------------------------------------------------------


class TestSafeSurfaces:
    def _job(self):
        from uuid import uuid4
        return SimpleNamespace(id=uuid4())

    def test_review_bundle_summary_safe(self):
        from packages.orchestration.review_bundle import _build_worker_registry_summary
        s = _build_worker_registry_summary(self._job())
        assert "enabled_workers" in s
        assert "route_policy" in s
        blob = str(s).lower()
        for marker in ("/home/", "/users/", "sk-ant", "sk-proj", "api_key", "-----begin", "secret_key"):
            assert marker not in blob, marker

    def test_cockpit_section_is_readonly(self):
        from packages.orchestration.ui_server import _build_worker_registry_section
        s = _build_worker_registry_section(self._job())
        assert s["live"] is False
        assert s["source"] in ("worker_registry", "unavailable")
        # No mutation/run affordances.
        assert "run" not in {k.lower() for k in s.keys()}
