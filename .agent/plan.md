# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1).

## Current Step
Session 1, round 1, the claim: book F200's round 14 (PASS), re-head the ledger, write the slice
list and DECISION F290 D1, and land T001 (R-1128, the preview test's nonce drawn with
`secrets.token_hex(8)`) and T002 (R-1127, a test that reads the interpreter's audit events while
the data-root allocator makes two roots). The resolutions of both are booked by the next round.

## Next Steps
1. Book round 1's verdict and the resolutions of R-1128 and R-1127; land T003 (R-1125, the README
   tier rows held to STATUS by a test) and T004 (R-1133, every page under `docs/system/` and
   `docs/guides/` linked from `docs/README.md`).
2. T005 — R-1129, the cockpit's refused task edit worded by its `detail`.
3. T006 — R-1117, a task whose apply changed no file is not recorded as passed.
4. T007 — R-1137, the suite's CPU time per module measured, then cut or recorded.
5. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- R-1117 touches the job pipeline every real run takes; its round reads every reader of a task's
  status before it changes one.
- R-1137 may find no cut that keeps every assertion; then a decision records the cost.
