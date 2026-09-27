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

ROUND 5: book round 4's PASS and its prose slip, record DECISION F029 D5
with its two assumption-log rows, and land T003's display half — the
task item's attempts in the browser's types, the `attempt <n>` chip on
the canvas, and the Attempts list in the task's detail popover.

## Next Steps

1. The review of round 5, with the reviewer's headless render of the
   chip and the Attempts list.
2. T003's control half: the Rerun control in place of the disabled
   button, the send module for `job.rerun-subtree` with its cost
   confirmation, and the report naming an override.
3. T003's end-to-end proof — run, rerun a middle task with an override,
   the subtree runs again, both attempts in the evidence.
4. The closure sequence.

## Risks

Open findings: none.
