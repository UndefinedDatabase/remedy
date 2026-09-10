# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 27 makes the advertisement guard see the class it was built for. Its scanner drops the
`GROUPS` pre-filter that hid every advertisement of a deleted group, gains the single-token
`remedy <something>` form, and counts a closing backtick as a command tail. Eight dead
next-action strings in production code become the live group-first commands, the
`architecture.md` banner loses the `remedy list` the reviewer invented and states the span it
really covers, and the dead advertisements the widening exposes on operator-facing pages are
pinned in a shrink-only allowlist as R-0872. R-0847 closes.

## Next Steps

1. R-0872's first half: delete the four pages that document command groups F275 deleted
   whole, and repair `core-product-spine-v0.md`, lowering the allowlist by 21.
2. R-0872's second half: the flat pre-Step-38 CLI in `architecture.md` and the one site in
   `vocabulary.md`, lowering the allowlist to zero and deleting the ratchet with it.
3. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice.
4. T003, the classic runner, which T002's ruling is the prerequisite for.
5. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 88 by distinct id at this round's base `c370dcee`, computed mechanically
  from the record. This round registers one and resolves one, leaving 88. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- The allowlist is the first mechanism in this feature that lets a known defect sit on disk
  under a green suite. It is bounded by two assertions rather than by intent: it may not
  grow, and it may not keep an entry whose advertisement is gone.
