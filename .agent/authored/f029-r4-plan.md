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

ROUND 4: book round 3's PASS and resolve R-1081, record DECISION F029
D4, and land the server half of T003 — the shared rerun command
function, the run-log event `subtree_rerun_prepared` with its plain
sentence, the task item's `attempt` and `attempts` on the dashboard, and
the write door's command `job.rerun-subtree`.

## Next Steps

1. The review of round 4.
2. T003's browser half: the send module, the types, the attempt chip,
   the attempt list in the task's popover, the Rerun control, and the
   render proof.
3. T003's end-to-end proof — run, rerun a middle task with an override,
   the subtree runs again, both attempts in the evidence.
4. The closure sequence.

## Risks

Open findings: none.
