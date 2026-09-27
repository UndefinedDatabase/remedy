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

ROUND 3: book round 2's PASS, resolve R-1080 and register R-1081, record
DECISION F029 D3, repair R-1081, and land the second half of T002 —
`remedy job rerun-subtree` with the subtree's cost estimate and the cost
preview's confirmation.

## Next Steps

1. The review of round 3.
2. T003: the rerun's run-log event with every reader of its name, the
   attempt fan in the graph, its popover, and the browser's command.
3. T003: the end-to-end proof — run, rerun a middle task with an
   override, the subtree runs again, both attempts in the evidence.
4. The closure sequence.

## Risks

Open findings: R-1081, repaired in this round.
