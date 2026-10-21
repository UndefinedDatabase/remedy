# Plan — F141 Permission matrix per autonomy level

## Goal
What running work may DO becomes one enforced table: eight actions by F078's levels `L2` to `L5`,
answered by one check in `packages/orchestration/permission_matrix.py` that every seam calls, with
a test per cell, answers that cite their cell, audited approvals of an instance, a table rendered
from the constant, and no bypass parameter (docs/roadmap/features/T7_F141.md; DECISION F141 D1).

## Current Step
Round 1 (session 1): claim F141, book F078's round 11, record the seam inventory, DECISION F141 D1
and operator question Q23, and land T001: the matrix, its check, the push switch and the record of
approvals, with a test per cell and per answer.

## Next Steps
1. Round 2: the pinned level at a job's start, and the `read` seam.
2. Round 3: the structural step of `job_apply.py` (the history, commit and push policy), then the
   `write_worktree`, `commit` and `push` seams, `do_push_mission` included.
3. Round 4: the `dependency_change` and `destructive` predicates and their seams.
4. Round 5: the `expensive` and `external_call` seams.
5. Round 6 (T003): the decision path with the cited cell, the table rendered in the docs and the
   UI from the constant, the guard against bypass parameters, the fate of `permissions.py` and of
   the builder bridge's integer level, and a fixture per level.
6. The closure sequence.

## Risks
- Every seam lives in a file on the structure ledger; each seam round takes a structural step first.
- The integrity check fails on High findings F141 does not own (DECISION F310 D7, Q20).
