# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1).

## Current Step
Session 4, round 4: book round 3's verdict (PASS) and the resolution of R-1129, register R-1138,
record DECISION F290 D2 and operator question Q4, and land T006 (R-1117):
`validate_job_task_result` in `packages/orchestration/pingpong_job.py` blocks a job task that
changed no file, with two tests in `tests/orchestration/test_job_task_runner.py`, and the test
builders in four other test files that named a file without writing it now write it. Its
resolution is booked by the next round.

## Next Steps
1. Book round 4's verdict and the resolution of R-1117; land T007 (R-1137, the suite's CPU time
   per module measured, then cut or recorded).
2. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- R-1137 may find no cut that keeps every assertion; then a decision records the cost.
- R-1138, registered this round, is owned by the paydown F290's closure registers.
