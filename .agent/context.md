# Context — F018 Budgets & Stop Conditions (10-Reproduction Closure)

## Branch
`feature/f018-budgets-stop-conditions-clean`
Base commit: `190b3528a2dada6a27fdd9c2fdb75a6a00e7ea43`

## Current state
10-reproduction closure round. External reviewer returned BLOCKED_EVIDENCE on
10 exact reproductions. All 10 closed through production-code fixes:
truthful VT V1.1 (counts + durations), strict persisted actuals (schema +
provenance), honest budget display, corrupt first_running_at blocks, exact
gate binding, manual-completion gate exemption, .agent/Evidence ZIP exclusion.
104 authority tests + 513 focused passing in 8 suites. Evidence + ZIP pending.

## 10-reproduction closure changes
1. VT V1.1 normalization: `_run_verifications` schema 1.1.0, field derivation
2. Monotonic duration in `_default_verification_runner`
3. Strict schema_version on persisted actuals in pingpong_job.py
4. Required actual_sources when actual_call_count > 0
5. Honest _cmd_job_budget passes real actual_sources
6. Corrupt first_running_at blocks instead of silent now() fallback
7. Exact runtime gate binding: test_run_job_rejects_budget_on_stopped + 3 new nodes
8. .agent/Evidence excluded from make_review_zip.sh
9. prior_execution accepted as dict on manual repairs (provider_token_evidence.py)
10. Manual completions exempt from fresh_evidence/runtime_integration gate blocking

## Files changed (this round)
- packages/orchestration/job_evidence.py (VT V1.1, duration, deselected)
- packages/orchestration/pingpong_job.py (strict schema, sources, first_running_at)
- packages/orchestration/provider_token_evidence.py (prior_execution acceptance)
- packages/orchestration/final_verifier.py (manual completion gate exemption)
- packages/orchestration/runtime_integration_gate.py (binding + critical nodes)
- apps/cli/commands/job.py (honest actual_sources passthrough)
- scripts/make_review_zip.sh (.agent/Evidence exclusion)
- tests/orchestration/test_f018_authority_integration.py (9 new + 5 fixed)
- tests/orchestration/test_provider_evidence_integration.py (prior_execution test)
- docs/roadmap/STATUS.md, docs/roadmap/features/T0_F018.md

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push/PR/merge/modify main
- F018 [~], F146 [ ]
