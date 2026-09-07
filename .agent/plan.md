# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 19 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and T003
are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair the production strings that advertise commands which do not exist, and
ship the guard that keeps them repaired. Round 19 deleted `job run-loop` and
left three such strings; two more, naming a `guide next` that never existed,
were found by the same measurement.

## Next Steps

1. Delete the `job.run-next` command surface. Its catalog entry, its handler
   entry and one test pin are a clean cut, but sixteen other sites advertise
   `remedy job run-next` as a next action and both approval-gate tests in
   `tests/cli/test_plan_approval.py` shell out to it, so the advisory layer
   and those two tests move in the same commit.
2. Delete `job.run`. It is the catalog's ONLY `is_expensive` command and three
   tests pin that, so F114's cost preview needs a carrier before it goes.
3. Rule and delete the classic `_cmd_job_resume`, and with it
   `agent_loop.run_agent_loop`, which is the last production caller of
   `_cmd_run_next_task_local`.
4. The resolver collapse, which DECISION F260 D5 puts in the SAME commit range
   as the classic store deletion — 199 files by
   `.agent/f272_t004_deletion_inventory.md`, so many rounds.
5. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- A half-performed deletion is the one state the feature's Orchestrator brief
  says this work must not leave behind, so every deletion round ends with the
  full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 10
  and round 20 the feature is inside it and no scope report is owed.
