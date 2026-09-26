# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 3: book round 2, resolve R-1065, register and repair R-1066,
record DECISION F027 D3, and complete T001 — a task vetoed while its
provider call runs finishes that call and is then vetoed while the run
goes on, and the cycle executor withholds a vetoed task and its
dependents and ends `blocked` naming them.

## Next Steps

1. T002: the replan proposal in the decision inbox with its two-option
   menu, and both options' documented effects.
2. The channel commands in the catalog, the CLI and the write door.
3. T003: the strike, the dimmed unreachable set and the inbox card on
   the page, and the diamond end-to-end.
4. The closure sequence.

## Risks

A veto must never kill a provider call mid-flight. Open findings: 1 —
R-1066, owned by F027 and repaired this round.
