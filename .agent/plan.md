# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 22 PASSED except round 2
(premise corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round
22). T001, T002 and T003 are COMPLETE. T004 is under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair R-0825: the round 9 rename of `JobPlan.status` to `state` left two
production guards reading the retired name through `getattr` with a default,
which answers silently rather than raising, so DECISION F272 D7's probe was
blind to them. Both are fixed, each pinned by a behaviour test, and a standing
scan now makes the class visible.

## Next Steps

1. Name F114's cost-preview carrier BEFORE `job.run` goes. Measured at
   `67515ab7`: `apps/cli/commands/job.py:726` is the ONLY call site of
   `confirm_cost_preview` in the product and it sits inside the handler being
   deleted, so the capability is lost silently unless `do.job-run` inherits it.
   `do.job-run` carries neither `is_expensive` nor `--yes`, and wiring the helper
   as-is would exit 2 on every non-tty run, so this needs a DECISION.
2. Delete `job.run-next` and `job.run` with their handlers and their sixteen
   advertisement sites. MEASURED at `67515ab7`: the store migration is NOT a
   prerequisite. DECISION F272 D13 requires a command's advertisements to DIE
   with it rather than be repointed, and rounds 20 through 22 established that
   shape for `job run-loop`. The classic runner is one connected component, so
   `_cmd_run_next_task_local`, `_cmd_job_run_cycles`, `_cmd_job_resume` and
   `agent_loop.run_agent_loop` fall together.
3. The classic store deletion: 199 files by
   `.agent/f272_t004_deletion_inventory.md`, staged in groups.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The store deletion is 199 files, 72 of them production, so it is many rounds
  and no single commit holds it.
- A half-performed deletion is the state the Orchestrator brief forbids, so every
  deletion round ends with the full suite green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 11
  and round 23 the feature is inside it and no scope report is owed.
