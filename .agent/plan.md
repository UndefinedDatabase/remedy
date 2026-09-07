# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 18 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001, T002 and T003
are COMPLETE. T004 has begun.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

T004's first deletion: the classic `job run-loop` command surface — its handler,
its catalog entry and the tests that exist only to pin it. It is the one of the
three classic-runner commands that deletes cleanly; the other two have
production callers and are deliberately left standing.

## Next Steps

1. Rule and then delete `job.run-next` and `job.run`. Measured at `4c70ba90`,
   neither is a clean cut: `_cmd_run_next_task_local` has a production caller
   at `packages/orchestration/agent_loop.py:626`, and `_cmd_job_run_cycles` is
   called by `_cmd_job_resume`, so the fate of `job resume` and of the agent
   loop's step must be ruled by measurement before either command dies.
2. The resolver collapse, which DECISION F260 D5 puts in the SAME commit range
   as the classic store deletion. `.agent/f272_t004_deletion_inventory.md`
   bounds that store at 199 tracked files, 72 of them production, so it is
   many rounds and its staging is designed from that file.
3. T005, the reachability test and the cluster deletion, which is never split.
   `packages/orchestration/autonomy_loop.py` becomes production-unreachable
   this round and is left for it rather than deleted early.

## Risks

- A half-performed deletion is the one state the feature's Orchestrator brief
  says this work must not leave behind, so every deletion round ends with the
  full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 9
  and round 19 the feature is inside it and no scope report is owed.
