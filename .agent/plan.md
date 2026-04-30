# Plan

## Goal
Step 12.8: Test Hygiene Before Decision Modes

## Status
COMPLETE — committed aa6fd27, pushed, PR #12 updated

## Steps
1. [x] Confirm branch: feature/step12-risk-classification
2. [x] tests/test_patch_intent.py: symlink test isolation via tmp_path_factory.mktemp
3. [x] tests/test_cli_main.py: fix "Private import" → "Public risk contract constant"
4. [x] docs/architecture.md: consumer contract note for patch_intent_risks
5. [x] .agent/decisions.md: consumer validation + skipped performance change documented
6. [x] 396 tests pass; committed; pushed

## Notes
Optional performance (avoid triple CLI scenario run): skipped — documented in decisions.md.

## Branch
feature/step12-risk-classification

## PR
#12 (open)
