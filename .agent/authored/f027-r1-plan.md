# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 1: claim F027, re-head the live review record, book F285's round
6, record DECISION F027 D1, and land the veto control protocol —
`packages/orchestration/task_veto.py` with the mandatory verbatim
reason, the pure state gate, the unreachable set, the create-only
control file per vetoed task, the command effect and its `task_vetoed`
event, the `TASK_VETOED` status, and their unit tests.

## Next Steps

1. The rest of T001: the runners fold a veto at their safe points, an
   in-progress task finishes its current call before it is vetoed, and
   the terminal accounting names the veto.
2. T002: the replan proposal in the decision inbox with its two-option
   menu, and both options' documented effects.
3. The channel commands in the catalog, the CLI and the write door.
4. T003: the strike, the dimmed unreachable set and the inbox card on
   the page, and the diamond end-to-end.
5. The closure sequence.

## Risks

A veto must never be lost to a running job's save, so the command writes
a control file and never the job record. Open findings: 0.
