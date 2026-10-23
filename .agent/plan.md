# Plan — operator order fix1022-review-findings

## Goal
Repair the orchestrator's review findings of F310 to F074 on one branch and merge it when green:
R-1422 (failover booking during a hold), R-1423 (`used.minutes` of a running job), R-1424
(`extend` without an answer on a deadline stop), R-1425 (mypy debt of the new modules, left open
for F314).

## Current Step
Stopped: the second hosted run is red on R-1427 and R-1428; pull request 381 is open and unmerged,
waiting on the operator's answer to Q24.

## Next Steps
1. The operator answers Q24: merge pull request 381 as it stands, or repair R-1427 and
   R-1428 and dispatch one more hosted run.

## Risks
- ORIG_BRANCH (`feature/f074-estimate-calibration`) was deleted by the Open PR Gate merge of
  pull request 380; the order ends on `main` (DECISION fix1022 (8)).
