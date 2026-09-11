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

ROUND 67 SPENDS the `--assert=plain` route DECISION F275 D40 chose, and DECISION F275 D41
rules the result. The probe was not modified; only the pytest invocation changed. The
synthetic receivers go from 24 to ZERO, the receiver-joined set goes from 2116 to 2138, its
drop list from 52 to 30, and 22 sites come back with NONE newly dropped. Both remaining
unexplained drops were already ruled by D40 a round ago, so the plain set carries no unruled
drop and half of D40's condition is discharged. The artefact is
`.agent/f275_t003_flip_residue_r67.md`. The round 66 verdict and its two prose slips are
booked here. No production line moves.

## Next Steps

1. RULE THE 54 ruled keys that resolve to no `ast` node at their recorded position, and
   answer first whether the transform's own consumption already loses them — which decides
   whether they are a reporting defect or a live under-selection in every dry run so far.
   That is the whole of what DECISION F275 D41 still holds the write shut on.
2. Point the transform at the plain re-derived set and re-run the flip's dry run, which is
   the first reading of what the re-keying costs or saves in failures rather than in sites.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The site set has yielded four distinct position defects in five rounds — the line key, the
  assertion rewriting, the sweep's own columns and the 54 non-resolving keys — and each was
  invisible to the gate that preceded it.
- `R-0880`'s SECOND obligation is still unbuilt, and the largest residue classes still need
  PRODUCTION-CODE work rather than another transform rule.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
