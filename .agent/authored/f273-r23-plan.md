# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 23 opens the closure sequence: it books round 22's verdict and the
resolutions of R-0997 and R-0803, runs the closure's one self-use item to
its approval gate, mirrors that run into the token ledger and records the
ledger's rows against the run's provider calls, which R-0807 reads.

## Next Steps

1. Closure round A, second half: R-0807's resolution or finding from the
   self-use run's reading, then the integrity check, which reads FAIL while
   a High finding is open, the evidence job and the review zip.
2. Closure round B: the ownership paragraph moving every open id F273 did
   not resolve to the next paydown, the ledger rotation, that paydown's
   registration, the STATUS flip with the self-use item's `consumed_by`,
   and the pull request. R-0984 reads the 3.12 column of that pull
   request's hosted CI, R-0892 waits on the operator's skill-page write,
   and the checklist findings R-0662, R-0819 and R-0820 are carried.
