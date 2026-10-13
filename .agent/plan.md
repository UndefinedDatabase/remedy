# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person can read one job's or
run's lines in order on the command line, on the public API and in the cockpit; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D3).

## Current Step
Round 3 on `feature/f203-structured-logging`, session 1: book round 2's PASS and R-1272's
resolution, the structural step of `continue_from_node`, ruff's `T20` over `packages/` with the
ruling of its 19 sites, and the ratchet `tests/test_t201_ratchet.py`. T001 closes with it.

## Next Steps
1. T002: the read of one job's or run's lines, oldest first across the rotated files, on the
   command line and on the public API.
2. T002: the cockpit's logs view over that API, and the correlation test.
3. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- Logging state is process-global; `tests/conftest.py` resets it after every test.
