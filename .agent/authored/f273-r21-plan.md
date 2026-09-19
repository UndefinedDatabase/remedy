# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 21 is the integration-gate round: it books round 20's verdict and
three resolutions, appends the feature file's Built State, and runs the one
full suite of the feature, committing its transcript.

## Next Steps

1. A red transcript is repaired first, by the shrinking rule of
   amend0917-throughput, at most three rounds.
2. Closure round A: the self-use item, the integrity check, the evidence
   job and the review zip.
3. Closure round B: the ownership paragraph moving every open id F273 did
   not resolve to the next paydown, the ledger rotation, that paydown's
   registration, the STATUS flip and the pull request. R-0803 reads the
   closure suite's transcript, R-0807 the closure self-use run's ledger
   rows, R-0984 the 3.12 column of the pull request's hosted CI, R-0892
   waits on the operator's skill-page write, and R-0662 waits for the
   checklist consolidation pass.
