# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1).

## Current Step
Session 3, round 3: book round 2's verdict (PASS) and the resolutions of R-1125 and R-1133, and
land T005 (R-1129): `describeTaskEditConflict` in `apps/ui/src/api/taskEditSend.ts` reads a
non-empty `detail` before `current_version`, so a refused edit whose plan fails its checks is
worded by its real reason, with two tests in `apps/ui/src/api/taskEditSend.test.ts`. Its
resolution is booked by the next round.

## Next Steps
1. Book round 3's verdict and the resolution of R-1129; land T006 (R-1117, a task whose apply
   changed no file is not recorded as passed).
2. T007 — R-1137, the suite's CPU time per module measured, then cut or recorded.
3. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- R-1117 touches the job pipeline every real run takes; its round reads every reader of a task's
  status before it changes one.
- R-1137 may find no cut that keeps every assertion; then a decision records the cost.
