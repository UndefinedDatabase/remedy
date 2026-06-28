# Plan — Steps 5261-5270: Non-Blocking Evidence Validation

## Goal
Make evidence validation in make_review_zip.sh informational only.
Always select newest evidence by mtime. Always create zip.
Validation status recorded in manifest for reviewer, never blocks operator.

## Current Step
Step 5265: Implementation complete, tests passing, smoke test passed.

## Completed
- Auto-selection ranks ALL candidates by mtime (not just valid ones)
- Validation warnings printed but never block zip creation
- --allow-incomplete-evidence now silent no-op
- Removed blocking exit 2 paths for incomplete evidence
- Updated 5 tests for non-blocking behavior
- 34/34 hygiene tests pass, 79/79 job flow tests pass
- Smoke test confirms real incomplete evidence dirs produce zip

## Next Steps
- Step 5266: Commit, push, create PR
- Step 5267: Write builder handoff to .agent/live_review.md

## Constraints
No auto-approval, no target mutation, no git ops, no UI mutation,
no filename pattern changes, no external providers.
