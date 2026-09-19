# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 15 books round 14's verdict and six resolutions, lands DECISION F273
D15, and builds R-0990, R-0931 and R-0981; the repair-loop, R-0914 and
worker-queue prototypes are held for rulings (D15 (4)).

## Next Steps

1. The held rulings, each with its patch: the repair loop (R-0923 with
   R-0918, R-0924, R-0925, R-0926), R-0914, the worker queue (R-0927
   with R-0928).
2. The remaining open ids the Acceptance names (R-0892, R-0912's
   leftovers, R-0940, R-0954, R-0977), and a measured owner for every
   other open id.
3. Closure; R-0803's resolution reads the closure suite's transcript,
   R-0807's the closure self-use run's ledger rows against its calls,
   R-0984's the 3.12 column of the closure pull request's hosted CI, and
   R-0662 waits for the checklist consolidation pass.
