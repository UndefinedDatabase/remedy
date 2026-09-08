# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit. AT SESSION SEVEN OF SEVEN THE SOFT LIMIT
BINDS, so the goal is now the amend0905-throughput SPLIT-AND-CLOSE default: close F274 at the edge
work it actually built, and carry the cluster deletion, the atomic record flip and the classic
runner to a follow-up feature registered directly after it.

## Current Step

The closure sequence's first round: book round 15's PASS verdict and the second R-0819 recurrence
this feature owes, then record DECISION F274 D8 — the dated split ruling with its scope report, its
rejected alternatives and its reversal. No line under `packages/`, `apps/` or `tests/` moves.

## Next Steps

1. Register the follow-up feature in ONE atomic ledger commit — the STATUS line directly after
   F274's inside the same Tier 2 heading, the feature file, the `TOTAL_FEATURES` pin, the README
   counters, and the `Depends on` edit in every open feature naming F274 — and give F274's own file
   a Built State section naming which slices moved.
2. The integration-gate round: the full suite per docs/agents/integration_gate.md.
3. The self-use item closure precondition 6 requires. The queue holds no pending item, so
   `generate_and_append_if_empty` runs first, then the item is planned and run to the approval gate.
4. The closure sequence itself: the remaining verdict bookings, the ledger rotation, the evidence
   job, the fresh review zip, the STATUS `[x]` flip with the README sync, and the pull request.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
