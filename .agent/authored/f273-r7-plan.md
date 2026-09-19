# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 7 books round 6's verdict and the resolutions of the twenty findings
rounds 3 to 6 landed, lands DECISION F273 D7, and builds R-0568 (a guard
trip on a non-provider subprocess is `resource_limit`) and T012 with the
F273-owned R-0838 and R-0972 (the self-use track).

## Next Steps

1. R-0986, then T006, T007, T010, T011 and T013, one module group per
   round where the budget allows.
2. The findings the Acceptance names by id.
3. Closure; R-0803's resolution reads the closure suite's transcript,
   R-0807's the closure self-use run's ledger rows against its calls,
   R-0984's the 3.12 column of the closure pull request's hosted CI, and
   R-0662 waits for the checklist consolidation pass.
