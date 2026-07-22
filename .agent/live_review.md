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
13. Staged refresh: scripts/refresh_review_evidence.py regenerates stale gates + updates inventory
14. Stopped-job guard in run_job: pending stop → block before config resolution
15. first_running_at timing: deferred past budget validation and pre-stop check
16. Closed actuals schema: schema_version + actual_sources + unmeasured_call_count
17. Stronger bound_run validation: head_sha, output_hash non-empty; passed ≥ min_passed

## 10-reproduction evidence integrity closure — ALL CLOSED
18. VT V1.1 normalization: truthful counts + monotonic duration capture
19. Strict persisted actuals: schema_version="1.0.0" required, reject banana/None
20. Source provenance: actual_sources required when actual_call_count > 0
21. Honest budget display: _cmd_job_budget passes real actual_sources
22. Corrupt first_running_at: blocks job instead of silent now() fallback
23. Exact gate binding: test_run_job_rejects_budget_on_stopped + 3 new nodes
24. .agent/Evidence exclusion from ZIP packaging
25. prior_execution accepted as audit dict on manual operator repairs
26. Manual completion gate exemption: fresh_evidence + runtime_integration
27. Manual completion tests: 44/44 passing (was 40/44)

## Test suites (10-reproduction closure round)
- `test_f018_authority_integration.py` — 104 passed (9 new)
- `test_budget_guard.py` — 52 passed
- `test_job_budgets.py` — 76 passed
- `test_budget_stop_integration.py` — 39 passed
- `test_manual_completion_bundle.py` — 44 passed (4 fixed)
- `test_final_verifier.py` — 97 passed
- `test_token_truth.py` — 37 passed
- `test_provider_evidence_integration.py` — 64 passed (1 updated)
- Total focused: 513 passed

## Next
Commit → Evidence from base 190b3528 → ZIP → receipt → stop. F018 stays `[~]`.
