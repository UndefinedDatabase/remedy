# Plan — Steps 5201-5230: Review Zip Auto-Select Latest Evidence v1

## Goal
Fix make_review_zip.sh to auto-select newest valid evidence dir when multiple
exist. Preserve filename pattern exactly. Add selection metadata to manifest.
Add deterministic tie-breaker. Add tests.

## Current Step
Step 5201: Implement auto-selection logic

## Next Steps
- Update manifest with selection metadata
- Add filename pattern regression test
- Add auto-selection tests
- Full verification + handoff

## Constraints
No auto-approval, no target mutation, no git ops, no UI mutation,
no filename pattern changes, no external providers.
