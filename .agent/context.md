# Context — F078 Autonomy levels

## Active Branch
feature/f078-autonomy-levels, from `main` at `e688b30f3` (the merge commit of pull request 338).

## Scope
F078 (Tier 3), as `docs/roadmap/features/T3_F078.md` and DECISION F078 D1 state: the autonomy
level, its one start check and matrix, its refusals and change record, the seams that start jobs,
the caps of `L5`, and showing the level.

## Do not touch
Approval semantics, budget mechanics and the gauntlet's pass definition. A level only answers who
may start work; every gate, fence, budget and watchdog applies at every level. A structural step
changes no behaviour.

## Active assumptions
- F078's levels are spelled `L2` to `L5`; the 0 to 7 scale of `autonomy_readiness.py` is another
  measure and is left alone.
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation; a
  structural step is proved by the unchanged tests.

## Constraints
- Every pytest run in a round is targeted; the closure runs the one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.
- The functions and files on `docs/system/structure-ledger-v1.md` may not grow.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
