# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world. Rounds 1 to 22 are reviewed; round 1 FAILED and was
repaired, and 2 to 22 PASSED. DECISION F260 D8 closes this feature at the scope it
built; F272 carries the remainder and was registered in round 18, directly after
F260 in the ledger.

## Goal

SESSION 8 finishes the closure sequence. Round 22 booked round 21 and rotated the
ledger, but its review package built BLOCKED_EVIDENCE because the block ordered the
wrong review base. This round repairs the cause and rebuilds the package; the STATUS
flip is the round after it.

## Current Step

Round 23 books round 22's verdict, registers `R-0817` — the closure protocol's
producer-pitfall list never stated that `base_commit` is the branch's FORK POINT
rather than its merge base — repairs that gap in
`docs/roadmap/STATUS_closure_protocol.md`, and then, committing nothing further,
reruns the evidence job and the review zip from base `b5cd6c20`, proving before the
run that the ancestry-path chain and the plain commit list over that base are the
same length.

## Next Steps

1. THE CLOSURE ROUND: book round 23's verdict and author `Done: R-0817`; then the
   STATUS `[x]` flip and the README capability sync in ONE commit, with
   `consumed_by` set to `F260` on SU-011 in that same commit, then the handback,
   then the pull request — left UNMERGED as the operator's review window.

## Risks

- SU-011 is PENDING and must be marked consumed in the closure commit, not before.
- A failing zip build is a closure BLOCKER. It is reported raw and the reviewer
  decides; the base, the evidence fields and the sources are never adjusted to make
  a package go READY.
- The ledger rotation already ran at `6cebdce6` and is not repeated; byte baselines
  are re-measured from each target's own terminal byte.
