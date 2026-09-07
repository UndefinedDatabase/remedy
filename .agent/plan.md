# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 16 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 and T002 are
COMPLETE. T003 is open: round 16 moved its first consumer, `job stop`, and this
round moves the second.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

T003's second consumer. `remedy job context` searched the CLASSIC store alone,
so it answered "no job matches prefix" for every job `remedy do job-run`
created. It now resolves across both stores and reads a `TaskEntry`'s own
`task_id` and `files_hint`, the way `job_stop_cmd._load_job` already reads
unified first and classic second.

## Next Steps

1. The remaining T003 consumer surface, re-grepped rather than taken from
   F260's 2026-09-05 list: `packages/orchestration/ui_server.py` and its
   `_JobPlanTaskAdapter`. That shim is finding R-0804's subject and the
   2026-09-06 triage routes R-0804 to F273 T001, so the boundary is ruled
   before it is touched. The `resolve_any_job_id` sites in
   `apps/cli/commands/teach_cmd.py` STAY: DECISION F260 D5 puts the resolver
   collapse in T004, with the store that makes it true.
2. Rule the Acceptance conflict as a DECISION, inside a round doing other
   work: this feature's Acceptance names tests.md ids that the 2026-09-06
   triage gave to F273 T001, and F272 cannot close while both claims stand.
3. T004, the classic runner and the resolver collapse, where `_CoreJobAdapter`
   dies with the classic store it exists to adapt.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- F272's soft limit is 12 sessions and 40 rounds under operator amendment
  amend0906-triage-throughput. At session 9 and round 17 the feature is
  inside it and no scope report is owed.
