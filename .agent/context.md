# Context — F141 Permission matrix per autonomy level

## Active Branch
`feature/f141-permission-matrix`, from `main` at `43e470560` (the merge commit of pull request
373, which carried F078).

## Scope
F141 (Tier 7), as `docs/roadmap/features/T7_F141.md` and DECISION F141 D1 state: the permission
matrix, its one check, the push switch, the record of approved instances, the level a job keeps
from its start, the seams that route through the check, the rendered table and the guard against
bypass parameters.

## Do not touch
Fence semantics, level-change mechanics (F078) and role dimensions (F175). A cell of the matrix
never replaces a gate a seam already has: fences, the apply's approval, budgets and the cost
threshold apply at every level.

## Active assumptions
- The levels are F078's `AUTONOMY_LEVELS`, imported from `packages/orchestration/autonomy_gate.py`.
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation; a
  structural step is proved by the unchanged tests.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
