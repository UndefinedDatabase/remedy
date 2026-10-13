# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person can read one job's or
run's lines in order on the command line, on the public API and in the cockpit; and no `print`
remains in `packages/` (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 and D2).

## Current Step
Round 2 on `feature/f203-structured-logging`, session 1: book round 1's PASS and R-1272, the
setup wired into every command at `_dispatch`, the lazy folder, the file-only crash record, the
timeline mirror carrying the ids, the reset in `tests/conftest.py`, R-1272's repair, and the page
`docs/system/structured-logging-v1.md`.

## Next Steps
1. Round 3: ruff's `T20` over `packages/` and a ruling for each of the 19 `print` sites.
2. T002: the read by job or run id on the command line, the public API and the cockpit, and the
   correlation test.
3. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1272 by F203.
- Logging state is process-global; `tests/conftest.py` resets it after every test.
