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

ROUND 11, the closing round: book round 10's PASS, rotate the ledger,
accept F029 in STATUS with its README pins, and open the pull request.

## Next Steps

1. The next session merges this feature's pull request at the Open PR
   Gate and claims the next feature by Rule A5.

## Risks

None open. Open findings: 0.
