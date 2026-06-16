"""Tests for Feature Planner v0 — deterministic suggestions."""

from __future__ import annotations

import json

from packages.orchestration.feature_planner import (
    FeaturePlan,
    FeaturePlanPriority,
    FeaturePlanSource,
    FeatureSuggestion,
    accept_feature_suggestion,
    build_feature_plan,
    export_feature_plan_json,
    summarize_feature_plan,
)
from packages.orchestration.progress_ledger import (
    ProgressItem,
    ProgressLedger,
    ProgressSource,
    ProgressStatus,
)

# ---------------------------------------------------------------------------
# Step 1018: Deterministic rule tests
# ---------------------------------------------------------------------------


class TestBuildFeaturePlan:

    def test_open_blocker_generates_suggestion(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(
                item_id="R-0099",
                title="Critical security issue",
                status=ProgressStatus.BLOCKED,
                source_type=ProgressSource.LIVE_REVIEW_FINDING,
                severity="Blocker",
            ),
        ]
        plan = build_feature_plan(ledger)
        assert len(plan.suggestions) >= 1
        sug = plan.suggestions[0]
        assert sug.priority == FeaturePlanPriority.HIGH
        assert sug.source_type == FeaturePlanSource.OPEN_FINDING
        assert "R-0099" in sug.source_refs

    def test_known_risk_generates_suggestion(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(
                item_id="risk-1",
                title="test_full_chain_order fails on main",
                status=ProgressStatus.RISK,
                source_type=ProgressSource.KNOWN_RISK,
            ),
        ]
        plan = build_feature_plan(ledger)
        assert len(plan.suggestions) >= 1
        risk_sugs = [s for s in plan.suggestions if s.source_type in (FeaturePlanSource.KNOWN_RISK, FeaturePlanSource.FAILED_TEST)]
        assert len(risk_sugs) >= 1

    def test_all_clean_generates_roadmap(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(item_id="plan-1", status=ProgressStatus.DONE),
            ProgressItem(item_id="plan-2", status=ProgressStatus.DONE),
        ]
        plan = build_feature_plan(ledger)
        assert len(plan.suggestions) >= 2
        roadmap = [s for s in plan.suggestions if s.source_type == FeaturePlanSource.ROADMAP]
        assert len(roadmap) >= 2

    def test_no_duplicate_suggestions(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(item_id="R-1", title="same issue", status=ProgressStatus.BLOCKED, source_type=ProgressSource.LIVE_REVIEW_FINDING, severity="Blocker"),
            ProgressItem(item_id="R-2", title="same issue", status=ProgressStatus.BLOCKED, source_type=ProgressSource.LIVE_REVIEW_FINDING, severity="High"),
        ]
        plan = build_feature_plan(ledger)
        ids = [s.suggestion_id for s in plan.suggestions]
        assert len(ids) == len(set(ids))

    def test_deterministic_ordering(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(item_id="risk-1", title="low risk", status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK),
            ProgressItem(item_id="R-1", title="blocker", status=ProgressStatus.BLOCKED, source_type=ProgressSource.LIVE_REVIEW_FINDING, severity="Blocker"),
        ]
        plan = build_feature_plan(ledger)
        assert plan.suggestions[0].priority == FeaturePlanPriority.HIGH

    def test_stale_handoff_generates_suggestion(self):
        ledger = ProgressLedger()
        ledger.inconsistencies = ["Verdict says PASS but open blocker exists"]
        plan = build_feature_plan(ledger)
        stale = [s for s in plan.suggestions if s.source_type == FeaturePlanSource.STALE_HANDOFF]
        assert len(stale) == 1
        assert stale[0].priority == FeaturePlanPriority.HIGH

    def test_empty_ledger_gets_roadmap(self):
        ledger = ProgressLedger()
        plan = build_feature_plan(ledger)
        assert len(plan.suggestions) >= 3
        assert all(s.source_type == FeaturePlanSource.ROADMAP for s in plan.suggestions)

    def test_proof_gap_generates_suggestion(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(
                item_id="risk-gap-1",
                title="Proof gap: approval_pending",
                status=ProgressStatus.RISK,
                source_type=ProgressSource.PROOF_GAP,
            ),
        ]
        plan = build_feature_plan(ledger)
        gap_sugs = [s for s in plan.suggestions if s.source_type == FeaturePlanSource.PROOF_GAP]
        assert len(gap_sugs) == 1

    def test_snapshot_gap_is_high_priority(self):
        """Unverified snapshot apply → HIGH priority suggestion (Step 1148)."""
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(
                item_id="risk-snap-1",
                title="Apply without verified snapshot: abc12345-0",
                status=ProgressStatus.RISK,
                source_type=ProgressSource.PROOF_GAP,
                safe_summary="Intent abc12345-0 applied without snapshot_verified=True",
            ),
        ]
        plan = build_feature_plan(ledger)
        gap_sugs = [s for s in plan.suggestions if s.source_type == FeaturePlanSource.PROOF_GAP]
        assert len(gap_sugs) == 1
        assert gap_sugs[0].priority == FeaturePlanPriority.HIGH
        assert gap_sugs[0].estimated_risk == "high"


