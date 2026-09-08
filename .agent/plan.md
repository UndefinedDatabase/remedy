# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8 — the split-and-close default operator
amendment amend0905-throughput makes standing at the soft limit, which this feature reached at
session seven of seven.

## Current Step

The registration round: book round 16's PASS verdict, then register F275 in ONE atomic ledger
commit — the STATUS line directly after F274's inside the same Tier 2 heading, the feature file,
the `TOTAL_FEATURES` pin and the README counters, plus the `Depends on` edit in every open
feature naming F274 — and give F274's own file a Built State section naming which slices moved.

## Next Steps

1. The integration-gate round: the full suite per docs/agents/integration_gate.md, whose verdict
   closure precondition 2 re-confirms.
2. The self-use item closure precondition 6 requires. Every queue item is consumed, so
   `generate_and_append_if_empty` runs FIRST; whatever it yields is planned and run to the normal
   approval gate, and every defect its findings reader returns is registered before the close.
3. The closure sequence itself: the remaining verdict bookings, the ledger rotation by
   `scripts/rotate_live_review.py` as its own commit, the evidence job, the fresh review zip, the
   STATUS `[x]` flip with the README sync in one commit, and the pull request.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
- The registration's four ledger pins must land in ONE commit; splitting them leaves an
  intermediate state in which `tests/docs/` is red.
