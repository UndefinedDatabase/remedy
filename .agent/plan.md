# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person or a program can read
one job's or run's lines in order on the command line and on the public API; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D5).

## Current Step
Round 5 on `feature/f203-structured-logging`, session 1: book round 4's PASS and R-1273's
resolution, the route `GET /api/v1/jobs/{job}/logs` with the client operation `doctor.logs`, the
correlation test over a fake-provider run, the cockpit's logs view moved to F303, and operator
question Q18. T002 closes with it.

## Next Steps
1. The closure: the integration gate with the one full suite and the self-use item, the
   evidence package, then the Built State, the ledger rotation, the STATUS flip and the pull
   request.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- Logging state is process-global; `tests/conftest.py` resets it after every test.
