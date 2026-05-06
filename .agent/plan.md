# Plan

## Goal
Step 24.2: Brain Smoke Test Polish — harden smoke tests and docs before visual Brain Viewer work.

## Prior step
Step 24.1: Brain CLI JSON + Detail Smoke Hardening (1217 tests).

## Status
COMPLETE — 1222 tests pass.

## Steps
1. [x] Strengthen brain-node CLI JSON redaction smoke
   - test_brain_node_json_no_sentinels now targets patch_intent node (fallback: artifact)
   - Job node intentionally avoided; patch_intent is directly adjacent to poisoned data
2. [x] Improve _assert_detail_keys diagnostics
   - Replaced symmetric-difference error with extra={...} / missing={...}
3. [x] Add TestBrainNodeUnknownNode (5 tests)
   - unknown node exits 1
   - stdout empty on failure
   - stderr contains "node not found" safe message
   - stderr does not contain traceback
   - long node_id (200 chars) safely truncated in stderr (not echoed verbatim)
4. [x] Add explicit helper comments to _call_brain_json / _call_brain_node_json
   - Documents that capsys.readouterr() is consumed; tests needing stderr must call main() directly
5. [x] Update docs/architecture.md — Step 24.2 locks smoke-level JSON contract
   - Frontend must treat --json stdout as only machine input, never parse human text output
6. [x] Run full suite (1222 pass)
7. [ ] Commit Step 24.2 changes
8. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
