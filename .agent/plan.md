# Plan — operator order fix1022-review-findings

## Goal
Repair the orchestrator's review findings of F310 to F074 on one branch and merge it when green:
R-1422 (failover booking during a hold), R-1423 (`used.minutes` of a running job), R-1424
(`extend` without an answer on a deadline stop), R-1425 (mypy debt of the new modules, left open
for F314).

## Current Step
Finish: R-1422 to R-1424 resolved, R-1425's repairs landed and its entry left OPEN; the finish
gates (ruff, tests/docs, the order's selections, the fast lane) run next.

## Next Steps
1. The handoff with the verification lines; push; the pull request.
2. Dispatch hosted CI once, watch it, merge only when every check is green.
3. `main` pulled, no open pull request left.

## Risks
- ORIG_BRANCH (`feature/f074-estimate-calibration`) was deleted by the Open PR Gate merge of
  pull request 380; the order ends on `main` (DECISION fix1022 (8)).
