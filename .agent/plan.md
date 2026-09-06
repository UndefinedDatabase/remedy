# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, `origin/main` merged in at round 16. Rounds 1 to
19 are reviewed; round 1 FAILED and was repaired, and 2 to 19 PASSED. DECISION
F260 D8 closes this feature at the scope it built; F272 carries the remainder and
was registered in round 18, directly after F260 in the ledger.

## Goal

Session 7 performs SPLIT-AND-CLOSE at the amend0905-throughput soft limit of 7
sessions. The split is ruled and registered, and round 19's integration gate was
GREEN on both sides with both comparison sets empty, which satisfies closure
precondition 2. What remains is the closure sequence itself.

## Current Step

Round 20 is CLOSURE PART 1, the content half: the §3 checklist's one mandated
consolidation pass, the self-use item generated and run for closure precondition
6, and round 19's verdict booked. It touches neither `docs/roadmap/STATUS.md` nor
`README.md`.

## Next Steps

1. Closure part 2: any findings the self-use run reported are registered first;
   then the evidence job, the review zip, and the ledger rotation.
2. Closure part 3: the STATUS accepted flip, the README sync, `consumed_by` set on
   the self-use item, the handback, and the pull request — left UNMERGED as the
   operator's review window.

## Risks

- The self-use run is a real job execution against a real budget. If it raises,
  that is reported with its full traceback and the reviewer rules on it; it is
  never hidden and never retried into silence.
- The consolidation may not lengthen the list. It merges two items into one and
  re-bases the figure the next pass measures against, in the same commit.
