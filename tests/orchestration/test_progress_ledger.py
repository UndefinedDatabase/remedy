"""Tests for Progress Ledger v1 — structured checklist from plan/live_review/risks."""

from __future__ import annotations

import json

from packages.orchestration.progress_ledger import (
    ProgressItem,
    ProgressLedger,
    ProgressSource,
    ProgressStatus,
    build_progress_ledger,
    build_progress_ledger_from_plan,
    export_progress_ledger_json,
    merge_known_risks,
    merge_live_review_findings,
    summarize_progress_ledger,
)

# ---------------------------------------------------------------------------
# Step 1012: Plan parsing tests
# ---------------------------------------------------------------------------


SAMPLE_PLAN = """\
# Plan — Steps 1010-1029: Progress Ledger v1

## Goal
Create structured progress ledger.

## Current Step
1015

## Steps
- [x] 1010: Handoff cleanup
- [x] 1011: Define Progress Ledger model
- [x] 1012: Build ledger from plan.md
- [ ] 1013: Build ledger from live_review.md
- [ ] 1014: Build ledger from known risks
- [x] 1015: CLI: progress checklist — skipped (deferred to v2)

## Pre-existing Issue
`test_full_chain_order` fails on main.
"""


class TestBuildFromPlan:

    def test_checked_steps_become_done(self):
        ledger = build_progress_ledger_from_plan(SAMPLE_PLAN)
        done = [i for i in ledger.items if i.status == ProgressStatus.DONE]
        assert len(done) == 3
        assert done[0].item_id == "plan-1010"
        assert done[1].item_id == "plan-1011"
        assert done[2].item_id == "plan-1012"

    def test_unchecked_steps_become_planned(self):
        ledger = build_progress_ledger_from_plan(SAMPLE_PLAN)
        planned = [i for i in ledger.items if i.status == ProgressStatus.PLANNED]
        assert len(planned) == 2
        assert planned[0].item_id == "plan-1013"

    def test_skipped_steps_become_skipped(self):
        ledger = build_progress_ledger_from_plan(SAMPLE_PLAN)
        skipped = [i for i in ledger.items if i.status == ProgressStatus.SKIPPED]
        assert len(skipped) == 1
        assert "skipped" in skipped[0].title.lower() or "deferred" in skipped[0].title.lower()

    def test_scope_extracted(self):
        ledger = build_progress_ledger_from_plan(SAMPLE_PLAN)
        assert "Steps 1010-1029" in ledger.scope

    def test_malformed_lines_ignored(self):
        text = "# Plan\n\n- not a checklist\n- also not\n## Other\nrandom text"
        ledger = build_progress_ledger_from_plan(text)
        assert len(ledger.items) == 0

    def test_source_type_is_plan_step(self):
        ledger = build_progress_ledger_from_plan(SAMPLE_PLAN)
        for item in ledger.items:
            assert item.source_type == ProgressSource.PLAN_STEP

    def test_step_numbers_in_source_ref(self):
        ledger = build_progress_ledger_from_plan(SAMPLE_PLAN)
        assert ledger.items[0].source_ref == "step-1010"

    def test_empty_plan(self):
        ledger = build_progress_ledger_from_plan("")
        assert len(ledger.items) == 0
        assert ledger.scope == ""


# ---------------------------------------------------------------------------
# Step 1013: Live review parsing tests
# ---------------------------------------------------------------------------


SAMPLE_LIVE_REVIEW = """\
# Live Review — Steps 995-1009

## Verdict
PASS — all blockers resolved

## Finding Ledger

### R-0007: Raw user prompt in bundle

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: redaction
- **Fix**: Done: R-0007 — Replaced user_prompt_preview with safe summary

### R-0008: Audit incomplete

- **Status**: Resolved
- **Severity**: High
- **Area**: safety-audit

### R-0009: Protected paths not filtered

- **Status**: Open
- **Severity**: Medium
- **Area**: protected-paths
"""


