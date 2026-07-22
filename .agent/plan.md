# Plan — F018 Budgets & Stop Conditions (Package-Authority Closure)

## Goal
Close package-pipeline root cause: manual Evidence hardcodes zero-check v1.0.0
runtime gate while production source has v1.1.0 with 19 checks. Fix unified
manual Evidence, versioned gate validation, staged refresh, strict F018 runtime
boundaries, real E2E tests, then one canonical ZIP.

## Status: IMPLEMENTING — scopes 1-4 complete, scope 5 in progress

## Scope 1 — Unified manual Evidence and runtime-gate schema ✓
- [x] build_manual_completion_gates: replace hardcoded zero-check gate with real
      build_runtime_integration_gate call
- [x] create_manual_completion_bundle: pass repo_root + verification_data to gate
- [x] build_review_manifest.py: add 1.1.0 to _SUPPORTED_GATE_VERSIONS
- [x] build_review_manifest.py: version-discriminated gate check schema (v1.0
      static + v1.1 execution binding)
- [x] build_review_manifest.py: zero-checks-total blocks READY_FOR_REVIEW
- [x] build_review_manifest.py: exact bound_run schema validation
- [x] Tests for v1.1.0 gate validation

## Scope 2 — Staged Evidence refresh and latest-ZIP correctness ✓
- [x] scripts/refresh_review_evidence.py: regenerate derivable gates in staging
- [x] make_review_zip.sh: call refresh after staging, before manifest
- [x] evidence_refresh_report.json with gate verdicts

## Scope 3 — Strict F018 runtime authority boundaries ✓
- [x] Stopped-job override guard in run_job boundary (not just CLI)
- [x] first_running_at not set before pre-work validation
- [x] Complete persisted actuals provenance (closed Actuals state)
- [x] Stronger execution bindings (HEAD SHA, output_hash, passed >= min_passed)
- [x] Tests for each boundary

## Scope 4 — Full real package E2E tests ✓
- [x] Manual bundle → v1.1.0 gate with nonzero checks (7 tests)
- [x] Stale v1.0 gate automatically refreshed in staging (4 tests)
- [x] Original Evidence not mutated (1 test)
- [x] BLOCKED_EVIDENCE for missing prerequisites (1 test)
- [x] Manifest validator for v1.1.0 (8 tests)
- [x] Stopped-job guard (2 tests)
- [x] first_running_at timing (1 test)
- [x] Persisted actuals schema (4 tests)
- [x] Run full test matrix: 444 focused + 56 package + 8038 full suite

## Scope 5 — Truthful docs, final Evidence and one canonical ZIP
- [x] STATUS.md, T0_F018.md, context.md, live_review.md, plan.md updated
- [ ] Commit all tracked files
- [ ] Fresh manual Evidence for final HEAD
- [ ] Run make_review_zip.sh once
- [ ] Verify ZIP (HEAD, SHA-256, members, status)
- [ ] No post-ZIP commit

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].