# ---------------------------------------------------------------------------
# Step 1020: Accept tests
# ---------------------------------------------------------------------------


class TestAcceptSuggestion:

    def test_accept_creates_metadata(self):
        plan = FeaturePlan()
        plan.suggestions = [
            FeatureSuggestion(
                suggestion_id="sug-test",
                title="Test suggestion",
                priority=FeaturePlanPriority.HIGH,
                source_type=FeaturePlanSource.OPEN_FINDING,
            ),
        ]
        result = accept_feature_suggestion(plan, "sug-test", "job-123")
        assert result["accepted"] is True
        assert result["suggestion_id"] == "sug-test"
        assert result["creates_proposed_task"] is True
        assert result["executed"] is False
        assert result["applied"] is False

    def test_invalid_suggestion_safe(self):
        plan = FeaturePlan()
        result = accept_feature_suggestion(plan, "nonexistent", "job-123")
        assert result["accepted"] is False
        assert "error" in result

    def test_no_execution(self):
        plan = FeaturePlan()
        plan.suggestions = [
            FeatureSuggestion(suggestion_id="sug-x", title="X"),
        ]
        result = accept_feature_suggestion(plan, "sug-x", "job-123")
        assert result["executed"] is False

    def test_duplicate_accept_safe(self):
        plan = FeaturePlan()
        plan.suggestions = [
            FeatureSuggestion(suggestion_id="sug-dup", title="Dup"),
        ]
        r1 = accept_feature_suggestion(plan, "sug-dup", "job-1")
        r2 = accept_feature_suggestion(plan, "sug-dup", "job-1")
        assert r1["accepted"] is True
        assert r2["accepted"] is True


# ---------------------------------------------------------------------------
# Export tests
# ---------------------------------------------------------------------------


class TestExportFeaturePlan:

    def test_export_json_structure(self):
        ledger = ProgressLedger()
        plan = build_feature_plan(ledger)
        data = export_feature_plan_json(plan)
        assert data["version"] == 0
        assert data["planner_version"] == "v0-deterministic"
        assert "suggestions" in data
        assert "suggestion_count" in data

    def test_export_json_parses(self):
        ledger = ProgressLedger()
        plan = build_feature_plan(ledger)
        data = export_feature_plan_json(plan)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert parsed["version"] == 0

    def test_suggestion_fields(self):
        ledger = ProgressLedger()
        plan = build_feature_plan(ledger)
        data = export_feature_plan_json(plan)
        sug = data["suggestions"][0]
        assert "suggestion_id" in sug
        assert "title" in sug
        assert "priority" in sug
        assert "source_type" in sug
        assert "next_action" in sug

    def test_summarize_text(self):
        ledger = ProgressLedger()
        plan = build_feature_plan(ledger)
        text = summarize_feature_plan(plan)
        assert "Feature Plan" in text
        assert "Suggestions:" in text
        assert "remedy feature accept" in text

    def test_no_raw_content(self):
        ledger = ProgressLedger()
        plan = build_feature_plan(ledger)
        data = export_feature_plan_json(plan)
        text = json.dumps(data)
        assert "raw_diff" not in text
        assert "__pycache__" not in text
        assert "Traceback" not in text


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:

    def test_priority_values(self):
        assert FeaturePlanPriority.HIGH.value == "high"
        assert FeaturePlanPriority.MEDIUM.value == "medium"
        assert FeaturePlanPriority.LOW.value == "low"

    def test_source_values(self):
        assert FeaturePlanSource.OPEN_FINDING.value == "open_finding"
        assert FeaturePlanSource.KNOWN_RISK.value == "known_risk"
        assert FeaturePlanSource.ROADMAP.value == "roadmap"

    def test_plan_defaults(self):
        plan = FeaturePlan()
        assert plan.version == 0
        assert plan.planner_version == "v0-deterministic"
        assert len(plan.suggestions) == 0
