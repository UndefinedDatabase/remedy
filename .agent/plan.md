# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 14 books round 13's independently-reviewed PASS (Gate: F280 R13, one prose slip, no new
R-id), authors DECISION F280 D9, and lands the rest of the `flight_plan` rename DECISION
amend0917-throughput D3 ordered — widened past D3's four items to the DAG-key construction sites
and the identifier residue the dry run measured — as one 61-file, 339-line mechanical patch,
reviewer-dry-run-tested twice in a disposable worktree before authoring.

## Next Steps

1. `propose`'s deletion (DECISION amend0917-throughput D1 answers operator question Q4): the
   `Decision` type `proposal` enqueue in `decision_queue.py`, `remedy decision list/show/answer`
   as its only surface, the two surviving gates reading the answer, then the `propose` group's
   deletion paragraph and its ids in `TestDeletedCommands`.
2. `job attach-repo`/`job permit` wait for F269's contract writer (DECISION amend0917-throughput
   D2) — not this feature's to close.
3. The DAG-scheduling key rename D9 executes is now DONE; no further `flight_plan` item is owed.
4. Remaining Acceptance lines: `job budget <id> set`, `worker doctor`, `job run --tasks n` are
   already landed per prior rounds' Built State; confirm the catalog-vs-D4 diff at closure.

## Risks

- 136 findings open by distinct id (unchanged this round); High: R-0803, R-0804, R-0807, none
  this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix) — unchanged.
- `propose`'s deletion is the largest remaining T001 item; DECISION amend0917-throughput D1 fixed
  the design, so the executing round measures exact seams rather than re-deciding shape.
