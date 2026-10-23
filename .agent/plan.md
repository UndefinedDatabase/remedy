# Plan — operator order fix1022-review-findings

## Goal
Repair the orchestrator's review findings of F310 to F074 on one branch and merge it when green:
R-1422 (failover booking during a hold), R-1423 (`used.minutes` of a running job), R-1424
(`extend` without an answer on a deadline stop), R-1425 (mypy debt of the new modules, left open
for F314).

## Current Step
Done: the operator answered Q24 "mergen" (DECISION fix1022 D2); pull request 381 merges.

## Next Steps
1. F314 owns R-1425 to R-1428.

## Risks
- ORIG_BRANCH (`feature/f074-estimate-calibration`) was deleted by the Open PR Gate merge of
  pull request 380; the order ends on `main` (DECISION fix1022 (8)).
