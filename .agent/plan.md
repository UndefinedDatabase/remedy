# Plan — Steps 4773-4787: Repair Governance Correctness Closure v3

## Goal
Fix 5 real correctness bugs found by review in repair governance v2.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Step 4773: repair_rounds=0 truly disables repair (removed legacy_max_rounds_behavior)
- Step 4774: CLI argparse default=None → resolve_repair_rounds(None) returns 2
- Step 4775: repair_rounds_source (cli/default) persisted in PingPongResult + JSON
- Step 4776: validate_reviewer_output receives test_passed — test failure is evidence
- Step 4777: review_inconsistent always adjudicates as needs_human_review (never ready)
- Step 4778: Open findings flow into final adjudication (already correct, verified)
- Step 4779: Re-review round label fixed (repair_rounds_used not +1)
- Step 4780: Promotion readiness proof tightened (already correct, verified)
- Step 4781: 5 explicit repair_rounds=0 regression tests
- Step 4782: 5 CLI default + source tracking tests
- Step 4783: 4 inconsistent-review adjudication tests (including E2E)
- Step 4784: 4 test-failure coherence tests + 1 re-review label test
- Step 4785: JSON/text reports updated with repair_rounds_source
- Step 4786: Existing safety preserved (455 related tests pass)
- Step 4787: Architecture guard clean, full suite 7655 passed
- 19 new tests (109 total in test_repair_loop.py)
- Full suite: 7655 passed, 0 failed
- Lint: ruff clean, compileall clean
