# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, `origin/main` merged in at round 16. Rounds 1 to
18 are reviewed; round 1 FAILED and was repaired, and 2 to 18 PASSED. DECISION
F260 D8 (round 17) closes this feature at the scope it built; F272 carries the
remainder and was registered in round 18, directly after F260 in the ledger.

## Goal

Session 7 performs SPLIT-AND-CLOSE at the amend0905-throughput soft limit of 7
sessions. The split is ruled and registered; what remains is the closure sequence
itself, and the integration gate that closure precondition 2 requires.

## Current Step

Round 19 is the INTEGRATION GATE: the full suite run once on this branch and once
in a disposable worktree at the merge base `f957c4c6`, with UI parity restored
before the base run, and the two failure sets compared. It measures; it does not
repair. A reproducible branch-only failure coupled to feature code is a BLOCKER
and buys its own reviewer-gated round.

## Next Steps

1. Closure part 1: the self-use item, the evidence job and the review zip.
2. Closure part 2: the verdict bookings and the ledger rotation.
3. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- The base worktree lacks `apps/ui/node_modules` and `apps/ui/dist`, and a copy
  of them carries stale mtimes that make the UI read as un-built. Both are
  repaired before the base run and the repair is proved by calling the real
  predicate, not by asserting it.
- The self-use queue is EXHAUSTED — all ten entries carry a `consumed_by` — so
  closure precondition 6 runs `generate_and_append_if_empty` FIRST and records
  `self-use NONE (queue exhausted)` only after that also answers `None`.
