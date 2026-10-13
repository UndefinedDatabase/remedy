# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies, the free disk and recent crash
reports — with `remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI
step can gate on; a crash leaves a local, redacted report under the data root; and the serve
supervisor answers its own health on its public API (docs/roadmap/features/T12_F199.md; DECISIONs
F199 D1 to D3).

## Current Step
Round 8 on `feature/f199-self-health`, session 2, the closure's evidence round: book round 7's
PASS and the recurrence of R-1252; the staging reclaim, the evidence job on the accepted head and
the review package; the handback.

## Next Steps
1. The closing round: the Built State, the ledger rotation, the self-use entry `SU-060`'s
   `consumed_by`, the STATUS flip with the README sync, and the pull request, left unmerged.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; F199 owns no open finding.
