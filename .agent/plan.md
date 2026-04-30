# Plan

## Goal
Step 12.7: Dry-Run Boundary Test Precision

## Status
IN PROGRESS

## Steps
1. [x] Confirm branch: feature/step12-risk-classification (same branch, test-only step)
2. [ ] tests/test_patch_intent.py:
       - add symlink escape test to TestGenerateDryRunPreviewBoundary
       - clarify traversal test comment (verify skipped intentionally)
3. [ ] tests/test_cli_main.py:
       - split test_patch_intent_risks_stored_values_in_risk_levels_and_risk_line_in_output
         into three focused tests using shared setup helper
4. [ ] Self-review, run tests, commit, push

## Branch
feature/step12-risk-classification

## PR
#12 (open — same branch)
