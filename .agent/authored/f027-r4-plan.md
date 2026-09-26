# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 4: book round 3, resolve R-1066, record DECISION F027 D4, and land
T002 — the `replan_proposal` decision derived from each veto, the answer
as a create-only control fact, the follow-up job created unplanned for a
replan, the settled completion of a job whose every veto is answered,
and the CLI route `remedy decision resolve <job> veto:<id>`.

## Next Steps

1. The channel commands: `job.veto-task` in the catalog, the CLI and the
   write door, and the door's answer of a replan proposal.
2. T003: the strike, the dimmed unreachable set and the inbox card on
   the page, and the diamond end-to-end.
3. The closure sequence.

## Risks

Nothing may replan or run without the operator's answer and relaunch.
Open findings: 0.
