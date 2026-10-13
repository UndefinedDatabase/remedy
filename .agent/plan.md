# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person can read one job's or
run's lines in order on the command line, on the public API and in the cockpit; and no `print`
remains in `packages/` (docs/roadmap/features/T12_F203.md; DECISION F203 D1).

## Current Step
Round 1 on `feature/f203-structured-logging`, session 1: claim F203, book F199's round 9, and land
the first part of T001, `packages/orchestration/structured_log.py` with its configuration keys,
the data-root class `logs` and its tests.

## Next Steps
1. Round 2: the setup wired into the command line and the serve supervisor, the ids bound on the
   job's run path and the provider call, and the page `docs/system/structured-logging-v1.md`.
2. Round 3: ruff's `T20` over `packages/` and a ruling for each of the 19 `print` sites.
3. T002: the read by job or run id on the command line, the public API and the cockpit, and the
   correlation test.
4. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- Logging state is process-global; every test that configures it resets it.
