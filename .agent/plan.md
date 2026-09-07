# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 20 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected, and round 21 FAILED
on R-0824, which this round repairs. T001, T002 and T003 are COMPLETE. T004 is
under way.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Repair R-0824: the round 21 block's own replacement prose wrote `remedy job
run-loop` into `docs/system/architecture.md` while the same block widened the
guard's zero-gate corpus to sweep that directory, so the branch tip shipped RED.
The sentence now names the deleted command without spelling it as an invocation.

## Next Steps

1. The classic store deletion, which leads T004 rather than following it.
   Measured at `5f4f0405`: every next-action rail advertising `remedy job
   run-next` — in `cockpit.py`, `timeline.py`, `trust_report.py`,
   `dashboard.py`, `brain_detail.py`, `agent_loop.py` and `autonomy_loop.py` —
   sits in a function typed `job: Job`, the CLASSIC record. None takes a
   `JobPlan`, so none can point at `remedy do job-run`, whose id is a
   16-character JobPlan id. The advertisements cannot move before the classic
   record does, and DECISION F272 D13 forbids deleting a command ahead of its
   advertisements.
2. `job.run-next` and `job.run` die inside that same commit range, with their
   rails. `job.run` is the catalog's only `is_expensive` command and three tests
   pin that, so F114's cost preview needs a carrier named before it goes.
3. `_cmd_job_resume` and `agent_loop.run_agent_loop`, the last production caller
   of `_cmd_run_next_task_local`, die with them per DECISION F272 D13.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The store deletion is 199 files by `.agent/f272_t004_deletion_inventory.md`,
  72 of them production, so it is many rounds and no single commit holds it.
- A half-performed deletion is the one state the Orchestrator brief says this
  work must not leave behind, so every deletion round ends with the full suite
  green in the PRIMARY checkout.
- F272's soft limit is 12 sessions and 40 rounds under amend0906. At session 10
  and round 22 the feature is inside it and no scope report is owed.
