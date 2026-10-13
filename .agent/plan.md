# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies and the free disk — with
`remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI step can gate
on; a crash leaves a local, redacted report under the data root; and the serve supervisor answers
its own health on its public API (docs/roadmap/features/T12_F199.md; DECISIONs F199 D1 and D2).

## Current Step
Round 4 on `feature/f199-self-health`, session 1: book round 3 and register R-1267 and R-1268,
repair both; T002: `packages/orchestration/crash_report.py`, the data-root class `crash`, the
report written at the CLI's catch-all and by a serve supervisor's thread, the check
`crash_reports`, their tests, and the page.

## Next Steps
1. T003: `GET /api/v1/health` on the supervisor's public API.
2. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1267 and R-1268 are F199's own.
