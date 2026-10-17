# Context — scale correctness (audit remedy_scale_audit_2026-10-17.md)

## Active Branch
feature/scale-correctness-routing, cut from main `07b342626`. Not merged: the supervisor runs main, so
a merge changes what the next order runs; merged only on decodeux's word.

## Scope
Lane decision, path resolution, order parts, check-only job, study staleness, the order's budget
ledger, the reviewer's and repair round's view of the order, the scale matrix, tests and docs.
No planner redesign, no provider default, no new orchestrator.

## Do not touch
`.agent/STOP` (untracked), F078 and the autonomous queue, the sandbox, the public API contract
(only `order_budget` is added to the `do.run` answer).

## Constraints
- No real model call, no unattended loop, no install or restart.
- Steps: one full local gate run at the end; structure ratchet: no listed function or file grows.
- Commits at most 500 insertions.
