# Plan — Steps 1155-1179: Snapshot Truth Final Closure + `remedy do --continue` v1

## Goal
Close remaining snapshot-truth gaps, then build one controlled continuation cycle:
approved intent → contract/permission checks → verified snapshot → apply → real test →
Proof Chain → safe stop. No auto-repair, no auto-revert, no loops. Crash-safe/idempotent.

## Current Step
1164 — do_continue models (in progress)

## Steps
- [x] 1155: Reconcile .agent/context.md, plan.md, live_review.md
- [x] 1156: build_snapshot_truth() authoritative shared helper (+ read-only integrity, ambiguity-aware)
- [x] 1157: Fix public File Provenance CLI (pass data_dir) + tests
- [x] 1158: Proof Chain uses durable snapshot truth + tests
- [x] 1159: Remove readiness event-only fallback + tests
- [x] 1160: snapshot_summary.json in Review Bundle
- [x] 1161: Close silent ApplyRecord persistence failure (structured result)
- [x] 1162: Event durability closure (EventPersistenceResult) — R-0051/R-0057
- [x] 1163: Canonical update_apply_record_state() (legal transitions, idempotent, atomic)
- [x] 1164: do_continue.py models (ContinueRequest/Result/Phase/Checkpoint/StopReason)
- [x] 1165: evaluate_continue_eligibility(job_id)
- [ ] 1166: CLI remedy do --continue <job_id> [--intent-id] [--json]
- [x] 1167: Continuation lease (deterministic, released on exit, stale-recoverable)
- [x] 1168: Durable phase checkpoints (idempotent resume)
- [ ] 1169: Snapshot phase (central path, verify before mutation)
- [ ] 1170: Apply phase (one ApplyRecord/apply_id, no double apply)
- [ ] 1171: Test phase (central Test Execution Service, usage once)
- [ ] 1172: Successful completion (completed_verified, Proof Chain rebuild)
- [ ] 1173: Failure completion (TestFailureArtifact + Fix Task, repair available)
- [ ] 1174: Apply succeeds but evidence degrades → evidence_incomplete
- [ ] 1175: do_continue_* events
- [ ] 1176: Progress Ledger + Feature Planner items
- [ ] 1177: continuation_summary.json in Review Bundle
- [ ] 1178: Runtime + idempotency tests (tiny temp repos)
- [ ] 1179: Docs + targeted/full pytest + live review + final handoff

## Carry-forward Risks
- R-0051/R-0057 event durability → Step 1162.
- File Provenance CLI missing data_dir → Step 1157.
- Readiness event fallback → Step 1159.
- Missing snapshot_summary.json → Step 1160.
- Silent ApplyRecord persistence failure → Step 1161.

## Next Block
Repair Loop v1 or bounded Overnight Mode preparation.
