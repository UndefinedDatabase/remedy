# Plan

## Goal
Step 12.8: Test Hygiene Before Decision Modes

## Status
IN PROGRESS

## Steps
1. [x] Confirm branch: feature/step12-risk-classification (same branch, test-only step)
2. [ ] tests/test_patch_intent.py: symlink test — replace tmp_path.parent / "outside_dir_12_7"
       with tmp_path_factory.mktemp("outside") for guaranteed isolation
3. [ ] tests/test_cli_main.py: fix "Private import" → "Public risk contract constant"
       in TestPatchIntentRisksCLI (RISK_LEVELS and RISK_UNKNOWN are public API)
4. [ ] docs/architecture.md: add consumer validation note for patch_intent_risks
5. [ ] .agent/decisions.md: record skipped performance change + consumer validation decision
6. [ ] Self-review, run tests, commit, push

## Notes
Optional performance (avoid triple CLI scenario run): skipped — pytest scope constraints
make a shared class-scoped fixture impractical without sacrificing clarity. Three fast
runs (<0.4s total) are preferable to a conftest.py addition or scope workaround.

## Branch
feature/step12-risk-classification

## PR
#12 (open — same branch)
