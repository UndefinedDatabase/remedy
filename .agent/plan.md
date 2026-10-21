# Plan — F141 Permission matrix per autonomy level

## Goal
What running work may DO becomes one enforced table: eight actions by F078's levels `L2` to `L5`,
answered by one check in `packages/orchestration/permission_matrix.py` that every seam calls, with
a test per cell, answers that cite their cell, audited approvals of an instance, a table rendered
from the constant, and no bypass parameter (docs/roadmap/features/T7_F141.md; DECISIONs F141 D1
to D3).

## Current Step
Round 3 (session 1): book round 2, resolve R-1395 and register R-1396, DECISION F141 D3, then the
apply's `write_worktree`, `commit` and `push` seams through `apply_permissions.py`, `remedy do`'s
push, and R-1396's test.

## Next Steps
1. Round 4: the `dependency_change` and `destructive` predicates and their seams in the apply.
2. Round 5: the `expensive` and `external_call` seams.
3. Round 6 (T003): the decision path with the cited cell, the table rendered in the docs and the
   UI from the constant, the guard against bypass parameters, the fate of `permissions.py` and of
   the builder bridge's integer level, and a fixture per level.
4. The closure sequence.

## Risks
- `job_apply.py` is on the structure ledger; every edit there stays line-neutral.
- The integrity check fails on High findings F141 does not own (DECISION F310 D7, Q20).
