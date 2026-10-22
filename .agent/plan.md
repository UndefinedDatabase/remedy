# Plan — operator order fix1022-review-findings

## Goal
Repair the orchestrator's review findings of F310 to F074 on one branch and merge it when green:
R-1422 (failover booking during a hold), R-1423 (`used.minutes` of a running job), R-1424
(`extend` without an answer on a deadline stop), R-1425 (mypy debt of the new modules, left open
for F314).

## Current Step
Part 1, R-1422: the `_with_calls` fix committed; next its record (docs, Built State, ledger).

## Next Steps
1. Part 2, R-1423: red tests, `in_flight` keyword, contract 1.28, kit seed and re-record.
2. Part 3, R-1424: red tests, the deadline refusal, the budget doc line.
3. Part 4, R-1425: mypy before/after counts, repairs per module, ledger entry left OPEN.
4. Part 5: CHANGELOG, decisions, handoff; the finish gates; PR, dispatched CI, merge.

## Risks
- The contract bump to 1.28 touches pinned versions in tests and the client-answers kit.
- ORIG_BRANCH (`feature/f074-estimate-calibration`) was deleted by the Open PR Gate merge of
  pull request 380; the order ends on `main`.
