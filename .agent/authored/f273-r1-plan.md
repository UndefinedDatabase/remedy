# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 1 claims F273, books F271 round 6's verdict, lands DECISION F273 D1
and builds three of T001's five: R-0803 (an isolated data root for every
test, and a run that fails when the configured root changed), R-0804 (a
test walking every cockpit read endpoint for a fake-provider job) and
R-0810 (the fake builder writes one marker per task).

## Next Steps

1. The rest of T001: R-0807's F260 half (one ledger row per provider
   call) and R-0812 (the unified job path's events narrated).
2. T003: the integration gate's procedure (R-0396, R-0445, R-0645,
   R-0736).
3. T016: the run state renders its value, a Python 3.12 CI column, the
   review zip's manifest reads the live ledger, and R-0839's tombstones.
4. T002, then T004 to T015, then the findings the Acceptance names by id.
5. Closure; R-0803's resolution reads the closure suite's transcript.