class TestMergeLiveReview:

    def test_resolved_finding(self):
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, SAMPLE_LIVE_REVIEW)
        r7 = next(i for i in ledger.items if i.item_id == "R-0007")
        assert r7.status == ProgressStatus.RESOLVED

    def test_open_finding_medium(self):
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, SAMPLE_LIVE_REVIEW)
        r9 = next(i for i in ledger.items if i.item_id == "R-0009")
        assert r9.status == ProgressStatus.PLANNED

    def test_open_blocker_becomes_blocked(self):
        text = """\
## Verdict
PASS

### R-0099: Critical issue

- **Status**: Open
- **Severity**: Blocker
- **Area**: test
"""
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, text)
        r99 = next(i for i in ledger.items if i.item_id == "R-0099")
        assert r99.status == ProgressStatus.BLOCKED

    def test_done_marker_linked_as_evidence(self):
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, SAMPLE_LIVE_REVIEW)
        r7 = next(i for i in ledger.items if i.item_id == "R-0007")
        assert len(r7.evidence_refs) >= 1
        assert r7.evidence_refs[0].source_type == "done_marker"

    def test_verdict_extracted(self):
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, SAMPLE_LIVE_REVIEW)
        assert "PASS" in ledger.verdict

    def test_pass_with_open_blocker_inconsistency(self):
        text = """\
## Verdict
PASS — all good

### R-0050: Blocker issue

- **Status**: Open
- **Severity**: Blocker
- **Area**: test
"""
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, text)
        assert len(ledger.inconsistencies) >= 1
        assert "blocker" in ledger.inconsistencies[0].lower()

    def test_severity_preserved(self):
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, SAMPLE_LIVE_REVIEW)
        r7 = next(i for i in ledger.items if i.item_id == "R-0007")
        assert r7.severity == "Blocker"

    def test_area_preserved(self):
        ledger = ProgressLedger()
        merge_live_review_findings(ledger, SAMPLE_LIVE_REVIEW)
        r8 = next(i for i in ledger.items if i.item_id == "R-0008")
        assert r8.area == "safety-audit"


# ---------------------------------------------------------------------------
# Step 1014: Known risk tests
# ---------------------------------------------------------------------------


SAMPLE_CONTEXT = """\
# Context

## Known Risks
- `test_full_chain_order` fails on main.
- Bundle safety v1 has no PEM body detection.

## Pre-existing Issue
`test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.
"""


class TestMergeKnownRisks:

    def test_known_risks_extracted(self):
        ledger = ProgressLedger()
        merge_known_risks(ledger, SAMPLE_CONTEXT)
        risks = [i for i in ledger.items if i.status == ProgressStatus.RISK]
        assert len(risks) >= 2

    def test_risk_source_type(self):
        ledger = ProgressLedger()
        merge_known_risks(ledger, SAMPLE_CONTEXT)
        for item in ledger.items:
            assert item.source_type == ProgressSource.KNOWN_RISK

    def test_empty_context_no_risks(self):
        ledger = ProgressLedger()
        merge_known_risks(ledger, "# Context\n\n## Active Branch\nmain")
        risks = [i for i in ledger.items if i.status == ProgressStatus.RISK]
        assert len(risks) == 0


# ---------------------------------------------------------------------------
# Unified builder tests
# ---------------------------------------------------------------------------


class TestBuildProgressLedger:

    def test_unified_builder(self):
        ledger = build_progress_ledger(
            plan_text=SAMPLE_PLAN,
            live_review_text=SAMPLE_LIVE_REVIEW,
            context_text=SAMPLE_CONTEXT,
        )
        assert ledger.done_count >= 2
        assert ledger.risk_count >= 1
        assert len(ledger.items) >= 6

    def test_no_sources(self):
        ledger = build_progress_ledger()
        assert len(ledger.items) == 0
        assert ledger.verdict == ""

    def test_unverified_snapshot_surfaces_risk(self):
        """Apply without snapshot_verified=True → RISK item in ledger (Step 1147)."""
        from unittest.mock import MagicMock
        art = MagicMock()
        art.metadata = {
            "patch_intent_apply_records": {
                "abc12345-0": {"state": "applied", "snapshot_verified": False}
            }
        }
        art.id = "art-001"
        job = MagicMock()
        job.artifacts = [art]
        ledger = build_progress_ledger(job=job)
        titles = [i.title for i in ledger.items]
        assert any("without verified snapshot" in t for t in titles)
        risk_items = [i for i in ledger.items if i.status == ProgressStatus.RISK]
        assert len(risk_items) >= 1

    def test_verified_snapshot_no_risk(self):
        """Apply with snapshot_verified=True → no snapshot risk item (Step 1147)."""
        from unittest.mock import MagicMock
        art = MagicMock()
        art.metadata = {
            "patch_intent_apply_records": {
                "abc12345-0": {"state": "applied", "snapshot_verified": True}
            }
        }
        art.id = "art-001"
        job = MagicMock()
        job.artifacts = [art]
        ledger = build_progress_ledger(job=job)
        titles = [i.title for i in ledger.items]
        assert not any("without verified snapshot" in t for t in titles)


