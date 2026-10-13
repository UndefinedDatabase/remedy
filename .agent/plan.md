# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies and the free disk — with
`remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI step can gate
on; a crash leaves a local, redacted report under the data root; and the serve supervisor answers
its own health on its public API (docs/roadmap/features/T12_F199.md; DECISION F199 D1).

## Current Step
Round 1 on `feature/f199-self-health`, session 1: claim F199, book F058's round 10, and land the
first half of T001, `packages/orchestration/self_health.py` with the checks `config`, `ledgers`,
`staging_copies` and `disk`, and their tests.

## Next Steps
1. Round 2: the structural step moving the catalog's `doctor` group to its own module, the checks
   `snapshots`, `worktrees` and `providers`, and the command `remedy doctor health`.
2. T002: the local crash report at the CLI's catch-all and the supervisor's threads, and the
   check `crash_reports`.
3. T003: `GET /api/v1/health` on the supervisor's public API.
4. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
