# Live Review — F018 Budgets & Stop Conditions

## Status
**BUILT + REPAIRED + 10 REPRODUCTION FINDINGS CLOSED + PACKAGE-PIPELINE CLOSURE** —
Root cause of packaged-vs-production gate split fixed at every layer.

Module:  `packages/orchestration/budget_guard.py` — pure deterministic evaluation
Model:   `packages/core/models.py` — JobBudgets (closed, extra="forbid", StrictInt)
Config:  `packages/orchestration/config.py` — budget.* keys (fail-closed on unknown)
Resolve: `packages/orchestration/budget_resolution.py` — CLI/env/TOML precedence
Safe:    `packages/orchestration/safe_points.py` — unified should_stop predicate
Runner:  `packages/orchestration/pingpong_job.py` — wall-clock continuity, deterministic stop id
Loop:    `packages/orchestration/pingpong_loop.py` — pre-retry budget check
Stop:    `packages/orchestration/stop_reasons.py` — StopReason derivation
Post:    `packages/orchestration/failure_postmortem.py` — budget_exhausted FailureClass
Decision:`packages/orchestration/decision_queue.py` — budget stop event detection (JobPlan safe)
Manifest:`packages/orchestration/run_manifest.py` — budgets in logical_input_projection
Contract:`packages/orchestration/run_contract.py` — inherits from JobBudgets
CLI:     `apps/cli/commands/job.py` — remedy job budget (honest: never invents zeros)
         `apps/cli/commands/do_cmd.py` — budget-aware stop_check + stopped-job guard
Gate:    `packages/orchestration/runtime_integration_gate.py` — 15 source checks + 4 execution bindings
Attest:  `packages/orchestration/manual_attestation.py` — real gate producer (v1.1.0)
Refresh: `scripts/refresh_review_evidence.py` — staged gate regeneration
Manifest:`scripts/build_review_manifest.py` — v1.0.0 + v1.1.0 gate validation
Package: `scripts/make_review_zip.sh` — refresh-before-manifest pipeline

## 10 reproduction findings — ALL CLOSED
1. Clean branch: cherry-picked 14 legitimate commits, excluded Evidence blobs
2. Strict budget decode: model_validate failure → corrupt_budget_state block
3. Strict resumed actuals: reject bool/float/string/negative (no int() coercion)
4. BudgetCounters invariants: closed source vocab, measured tokens↔calls, tz-aware
5. JobPlan Decision Queue: getattr fallback for .metadata/.artifacts
6. Stopped job override: CLI exit 2 + Decision workflow message
7. Real runtime gate: test_execution_binding checks replace name-existence checks
8. Verification authority: all suites pass with production-level assertions
9. Doc updates: T0_F018.md, STATUS.md, context, plan, live_review current
10. Final sequencing: commit → evidence → ZIP → verify → stop

## Package-pipeline closure — ROOT CAUSE FIXED
11. Manual attestation: hardcoded zero-check v1.0.0 → real v1.1.0 gate producer
12. Manifest validator: v1.1.0 accepted with version-discriminated field sets
13. Staged refresh: scripts/refresh_review_evidence.py regenerates stale gates
14. Stopped-job guard in run_job: pending stop → block before config resolution
15. first_running_at timing: deferred past budget validation and pre-stop check
16. Closed actuals schema: schema_version + actual_sources + unmeasured_call_count
17. Stronger bound_run validation: head_sha, output_hash non-empty; passed ≥ min_passed

## Test suites (package-pipeline closure round)
- `test_f018_package_pipeline_e2e.py` — 28 passed (new)
- `test_f018_authority_integration.py` — 77 passed
- `test_budget_guard.py` — 52 passed
- `test_job_budgets.py` — 76 passed
- `test_budget_stop_integration.py` — 39 passed
- `test_runtime_integration_gate.py` — 14 passed
- `test_review_gate_exact_schemas.py` — 18 passed
- `test_review_gate_recursive_schemas.py` — 7 passed
- `test_review_gate_semantic_consistency.py` — 27 passed
- `test_review_gate_complete_semantics.py` — 46 passed
- `test_review_gate_typed_shapes.py` — 17 passed
- `test_review_gate_totality.py` — 3 passed
- `test_review_gate_embedded_verdicts.py` — 6 passed
- `test_review_gate_key_safety.py` — 5 passed
- `test_review_gate_sensitive_metadata.py` — 5 passed
- `test_review_gate_duplicate_keys.py` — 5 passed
- `test_review_ready_gate_matrix.py` — 19 passed
- Full orchestration suite: 8038 passed (pre-existing failures only)

## Next
Evidence + full review ZIP. F018 stays `[~]`.
