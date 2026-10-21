# Plan — F141 Permission matrix per autonomy level

## Goal
What running work may DO becomes one enforced table: eight actions by F078's levels `L2` to `L5`,
answered by one check in `packages/orchestration/permission_matrix.py` that every seam calls, with
a test per cell, answers that cite their cell, audited approvals of an instance, a table rendered
from the constant, and no bypass parameter (docs/roadmap/features/T7_F141.md; DECISIONs F141 D1
to D7).

## Current Step
Round 7 (session 1): book round 6, resolve R-1400, DECISION F141 D7, then the matrix in the status
answer for the Orb (contract 1.24) and a fixture per level through the real seams (T003's last
items).

## Next Steps
1. The closure sequence, per `docs/roadmap/STATUS_closure_protocol.md`: the Built State, the
   integration gate's one full suite, the evidence job and review package, the STATUS acceptance
   with its README sync, and the pull request.

## Risks
- `job_apply.py`, `job.py`, `exec_guard.py` and `_cmd_status` are at or above the structure
  ledger's limits; every edit there stays line-neutral.
- The integrity check fails on High findings F141 does not own (DECISION F310 D7, Q20).
