# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies, the free disk and recent crash
reports — with `remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI
step can gate on; a crash leaves a local, redacted report under the data root; and the serve
supervisor answers its own health on its public API (docs/roadmap/features/T12_F199.md; DECISIONs
F199 D1 to D3).

## Current Step
Round 6 on `feature/f199-self-health`, session 1, the repair of round 5: book round 5's FAIL and
register R-1270 and R-1271, DECISION F199 D3; step (2) of the public API's boundary, the route
table, to `packages/orchestration/public_api_routes.py`; `doctor.health` registered as a client
operation; the handback for rounds 5 and 6; the push.

## Next Steps
1. The closure: the one full suite on the shipped tree, the staging reclaim, the evidence job and
   the review package; then the bookings, the ledger rotation, the STATUS flip and the pull request.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1269, R-1270 and R-1271 are F199's own.
