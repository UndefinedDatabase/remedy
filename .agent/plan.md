# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 17 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and now
T003 are COMPLETE.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Ruling the boundary this feature could not close over. F272's Acceptance names
five tests.md ids that the 2026-09-06 triage gives to F273 T001, and one of
them, R-0804, is the `ui_server.py` adapter that was the last unmoved item on
T003's list. DECISION F272 D12 rules the triage the winner, which closes T003 at
round 17's `job context` move and hands the cockpit adapter to F273. The same
round commits the probe-measured inventory that bounds T004.

## Next Steps

1. T004, the classic runner and the resolver collapse, staged from
   `.agent/f272_t004_deletion_inventory.md` rather than from any grep. That
   inventory is why T004 is many rounds and not one: 199 tracked files
   reference a classic job-store symbol by AST reading, 72 of them under
   `packages/` and `apps/`. DECISION F260 D5 keeps the resolver collapse in
   the SAME commit range as the store deletion.
2. T005, the reachability test and the cluster deletion. The Orchestrator
   brief's one hard rule: NEVER SPLIT INSIDE T005, so a session splits before
   it and never within it.

## Risks

- T004 is the largest remaining slice and its blast radius is measured rather
  than estimated. A round that tries to take it whole will exceed the
  DECISION F104 D1 insertion cap; the inventory exists to stage it.
- F272's soft limit is 12 sessions and 40 rounds under operator amendment
  amend0906-triage-throughput. At session 9 and round 18 the feature is
  inside it and no scope report is owed.
