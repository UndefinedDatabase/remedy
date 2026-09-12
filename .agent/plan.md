# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 82 FIXES THE FLIP'S INPUT SET ON DISK AND MAKES IT REPRODUCIBLE. The corrected set
loses the two sites DECISION F275 D55 names, is re-keyed onto the tree the flip will run on
by the committed round 59 stage, and is re-checked by the committed round 73 owner check;
the generator that does all three is committed with the artefact it writes. Two controls sit
beside the re-key, and the second one found something: removing a ruled statement does not
make the stage refuse, it makes the next attribute of that name in that scope answer to the
key and carries the old owner verdict onto it. That is `R-0880`'s defect by a second route,
so no id is minted. The round 81 verdict and its prose slip are booked.

## Next Steps

1. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the
   input is re-derived by round 82's committed generator at the flip's own base, and any
   site fallen to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, which are
  gitignored. Rebuilding those needs the round 53 probe run, which no round has re-taken.
- THE RE-KEY CANNOT SEE A DELETED RULED SITE. Any round between here and the flip that
  removes a ruled read moves that site's verdict onto its neighbour with nothing said.
- The open set is 87 by distinct id at this round's base, with `R-0880` open. Four are High
  — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
