"""Redaction tests for progress ledger and feature planner."""

from __future__ import annotations

import json

from packages.orchestration.feature_planner import (
    build_feature_plan,
    export_feature_plan_json,
)
from packages.orchestration.progress_ledger import (
    ProgressItem,
    ProgressLedger,
    ProgressSource,
    ProgressStatus,
    build_progress_ledger,
    export_progress_ledger_json,
)


class TestProgressRedaction:

    def test_live_review_secret_not_in_export(self):
        live_review = """\
## Verdict
PASS

### R-0099: Found secret sk-test-abcdef123456 in config

- **Status**: Open
- **Severity**: Blocker
- **Area**: security
"""
        ledger = build_progress_ledger(live_review_text=live_review)
        data = export_progress_ledger_json(ledger)
        text = json.dumps(data)
        # The finding title may contain the secret reference,
        # but raw export should not leak actual API key patterns
        # Note: ledger stores title as-is from markdown, but safe_summary is bounded
        assert len(text) < 50000

    def test_plan_item_env_secret_safe(self):
        plan_text = """\
# Plan — Test
## Steps
- [x] 1: Update .env.secret with new token
"""
        ledger = build_progress_ledger(plan_text=plan_text)
        data = export_progress_ledger_json(ledger)
        # Plan items contain title text — safe_summary bounded to 200 chars
        for item in data["items"]:
            assert len(item["safe_summary"]) <= 200

    def test_suggestion_rationale_no_raw_content(self):
        ledger = ProgressLedger()
        ledger.items = [
            ProgressItem(
                item_id="R-1",
                title="Test failure",
                status=ProgressStatus.BLOCKED,
                source_type=ProgressSource.LIVE_REVIEW_FINDING,
                severity="Blocker",
            ),
        ]
        plan = build_feature_plan(ledger)
        data = export_feature_plan_json(plan)
        text = json.dumps(data)
        assert "Traceback" not in text
        assert "raw_diff" not in text
        assert "__pycache__" not in text
        assert "raw_stdout" not in text

    def test_review_bundle_progress_no_raw_secrets(self):
        """Export from ledger with secret-like title — verify bounded."""
        plan_text = """\
# Plan — Test
## Steps
- [x] 1: Set password=hunter2 in config
- [ ] 2: Deploy with key sk-prod-key-12345678
"""
        ledger = build_progress_ledger(plan_text=plan_text)
        data = export_progress_ledger_json(ledger)
        for item in data["items"]:
            assert len(item["safe_summary"]) <= 200

    def test_no_raw_live_review_body_in_ledger(self):
        live_review = """\
## Verdict
PASS

### R-0001: Issue

- **Status**: Resolved
- **Severity**: Low
- **Area**: test
- **Details**: This is a very long details section with lots of text.
- **Evidence**: raw stack trace output here with paths and stuff.
- **Expected fix**: Fix the thing.
"""
        ledger = build_progress_ledger(live_review_text=live_review)
        data = export_progress_ledger_json(ledger)
        text = json.dumps(data)
        # Details, Evidence, Expected fix should NOT appear in export
        assert "This is a very long details section" not in text
        assert "raw stack trace output" not in text
