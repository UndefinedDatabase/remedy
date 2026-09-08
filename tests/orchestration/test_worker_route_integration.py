"""Worker Registry route-policy integration tests (Steps 1734/1736).

Builder-routing constraint, progress ledger items, feature suggestions, review-bundle section, and
cockpit section. All read-only; nothing executes a worker.
"""
from __future__ import annotations

from types import SimpleNamespace

from packages.orchestration.builder_routing import (
    BuilderRoutingTier,
    _route_policy_blocks_tier,
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


# ---------------------------------------------------------------------------
# Feature suggestions (Step 1728)
# ---------------------------------------------------------------------------


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
