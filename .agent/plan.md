# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies and the free disk — with
`remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI step can gate
on; a crash leaves a local, redacted report under the data root; and the serve supervisor answers
its own health on its public API (docs/roadmap/features/T12_F199.md; DECISIONs F199 D1 and D2).

## Current Step
Round 3 on `feature/f199-self-health`, session 1: book round 2 and R-1266's resolution; DECISION
F199 D2; the checks `snapshots`, `worktrees` and `providers` with their tests; the command's
description and its page brought to seven checks. T001 is then complete.

## Next Steps
1. T002: the local crash report at the CLI's catch-all and the supervisor's threads, and the
   check `crash_reports`.
2. T003: `GET /api/v1/health` on the supervisor's public API.
3. The closure.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
