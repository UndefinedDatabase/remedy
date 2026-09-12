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

ROUND 76 TAKES THE FLIP'S DRY RUN AGAINST THE CORRECTED INPUTS OF ROUNDS 67 AND 69 TOGETHER,
which DECISIONs F275 D41, D42 and D44 each deferred by name, and the answer is that NEITHER
SET IS THE FLIP'S INPUT. The two arms differ in the ruled site set alone. The round 67 plain
re-derivation is a strict subset of the round 53 committed set, 60 sites smaller, and it costs
134 additional bad test nodes: it breaks 172 and fixes 38. The cause is measured rather than
inferred — it removes every production record class `R-0880` names from the residue, 59
over-selection frames falling to 1, and introduces 231 under-selection frames where the round
53 set has none. DECISION F275 D50 records the route. The round 75 verdict and its two prose
slips are booked.

## Next Steps

1. Partition the 60 dropped sites into correctly and wrongly dropped, by carrying each
   over-selection frame back through the re-key to the ruled site that produced it. That
   partition IS the flip's input set, and this round establishes that such a set exists.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, on the partitioned set, carrying DECISION F275 D48's obligations: the full suite
   is the backstop, and the thin set is re-derived before the flip with any site fallen to
   zero witnesses treated as a stop.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- THE FLIP'S INPUT SET IS WRONG IN BOTH DIRECTIONS and this round is the first to measure
  both in one pass. Neither arm is near green: 1227 bad nodes under the better of the two.
- A UNIT IS PART OF A NUMBER. This round counts LOCATION FRAMES where `R-0880` counts
  `E <Exc>` lines, and says so rather than comparing the two figure for figure.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
