# Context — F078 Autonomy levels

## Active Branch
`feature/f078-autonomy-levels-2`, from `main` at `ff309f737` (the merge commit of pull request
372), whose first commit merges session 1's `feature/f078-autonomy-levels` at `9d3187143`
(DECISION F078 D4).

## Scope
F078 (Tier 3), as `docs/roadmap/features/T3_F078.md` and DECISIONs F078 D1 to D4 state: the
autonomy level, its one start check and matrix, its refusals and change record, the seams that
start jobs, the caps of `L5`, and showing the level.

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
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.