# ---------------------------------------------------------------------------
# Export tests
# ---------------------------------------------------------------------------


class TestExportLedger:

    def test_export_json_structure(self):
        ledger = build_progress_ledger(plan_text=SAMPLE_PLAN)
        data = export_progress_ledger_json(ledger)
        assert data["version"] == 1
        assert isinstance(data["items"], list)
        assert "done_count" in data
        assert "open_count" in data
        assert "blocked_count" in data
        assert "risk_count" in data
        assert "inconsistencies" in data

    def test_export_json_parses(self):
        ledger = build_progress_ledger(plan_text=SAMPLE_PLAN)
        data = export_progress_ledger_json(ledger)
        text = json.dumps(data)
        parsed = json.loads(text)
        assert parsed["version"] == 1

    def test_item_fields(self):
        ledger = build_progress_ledger(plan_text=SAMPLE_PLAN)
        data = export_progress_ledger_json(ledger)
        item = data["items"][0]
        assert "item_id" in item
        assert "title" in item
        assert "status" in item
        assert "source_type" in item

    def test_summarize(self):
        ledger = build_progress_ledger(
            plan_text=SAMPLE_PLAN,
            live_review_text=SAMPLE_LIVE_REVIEW,
        )
        text = summarize_progress_ledger(ledger)
        assert "Progress Ledger" in text
        assert "Done:" in text
        assert "[x]" in text

    def test_no_raw_content(self):
        ledger = build_progress_ledger(
            plan_text=SAMPLE_PLAN,
            live_review_text=SAMPLE_LIVE_REVIEW,
            context_text=SAMPLE_CONTEXT,
        )
        data = export_progress_ledger_json(ledger)
        text = json.dumps(data)
        assert "Traceback" not in text
        assert "raw_diff" not in text
        assert "__pycache__" not in text


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:

    def test_ledger_counts(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(item_id="1", status=ProgressStatus.DONE),
            ProgressItem(item_id="2", status=ProgressStatus.DONE),
            ProgressItem(item_id="3", status=ProgressStatus.PLANNED),
            ProgressItem(item_id="4", status=ProgressStatus.BLOCKED),
            ProgressItem(item_id="5", status=ProgressStatus.RISK),
            ProgressItem(item_id="6", status=ProgressStatus.SKIPPED),
            ProgressItem(item_id="7", status=ProgressStatus.RESOLVED),
        ]
        assert ledger.done_count == 3
        assert ledger.open_count == 1
        assert ledger.blocked_count == 1
        assert ledger.risk_count == 1
        assert ledger.skipped_count == 1

    def test_status_enum_values(self):
        assert ProgressStatus.PLANNED.value == "planned"
        assert ProgressStatus.IN_PROGRESS.value == "in_progress"
        assert ProgressStatus.DONE.value == "done"
        assert ProgressStatus.RESOLVED.value == "resolved"
        assert ProgressStatus.BLOCKED.value == "blocked"
        assert ProgressStatus.DEFERRED.value == "deferred"
        assert ProgressStatus.RISK.value == "risk"
        assert ProgressStatus.SKIPPED.value == "skipped"

    def test_source_enum_values(self):
        assert ProgressSource.PLAN_STEP.value == "plan_step"
        assert ProgressSource.LIVE_REVIEW_FINDING.value == "live_review_finding"
        assert ProgressSource.KNOWN_RISK.value == "known_risk"
        assert ProgressSource.FEATURE_SUGGESTION.value == "feature_suggestion"
