# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person can read one job's or
run's lines in order on the command line, on the public API and in the cockpit; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D4).

## Current Step
Round 4 on `feature/f203-structured-logging`, session 1: book round 3's PASS and R-1273, repair
R-1273 in `tests/regression/test_resource_safety.py`, and the first part of T002: the read of one
job's lines and `remedy doctor logs`.

## Next Steps
1. Round 5: the same read on the public API, with its client operation.
2. Round 6: the cockpit's logs view over that route, and the correlation test.
3. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1273 by F203.
- Logging state is process-global; `tests/conftest.py` resets it after every test.
