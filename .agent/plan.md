# Plan — F078 Autonomy levels

## Goal
A configured autonomy level, `L2` to `L5`, states what Remedy may start on its own; one shared
check answers every starting seam from a sixteen-cell matrix, a level of `L3` or higher needs the
passed gauntlet, every level change needs a decision record, and the level is visible where it
matters (docs/roadmap/features/T3_F078.md; DECISIONs F078 D1 to D9). Accepted PASS_WITH_RISKS on
2026-10-21.

## Current Step
Round 11 (session 2), the closing round: book round 10 and resolve R-1394, DECISION F078 D9 (no
rotation this closure), the Built State brought current, accept F078 in STATUS with the README sync
and SU-069's `consumed_by`, and open the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F078's pull
   request; then Rule A5 proposes the next feature, F141.

## Risks
- The integrity check fails on High findings F078 does not own (DECISION F310 D7, Q20).
- The first branch `feature/f078-autonomy-levels` stays on the remote until the operator deletes it.
