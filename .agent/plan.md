# Plan — Steps 1155-1179: Snapshot Truth Final Closure + `remedy do --continue` v1

## Goal
Close remaining snapshot-truth gaps, then build one controlled continuation cycle:
approved intent → contract/permission checks → verified snapshot → apply → real test →
Proof Chain → safe stop. No auto-repair, no auto-revert, no loops. Crash-safe/idempotent.

## Current Step
1179 — Docs + full pytest + final handoff (complete; awaiting reviewer final verdict)

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
- [x] 1166: CLI remedy do continue <job_id> [--intent-id] [--json]
- [x] 1167: Continuation lease (deterministic, released on exit, stale-recoverable)
- [x] 1168: Durable phase checkpoints (idempotent resume)
- [x] 1169: Snapshot phase (central path, verify before mutation)
- [x] 1170: Apply phase (one ApplyRecord/apply_id, no double apply)
- [x] 1171: Test phase (central Test Execution Service, usage once)
- [x] 1172: Successful completion (completed_verified, Proof Chain rebuild)
- [x] 1173: Failure completion (TestFailureArtifact + Fix Task, repair available)
- [x] 1174: Apply succeeds but evidence degrades → evidence_incomplete
- [x] 1175: do_continue_* events
- [x] 1176: Progress Ledger + Feature Planner items
- [x] 1177: continuation_summary.json in Review Bundle
- [x] 1178: Runtime + idempotency tests (tiny temp repos)
- [x] 1179: Docs (do-continue-v1 + cross-links) + full pytest + final handoff

## Carry-forward Risks — all closed this block
- R-0051/R-0057 event durability → closed Step 1162 (EventPersistenceResult).
- File Provenance CLI missing data_dir → closed Step 1157.
- Readiness event fallback → closed Step 1159.
- Missing snapshot_summary.json → closed Step 1160.
- Silent ApplyRecord persistence failure → closed Step 1161.
- R-0061 snapshot truth builder → closed Step 1156 + wired Steps 1157-1160, 1169-1172.
- R-0062 continuation cycle → closed Steps 1164-1178.

## Next Block
Repair Loop v1 or bounded Overnight Mode preparation.
