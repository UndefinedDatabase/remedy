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

ROUND 8: book round 7's PASS, record DECISION F029 D7, and land the
feature file's last edge case — a rerun of one of a mission's jobs is
noted in the mission's dossier as one decision line, read from the job's
own record at the loop's next refresh.

## Next Steps

1. The review of round 8.
2. The closure sequence: Built State and the checklist consolidation
   with the one full suite, then the evidence job and review zip, then
   the ledger rotation, the STATUS line and the pull request.

## Risks

Open findings: none.
