# Context — F018 Budgets & Stop Conditions (Package-Pipeline Closure)

## Branch
`feature/f018-budgets-stop-conditions-clean`
Base commit: `720d97290601709fd988d784c638ffe151fc405c`

## Current state
Package-pipeline closure round. Root cause fixed: manual Evidence now produces
v1.1.0 runtime gate with 19 real checks (not zero-check v1.0.0). Manifest
validator accepts v1.1.0 with version-discriminated field sets. Staged evidence
refresh regenerates stale gates before packaging. Runtime boundaries hardened:
stopped-job guard in run_job, first_running_at timing, closed actuals schema.
29 new E2E tests + 287 focused + 8067 full suite passing. Evidence + ZIP pending.

## Package-pipeline closure changes
1. Unified gate producer: manual_attestation calls real write_runtime_integration_gate
2. Versioned gate validation: build_review_manifest.py accepts v1.0.0 + v1.1.0
3. Staged evidence refresh: scripts/refresh_review_evidence.py in make_review_zip.sh + inventory update
4. Stopped-job guard: run_job blocks if pending stop signal exists
5. first_running_at timing: deferred until after budget validation + pre-stop pass
6. Closed actuals schema: schema_version, actual_sources, unmeasured_call_count
7. Stronger bound_run validation: head_sha, output_hash non-empty; passed >= min_passed

## Files changed (this round)
- packages/orchestration/manual_attestation.py (real gate producer call)
- packages/orchestration/job_evidence.py (verification_data passthrough)
- packages/orchestration/pingpong_job.py (stopped-job guard, timing, actuals)
- scripts/build_review_manifest.py (v1.1.0 support, stronger binding validation)
- scripts/refresh_review_evidence.py (new — staged gate refresh)
- scripts/make_review_zip.sh (refresh integration)
- tests/orchestration/test_f018_package_pipeline_e2e.py (28 new E2E tests)
- docs/roadmap/STATUS.md, docs/roadmap/features/T0_F018.md

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push/PR/merge/modify main
- F018 [~], F146 [ ]
