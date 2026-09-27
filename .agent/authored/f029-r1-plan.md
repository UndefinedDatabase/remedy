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

ROUND 1: claim F029, re-head the live review record, book F028's round
12, record DECISION F029 D1, and land T001 — the subtree, the walk of the
job branch, the refusals and the reset with its hash proof in
`packages/orchestration/subtree_rerun.py`, with its tests.

## Next Steps

1. The review of round 1.
2. T002: `remedy job rerun-subtree` behind the cost preview, the attempt
   counter, the subtree's tasks returned to pending, earlier attempts'
   evidence linked, and the model override recorded as disclosure.
3. T003: the attempt fan, its popover and the end-to-end proof.
4. The closure sequence.

## Risks

None open. Open findings: 0.
