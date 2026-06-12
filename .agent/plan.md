# Plan — Steps 1110-1134: Test Evidence Durability + Snapshot / Rollback Proof v1

## Goal
Close evidence durability gaps from Real Test Execution v1.
Create one mandatory, verified Snapshot / Rollback system for repository mutations.
No successful mutation without a verified path back.
No real test without clearly reported evidence persistence outcome.

## Current Step
1110 — Reconcile previous handoff

## Steps
- [x] 1110: Reconcile previous handoff — context.md, plan.md, live_review.md
- [ ] 1111: Close fake test.status action — add test.status command or replace with catalog command
- [ ] 1112: Repository-scoped test lease — prevent concurrent tests on same repo across jobs
- [ ] 1113: Explicit test_run_started event after Popen success
- [ ] 1114: TestExecutionResult evidence_status fields
- [ ] 1115: Remove silent persistence failure — narrow exception handling, structured outcomes
- [ ] 1116: Atomic job outcome finalization — finalize_test_outcome()
- [ ] 1117: Failure artifact idempotency by test_run_id
- [ ] 1118: RepositorySnapshot model — repository_snapshot.py
- [ ] 1119: Private snapshot storage — .data/workspaces/<job_id>/repository_snapshots/<snapshot_id>/
- [ ] 1120: Snapshot path set from structured patch
- [ ] 1121: Snapshot verification before apply — block apply if snapshot fails
- [ ] 1122: Integrate structured source_apply.py
- [ ] 1123: Integrate markdown patch_apply.py
- [ ] 1124: Durable apply record
- [ ] 1125: Explicit revert service — revert_repository_apply()
- [ ] 1126: Post-apply drift protection
- [ ] 1127: Revert verification
- [ ] 1128: Snapshot and revert events
- [ ] 1129: Snapshot CLI — remedy snapshot inspect, remedy patch revert
- [ ] 1130: Proof Chain and File Provenance
- [ ] 1131: Progress, Feature Planner, Review Bundle
- [ ] 1132: Readiness integration
- [ ] 1133: Tests and documentation
- [ ] 1134: Final handoff

## Known Risks
- R-0038: Silent persistence swallowing (Steps 1115-1116)
- R-0041: Fake test.status next_safe_action (Step 1111)
- R-0042: Job-only test lease (Step 1112)
- R-0043: Partial evidence persistence (Steps 1114-1116)
- Pre-existing: test_project_brain.py::test_full_chain_order fails on main
