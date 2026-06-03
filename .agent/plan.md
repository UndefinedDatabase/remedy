# Plan — Steps 375-382

## Goal
Resource-safe pytest harness, reviewer safety protocol, handoff truth cleanup.

## Current Step
Step 382: Baseline complete, finalizing.

## Steps
- [x] Step 375: Resource-safety policy docs (docs/reviewer-safety.md, tests/README.md, .agent/context.md)
- [x] Step 376: Guarded pytest wrapper (scripts/remedy_pytest.sh) with flock + timeout
- [x] Step 377: Reviewer protocol update (no repeated full pytest, use wrapper)
- [x] Step 378: Fix handoff truth (live_review.md, plan.md, context.md)
- [x] Step 379: Standardize test command matrix
- [x] Step 380: Resource-safety regression tests (13 tests)
- [x] Step 381: Emergency cleanup guidance
- [x] Step 382: Guarded baseline (3943 passed, 7 skipped), next plan ready
