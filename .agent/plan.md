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

ROUND 7: book round 6's PASS and its prose slip, put space between the
run detail's confirmation sentence and its two buttons, and land T003's
end-to-end proof — a real three-task job run through the command line,
its middle task rerun with a model override through the live write door
and through `remedy job rerun-subtree`, the subtree run again, and both
attempts read back from the job record, git, the run log, the dashboard,
the run records and the final report.

## Next Steps

1. The review of round 7, with the reviewer's headless render of the
   confirmation row.
2. The closure sequence: Built State and the checklist consolidation
   with the one full suite, then the evidence job and review zip, then
   the ledger rotation, the STATUS line and the pull request.

## Risks

Open findings: none.
