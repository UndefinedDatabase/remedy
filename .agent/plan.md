# Plan — Steps 880-894: Context Inspector Truth Closure

## Goal
Fix 6 identified issues from independent review. No fake visibility, no overclaim.

## Current Step
Complete — all steps verified

## Steps
- [x] 880: Handoff truth (.agent files update)
- [x] 881: Harden `.env.*` protected path policy (pattern-based)
- [x] 882: Fix path traversal to segment-based (`..` as path part)
- [x] 883: Validate task_id exists in job.tasks
- [x] 884: Extract event target paths (applied changes, proof chain targets)
- [x] 885: Align with proof chain path filter (superset verified)
- [x] 886: Budget truth — renamed to assessed, not enforced
- [x] 887: Stable sorting/priority with event/proof targets
- [x] 888: Grouped CLI runtime test
- [x] 889: JSON contract snapshot test
- [x] 890: CLI text honesty test
- [x] 891: Docs update
- [x] 892: Targeted tests — 98 passed
- [x] 893: Fast lane — 4660 passed, 8 skipped (1 pre-existing deselected)
- [x] 894: Final handoff

## Risks
- Events parameter may not have relevant targets in all scenarios.
- Budget trimming deferred; wording fix is honest alternative.
- Pre-existing failure in test_project_brain.py::TestFileProvenanceChain::test_full_chain_order (not related).
