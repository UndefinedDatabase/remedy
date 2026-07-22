# Context — F018 Budgets & Stop Conditions (Final Acceptance Closure)

## Branch
`feature/f018-budgets-stop-conditions-clean`
Base commit: `190b3528a2dada6a27fdd9c2fdb75a6a00e7ea43`

## Current state
Final acceptance closure round. 9 exact remaining reproductions closed:
canonical PersistedBudgetActualsV1 (shared decoder, no default-zero),
unified wall-clock authority (started_at == first_running_at cross-check),
honest budget CLI (shared decoder, mismatch → corrupt), real three-call
acceptance test through run_job, VT V1.1 cross-consistency (selected ==
p+f+s, node_ids count, output_hash verifiable). 114 authority tests +
focused passing in 9 suites.

## Final closure changes (this round)
1. `decode_persisted_budget_actuals` in budget_guard.py — 7-field strict decoder
2. `counters_from_persisted` in budget_guard.py — builds BudgetCounters from validated record
3. pingpong_job.py resume path wired to shared decoder (replaces inline validation)
4. apps/cli/commands/job.py CLI wired to shared decoder (both paths)
5. VT V1.1 cross-consistency checks in build_review_manifest.py
6. output_hash always computed in job_evidence.py (even for empty stdout)
7. test_review_verification_tests_strict.py fixtures updated (node_ids)
8. test_f018_authority_integration.py fixtures updated (complete actuals records)
9. TestWallClockSplit (3 tests), TestRealThreeCallLimit (1 test), TestVTCrossConsistency (6 tests)

## Files changed (this round)
- packages/orchestration/budget_guard.py (decoder + counters_from_persisted)
- packages/orchestration/pingpong_job.py (shared decoder wiring)
- packages/orchestration/job_evidence.py (output_hash always computed)
- apps/cli/commands/job.py (shared decoder, diagnostic output)
- scripts/build_review_manifest.py (VT V1.1 cross-consistency checks)
- tests/orchestration/test_f018_authority_integration.py (10 new tests, fixture fixes)
- tests/orchestration/test_review_verification_tests_strict.py (fixture fixes)
- tests/orchestration/test_manual_completion_bundle.py (fixture fixes)
- .agent/plan.md, .agent/context.md, .agent/live_review.md

## External Acceptance
- **Verdict**: PASS_WITH_RISKS — ACCEPTED (2026-07-22)
- **Accepted HEAD**: `30dd4a8107bf6346e046d2faa098ee8a23f4191a`
- **Evidence job**: `f018_final_closure_684c4eaf027e`
- **Package**: `remedy-review-20260722-175112-READY_FOR_REVIEW.zip`
- **SHA-256**: `41a77d46e5f48c1120937061d33e2c505cee00633f0f31147c14a054fc4aeaad`
- 547 tests passing across 9 suites
- F018 [x]. F146 [ ] — next, not started.
