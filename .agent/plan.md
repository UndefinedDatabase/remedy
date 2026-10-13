# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies, the free disk and recent crash
reports — with `remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI
step can gate on; a crash leaves a local, redacted report under the data root; and the serve
supervisor answers its own health on its public API (docs/roadmap/features/T12_F199.md; DECISIONs
F199 D1 and D2).

## Current Step
Round 5 on `feature/f199-self-health`, session 1: book round 4 and the resolutions of R-1267 and
R-1268, register and repair R-1269; T003: `GET /api/v1/health` on the public API the supervisor
and the cockpit answer, with its tests and pages. Every slice is then complete.

## Next Steps
1. The closure: the one full suite on the shipped tree, the staging reclaim, the evidence job and
   the review package; then the bookings, the ledger rotation, the STATUS flip and the pull request.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1269 is F199's own.
