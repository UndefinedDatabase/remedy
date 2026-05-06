# Plan

## Goal
Step 24.3: Brain Smoke Final Polish — final pre-frontend smoke hardening before Brain Viewer v0.

## Prior step
Step 24.2: Brain Smoke Test Polish (1222 tests).

## Status
COMPLETE — 1222 tests pass.

## Steps
1. [x] Update tests/test_brain_smoke.py module docstring
   - Mentions Steps 24.1 / 24.2 / 24.3
   - Documents TestBrainNodeUnknownNode
   - Notes brain-node redaction targets patch_intent/artifact, not job
   - States --json stdout is the frontend contract
2. [x] Align run-log redaction target in test_brain_node_run_log_no_sentinels
   - Now uses patch_intent → artifact → job fallback (mirrors test_brain_node_json_no_sentinels)
3. [x] Strengthen raw stdout redaction in test_brain_node_json_no_sentinels
   - Captures raw stdout before json.loads/dumps roundtrip
   - Asserts all 5 sentinels absent from raw bytes
   - Then json.loads(raw) confirms it still parses
4. [x] Update docs/architecture.md
   - Step 24.3: final pre-frontend smoke hardening
   - Step 25: read-only local Brain Viewer v0
   - Future UI must consume only --json outputs, not human text mode
5. [x] Run full suite (1222 pass)
6. [ ] Commit Step 24.3 changes
7. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
