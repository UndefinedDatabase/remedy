# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 15 books round 14's independently-reviewed PASS (Gate: F280 R14, no prose slip, no new
finding) and executes DECISION amend0917-throughput D1: `decision_queue.py` gains a `proposal`
decision type mirroring `can_finalize`'s own blocking predicate, `decision resolve` gains a
`proposal:` branch answering approve/reject/defer, and the `propose` group — seven commands,
their catalog entries, their handler module and their dedicated tests — is deleted whole with
no alias, per DECISION F280 D10, which also names two gates D1 did not (`worker_queue.py`,
the dashboard-v2 section) that need no code change.

## Next Steps

1. `job attach-repo`/`job permit` wait for F269's contract writer (DECISION amend0917-throughput
   D2) — not this feature's to close.
2. `propose`'s deletion (this round) was T001's largest remaining item; after round 15 the
   catalog owes only the two D4 words already confirmed landed below.
3. Remaining Acceptance lines: `job budget <id> set`, `worker doctor`, `job run --tasks n` are
   already landed per prior rounds' Built State; confirm the catalog-vs-D4 diff at closure.
4. If T001 and the Acceptance list both hold after round 15, the next round is F280's closure
   sequence (integration gate, full suite, STATUS flip) per DECISION amend0917-throughput D4.

## Risks

- 137 findings open by distinct id after this round (136 plus R-0941); High: R-0803, R-0804,
  R-0807, none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941 (owned
  F273, minted this round) — unchanged/new.
- The `proposal` decision type is new territory (no existing 3-way approve/reject/defer decision
  to model verbatim); round 15's own targeted tests and mutation red-proofs are this round's
  only correctness evidence until closure's integration gate runs the full suite once.
