# Plan

## Goal
Step 12.6: Dry-Run Boundary + Risk Coverage Hardening

## Status
IN PROGRESS

## Steps
1. [x] Confirm branch: feature/step12-risk-classification (same branch, in-scope)
2. [ ] patch_intent.py: boundary check in generate_dry_run_preview (resolve + is_relative_to + RuntimeError)
3. [ ] patch_intent.py: truncate_preview(text) helper using _MAX_PREVIEW_CHARS
4. [ ] apps/cli/main.py: use truncate_preview instead of inline [:2000]
5. [ ] tests/test_patch_intent.py: boundary rejection test, valid path test, truncate_preview tests (3+)
6. [ ] tests/test_cli_main.py: tighten TestPatchIntentRisksCLI — assert exact RISK_UNKNOWN value in stdout
7. [ ] decisions.md: diff_preview CLI omission rationale
8. [ ] docs/architecture.md: brief note on diff_preview omission from CLI output
9. [ ] Self-review, run tests (target 390+), commit, push

## Branch
feature/step12-risk-classification

## PR
#12 (open — Step 12.6 is in-scope hardening continuation)
