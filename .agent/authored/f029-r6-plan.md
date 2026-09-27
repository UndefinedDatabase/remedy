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

ROUND 6: book round 5's PASS, record DECISION F029 D6 with its
assumption-log row, and land T003's control half — the send module and
the sentences for `job.rerun-subtree`, the Rerun control in the run
detail with its cost confirmation and optional model, and the final
report naming a task's attempt and its override.

## Next Steps

1. The review of round 6, with the reviewer's headless render of the
   Rerun control.
2. T003's end-to-end proof — run, rerun a middle task with an override,
   the subtree runs again, both attempts in the evidence.
3. The closure sequence.

## Risks

Open findings: none.
