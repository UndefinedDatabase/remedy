# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 4 books round 3's verdict and the resolutions of R-0671, R-0689 and
R-0690, lands DECISION F273 D4, and builds T002: R-0518, R-0569, R-0649,
R-0664, R-0691, R-0708, R-0734 and R-0815, each with a mutation that now
dies. R-0499 and R-0662 stay open with the reasons D4 gives.

## Next Steps

1. T004 to T015, one module group per round where the budget allows.
2. The findings the Acceptance names by id.
3. Closure; R-0803's resolution reads the closure suite's transcript,
   R-0807's the closure self-use run's ledger rows against its calls,
   R-0984's the 3.12 column of the closure pull request's hosted CI, and
   R-0662 waits for the checklist consolidation pass.
