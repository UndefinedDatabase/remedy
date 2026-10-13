# Plan — F199 Self-health & crash reports

## Goal
Remedy checks its own health — the configuration, the token ledgers, the snapshot manifests, the
worktrees, the providers' prerequisites, the staging copies, the free disk and recent crash
reports — with `remedy doctor health`, a PASS, WARN or FAIL table with hints and an exit code a CI
step can gate on; a crash leaves a local, redacted report under the data root; and the serve
supervisor answers its own health on its public API (docs/roadmap/features/T12_F199.md; DECISIONs
F199 D1 to D3).

## Current Step
Round 7 on `feature/f199-self-health`, session 2, the closure's integration-gate round: book round
6's PASS and the resolutions of R-1269, R-1270 and R-1271; the checklist's consolidation pass; the
closure's self-use item run to its approval gate, never applied; the one full suite and its CPU
cost; the handback.

## Next Steps
1. A green suite: the staging reclaim, the evidence job and the review package on the accepted
   head. A red suite: a repair round naming every bad node id.
2. The closing round: the Built State, the ledger rotation, the self-use entry's `consumed_by`, the
   STATUS flip with the README sync, and the pull request, left unmerged.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; F199 owns no open finding.
- The self-use run calls a paid provider within the `self_use` role's budget.
