# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world. Rounds 1 to 21 are reviewed; round 1 FAILED and was
repaired, and 2 to 21 PASSED. DECISION F260 D8 closes this feature at the scope it
built; F272 carries the remainder and was registered in round 18, directly after
F260 in the ledger.

## Goal

SESSION 8 finishes the closure sequence. This round is CLOSURE PART 2, the evidence
half: book round 21's verdict, rotate the ledger, then build the evidence bundle and
the FRESH review zip from a clean tree. The STATUS flip is the part after it.

## Current Step

Round 22 books round 21's PASS into `.agent/live_review.md` as the `Gate: R21`
record, rotates the ledger into `.agent/live_review_archive.md` as its own commit,
and then — committing nothing further — runs the evidence job and builds the review
zip. The handback carries the evidence job id, the package filename, its SHA-256,
the package's absolute directory and the accepted head, because the STATUS line
cannot be authored until those values are measured.

## Next Steps

1. CLOSURE PART 3: the STATUS `[x]` flip and the README capability sync in ONE
   commit, with `consumed_by` set to `F260` on SU-011 in that same commit, then the
   handback, then the pull request — left UNMERGED as the operator's review window.

## Risks

- SU-011 is PENDING and must be marked consumed in the closure commit, not before.
  Nothing else may set it.
- A failing zip build is a closure BLOCKER, not a nuisance: it is reported raw and
  the reviewer decides.
- The rotation re-bases every byte baseline, so the block after it measures its own
  terminal bytes rather than reusing any number from this session.
