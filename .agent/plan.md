# Plan — F078 Autonomy levels

## Goal
A configured autonomy level, `L2` to `L5`, states what Remedy may start on its own; one shared
check answers every starting seam from a sixteen-cell matrix, a level of `L3` or higher needs the
passed gauntlet, every level change needs a decision record, and the level is visible where it
matters (docs/roadmap/features/T3_F078.md; DECISIONs F078 D1 to D4).

## Current Step
Round 4 (session 2) on `feature/f078-autonomy-levels-2`: merge the first branch onto `main`
(DECISION F078 D4), book round 3, and refuse an L5 cap of `claim_idea_start` that is not a
number of at least 0.

## Next Steps
1. Prove each level's increment end to end and every existing gate at `L5`; decide whether the
   new `autonomy` key of `remedy status`'s answer is a contract change after 1.22 (DECISION
   F313 D1's rule for a grown answer); bring `docs/system/autonomy-levels-v1.md` up to date; add
   one line each to the files of F063 and F068.
2. The closure sequence: the one full suite, the consolidation pass, the self-use run, the
   evidence and the package, the Built State, the STATUS line and the pull request.

## Risks
- The integrity check fails on High findings F078 does not own (DECISION F310 D7, Q20).
- The first branch `feature/f078-autonomy-levels` stays on the remote until the operator deletes it.
