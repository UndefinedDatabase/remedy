# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, `origin/main` merged in at round 16. Rounds 1 to
20 are reviewed; round 1 FAILED and was repaired, and 2 to 20 PASSED. DECISION
F260 D8 closes this feature at the scope it built; F272 carries the remainder and
was registered in round 18, directly after F260 in the ledger.

## Goal

Session 7 performs SPLIT-AND-CLOSE at the amend0905-throughput soft limit of 7
sessions. The split is RULED and REGISTERED, the integration gate was GREEN on both
sides with both comparison sets empty, the §3 checklist has had its one mandated
consolidation pass, and closure precondition 6's self-use item has been generated
and run. What remains is the closure's evidence half.

## Current Step

Round 21 books round 20, registers the self-use run's outcome as a RECURRENCE of
the open finding R-0784 rather than a new id, and repairs one garbled phrase the
reviewer's round-20 slice landed in the §3 checklist. THIS SESSION ENDS AFTER IT.

## Next Steps

1. CLOSURE PART 2, first commit: book round 21's verdict. Then the evidence job
   (`create_manual_completion_bundle(review_feature_id='f260', ...)`), the review
   zip from a clean tree, and `python3 scripts/rotate_live_review.py` as its OWN
   commit — after the bookings and before the STATUS flip.
2. CLOSURE PART 3: the STATUS `[x]` flip and the README sync in ONE commit, with
   `consumed_by` set to `F260` on SU-011 in that same commit, then the handback,
   then the pull request — left UNMERGED as the operator's review window.

## Risks

- The self-use queue's SU-011 is PENDING and must be marked consumed in the
  closure commit, not before. Nothing else may set it.
- The ledger rotation re-bases every byte baseline, so the block after it measures
  its own terminal bytes rather than reusing any number from this session.
