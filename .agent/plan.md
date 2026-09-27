# Plan — F029 Subtree rerun

Branch: feature/f029-subtree-rerun, cut from `main` at `b2863af4`, the
merge commit of pull request 287 (F028 Task injection).

## Goal

"Do that part again" is safe and cheap: a rerun from a task in the middle
of a job resets that task and everything depending on it, restores the
files they changed to their state before the task (proved by tree
hashes), keeps earlier attempts as evidence in an attempt fan, and may run
with a model override that the evidence records
(`docs/roadmap/features/T5_F029.md`).

## Current Step

ROUND 2: book round 1's PASS and register R-1080, record DECISION F029
D2, repair R-1080, and land the first half of T002 — the rerun
preparation in `packages/orchestration/subtree_rerun.py`, the attempt
fields on the task, the job's rerun list, and the per-task model that
`run_job` passes to the builder.

## Next Steps

1. The review of round 2.
2. The second half of T002: `remedy job rerun-subtree` with the
   subtree's cost estimate, the cost preview's confirmation, and the
   run-log event with its readers.
3. T003: the attempt fan, its popover and the end-to-end proof.
4. The closure sequence.

## Risks

Open findings: R-1080, repaired in this round.
