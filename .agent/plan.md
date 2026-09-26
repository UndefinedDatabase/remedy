# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 2: book round 1, register and repair R-1065, record DECISION F027
D2, and land the linear runner's fold of a veto — the fold before the
task loop and at every pre-task safe point, the workspace returned to a
vetoed attempt's start tree by `worktrees.restore_tree`, the unreachable
set never dispatched, the skipped tasks a block left going back to
pending, the terminal that names the vetoed and the unreachable tasks,
and `vetoed` in the run manifest's vocabulary.

## Next Steps

1. The rest of T001: a task vetoed while its call runs finishes that
   call and is then vetoed, and the cycle executor reads a veto.
2. T002: the replan proposal in the decision inbox with its two-option
   menu, and both options' documented effects.
3. The channel commands in the catalog, the CLI and the write door.
4. T003: the strike, the dimmed unreachable set and the inbox card on
   the page, and the diamond end-to-end.
5. The closure sequence.

## Risks

A vetoed attempt's partial work must never reach a later task's diff.
Open findings: 1 — R-1065, owned by F027 and repaired this round.
