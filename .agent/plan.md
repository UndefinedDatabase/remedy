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

ROUND 61 builds DECISION F275 D32's THIRD retype rule family against the nine sites
DECISION F275 D35 names, and re-runs the dry run against a control at the same production
tree. Rule T8 fires exactly nine times and no other rule count moves. The class it was
built for is at ZERO, down from 61 exception lines, and total failures fall from 1240 to
1186. All three of D32's rule families are now accounted for. The artefact is
`.agent/f275_t003_flip_residue_r61.md`. The round 60 verdict is booked here.

## Next Steps

1. Bound `R-0880` statically: read the ruled set's owner verdicts against the live record
   classes, so the over-selected sites are known rather than only the ones a run reaches,
   and give the transform the refusal `R-0879` already gave it for stale keys.
2. Diagnose the three largest residue classes, which are reads of an id whose SHAPE
   changed rather than renames, and rule whether they are a fourth rule family or a
   consequence of records written to disk under the classic shape.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store, then the
   closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- 1186 failures is not a landable state, and no rule family of D32's kind is left to build.
- The 42 errors have not moved across three runs and are still undiagnosed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
