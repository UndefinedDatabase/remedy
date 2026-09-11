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

ROUND 66 RULES the three sites DECISION F275 D39 held the write shut on, and DECISION F275
D40 records the result. They rule three ways: one correct drop, one site that was never in
the committed set, and one wrong drop whose cause is pytest's assertion rewriting — which
reaches 22 of the 52 drops, so the re-derived set is NOT safe to consume. A second and
independent defect is measured beside it: 54 of the 2198 ruled keys resolve to no `ast`
node at their recorded position, which is what the `long_run_executor.py:504` disagreement
round 64 reported turns out to be. The artefact is `.agent/f275_t003_flip_residue_r66.md`.
The round 65 verdict and its prose slip are booked here. No production line moves.

## Next Steps

1. RE-DERIVE from a PLAIN run: two suite passes under the committed probe with
   `--assert=plain`, rebuild the set, and confirm the 22 rewriting drops become refusals
   that the join keeps. That is the first half of what DECISION F275 D40 holds shut.
2. RULE THE 54 ruled keys that resolve to no `ast` node, and measure whether the
   transform's own consumption already loses them — which decides whether they are a
   reporting defect or a live under-selection in every dry run taken so far.
3. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
4. THE FLIP, then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The site set has now yielded three distinct position defects in four rounds — the line
  key, the rewriting and the sweep's own columns — and each was invisible to the gate that
  preceded it.
- `R-0880`'s SECOND obligation is still unbuilt, and the largest residue classes still need
  PRODUCTION-CODE work rather than another transform rule.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
