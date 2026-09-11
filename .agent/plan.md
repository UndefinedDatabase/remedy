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

ROUND 59 re-keys the ruled site set off line numbers as DECISION F275 D34 orders, gives the
transform a precondition that REFUSES on a stale set, and re-runs the dry run against a
control at the same commit. The re-key recovers 2198 of 2198 sites where the line key
recovers 2144, and the run's failures fall from 1476 to 1240 with the `JobPlan`-receiver
attribute class down from 255 lines to 18. The run exposed the mirror defect, finding
`R-0880`: the same set OVER-selects, renaming a field on records the flip does not touch.
The artefact is `.agent/f275_t003_flip_residue_r59.md`. The round 58 verdict, one dated
prose slip and the `R-0878` resolution are booked here.

## Next Steps

1. Resolve the `.status` field by type, in a round of round 53's shape — the descriptor
   probe run twice, unioned with a static sweep — then build DECISION F275 D32's third
   rule family, which this run leaves as the largest cleanly attributed unbuilt rule.
2. Bound `R-0880` statically: read the ruled set against the live record classes, so the
   over-selected sites are known rather than only the ones the suite happens to execute.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store, then the
   closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The three largest residue classes are attributed to an id SHAPE change rather than to a
  rename, and no rule family this chain has written covers them.
- The 42 errors did not move between the two runs and are still undiagnosed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
