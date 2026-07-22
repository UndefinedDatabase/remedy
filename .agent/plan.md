# Plan — F018 Budgets & Stop Conditions (Final Acceptance Closure)

## Goal
Close 9 exact remaining reproductions from reviewed READY_FOR_REVIEW
package. Canonical PersistedBudgetActualsV1, unified wall-clock authority,
honest CLI, real three-call E2E, VT V1.1 cross-consistency, output proof.
One canonical ZIP from base 190b3528a2dada6a27fdd9c2fdb75a6a00e7ea43.

## Status: IMPLEMENTING

## Scope 1 — Canonical PersistedBudgetActualsV1
- [x] Shared decoder/encoder in budget_guard.py with exact 7-field schema
- [x] No default-zero for missing fields; no invented sources
- [x] Wire into pingpong_job.py resume (replace inline validation)
- [x] Wire into _cmd_job_budget (replace inline decoding)
- [x] Wire into _persist_budget_actuals roundtrip
- [x] Tests for every corrupt case (fixtures updated for complete records)

## Scope 2 — Wall-clock and budget-display authority
- [x] started_at must equal first_running_at at persist time
- [x] CLI uses first_running_at through shared decoder
- [x] Mismatch blocks as corrupt
- [x] Tests for timestamp agreement, disagreement, and CLI corrupt report

## Scope 3 — Real limit-three runtime acceptance
- [x] Deterministic in-process test through run_job path
- [x] max_provider_calls=3; calls 1-3 begin; call 4 never begins
- [x] Persisted provider_call_count=3; STOPPED via budget source

## Scope 4 — Verification V1.1 consistency and package blocking
- [x] selected == passed+failed+skipped per run
- [x] node_ids count == selected for production runs
- [x] output_hash = hash of packaged stdout_summary
- [x] output_hash always computed (even for empty stdout)
- [x] Tamper tests for overcount, undercount, hash mismatch

## Scope 5 — Truthful final state, Evidence and ZIP
- [x] Update context.md, plan.md, live_review.md
- [ ] Commit all tracked files; confirm clean tree
- [ ] Fresh Evidence from base 190b3528
- [ ] One make_review_zip.sh invocation; no post-ZIP commit

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].
