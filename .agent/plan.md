# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1).

## Current Step
Session 1, round 2: book round 1's verdict (PASS) and the resolutions of R-1128 and R-1127, and
land T003 (R-1125, a test that holds every README tier row's Total to the STATUS lines under that
tier) and T004 (R-1133, a test that every page under `docs/system/` and `docs/guides/` is linked
from `docs/README.md`), both in `tests/docs/test_docs_consistency.py`. The resolutions of both are
booked by the next round.

## Next Steps
1. Book round 2's verdict and the resolutions of R-1125 and R-1133; land T005 (R-1129, the
   cockpit's refused task edit worded by its `detail`).
2. T006 — R-1117, a task whose apply changed no file is not recorded as passed.
3. T007 — R-1137, the suite's CPU time per module measured, then cut or recorded.
4. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- R-1117 touches the job pipeline every real run takes; its round reads every reader of a task's
  status before it changes one.
- R-1137 may find no cut that keeps every assertion; then a decision records the cost.
