# Plan — F141 Permission matrix per autonomy level

## Goal
What running work may DO becomes one enforced table: eight actions by F078's levels `L2` to `L5`,
answered by one check in `packages/orchestration/permission_matrix.py` that every seam calls, with
a test per cell, answers that cite their cell, audited approvals of an instance, a table rendered
from the constant, and no bypass parameter (docs/roadmap/features/T7_F141.md; DECISIONs F141 D1
to D5).

## Current Step
Round 5 (session 1): book round 4, resolve R-1397 and R-1398, register R-1399, DECISION F141 D5,
then the `expensive` seam at the cost prompt, the `external_call` seam at a networked child, the
prompt's own approval kind, and R-1399's tests.

## Next Steps
1. Round 6 (T003): the table rendered in the docs from the constant, the guard against bypass
   parameters, the import guard over the seams, the fate of `permissions.py` and of the builder
   bridge's integer level, and a fixture per level.
2. Round 7 (T003): the matrix in the UI, rendered from the constant.
3. The closure sequence.

## Risks
- `job_apply.py`, `job.py` and `exec_guard.py` are at or above the structure ledger's limits; every
  edit there stays line-neutral.
- The integrity check fails on High findings F141 does not own (DECISION F310 D7, Q20).
