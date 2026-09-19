# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 5 books round 4's verdict and R-0774's resolution, lands DECISION
F273 D5, and builds T004's R-0648 (the integrity gate reads open Highs
through the ledger's canonical reader) and T005 (R-0469's undefined name,
every ruff finding cleared, the `budgets` stage failing on any finding,
ruff pinned).

## Next Steps

1. R-0753: the persisted actuals record carries money, as DECISION F273
   D5 (5) rules.
2. T006 to T015, one module group per round where the budget allows.
3. The findings the Acceptance names by id.
4. Closure; R-0803's resolution reads the closure suite's transcript,
   R-0807's the closure self-use run's ledger rows against its calls,
   R-0984's the 3.12 column of the closure pull request's hosted CI, and
   R-0662 waits for the checklist consolidation pass.
