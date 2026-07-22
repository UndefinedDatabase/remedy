# Live Review — F018 Budgets & Stop Conditions

## Status
**BUILT + REPAIRED + ALL REPRODUCTION FINDINGS CLOSED + FINAL ACCEPTANCE** —
Canonical PersistedBudgetActualsV1, wall-clock authority, real three-call test,
VT V1.1 cross-consistency with output_hash verification.

Module:  `packages/orchestration/budget_guard.py` — pure deterministic evaluation +
         `decode_persisted_budget_actuals` (7-field strict decoder) +
         `counters_from_persisted` (validated → BudgetCounters)
Model:   `packages/core/models.py` — JobBudgets (closed, extra="forbid", StrictInt)
Config:  `packages/orchestration/config.py` — budget.* keys (fail-closed on unknown)
Resolve: `packages/orchestration/budget_resolution.py` — CLI/env/TOML precedence
Safe:    `packages/orchestration/safe_points.py` — unified should_stop predicate
Runner:  `packages/orchestration/pingpong_job.py` — wall-clock continuity, shared decoder
Loop:    `packages/orchestration/pingpong_loop.py` — pre-retry budget check
Stop:    `packages/orchestration/stop_reasons.py` — StopReason derivation
Post:    `packages/orchestration/failure_postmortem.py` — budget_exhausted FailureClass
Decision:`packages/orchestration/decision_queue.py` — budget stop event detection (JobPlan safe)
Manifest:`packages/orchestration/run_manifest.py` — budgets in logical_input_projection
Contract:`packages/orchestration/run_contract.py` — inherits from JobBudgets
CLI:     `apps/cli/commands/job.py` — remedy job budget (shared decoder, corrupt diagnostic)
         `apps/cli/commands/do_cmd.py` — budget-aware stop_check + stopped-job guard
Gate:    `packages/orchestration/runtime_integration_gate.py` — 15 source checks + 4 execution bindings
Attest:  `packages/orchestration/manual_attestation.py` — real gate producer (v1.1.0)
Refresh: `scripts/refresh_review_evidence.py` — staged gate regeneration
Manifest:`scripts/build_review_manifest.py` — v1.0.0 + v1.1.0 gate validation + cross-consistency
Package: `scripts/make_review_zip.sh` — refresh-before-manifest pipeline

## Final acceptance closure — ALL CLOSED
28. Canonical PersistedBudgetActualsV1: shared decoder, exact 7-field schema, no default-zero
29. Wall-clock authority: started_at == first_running_at cross-check in decoder
30. Honest CLI: shared decoder, mismatch → corrupt, diagnostic output
31. Real three-call: FakeProvider with counted names, budget stops at 3
32. VT V1.1 cross-consistency: selected == p+f+s, node_ids count == selected
33. VT output_hash: verifiable sha256(stdout_summary), always computed
34. Test fixture completeness: all actuals records have 7 required fields

## External Acceptance
- **Verdict**: PASS_WITH_RISKS — ACCEPTED (2026-07-22)
- **Accepted HEAD**: `30dd4a8107bf6346e046d2faa098ee8a23f4191a`
- **Evidence job**: `f018_final_closure_684c4eaf027e`
- **Package**: `remedy-review-20260722-175112-READY_FOR_REVIEW.zip` (SHA-256 `41a77d46...fc4aeaad`)
- Next: F146 — not started.

## Test suites (final acceptance round)
- `test_f018_authority_integration.py` — 114 passed (10 new, fixtures updated)
- `test_review_verification_tests_strict.py` — 24 passed (fixtures updated)
- `test_budget_guard.py` — 52 passed
- `test_job_budgets.py` — 76 passed
- `test_budget_stop_integration.py` — 39 passed
- `test_manual_completion_bundle.py` — 44 passed
- `test_final_verifier.py` — 97 passed
- `test_token_truth.py` — 37 passed
- `test_provider_evidence_integration.py` — 64 passed
