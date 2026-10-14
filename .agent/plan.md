# Plan — F078 Autonomy levels

## Goal
A configured autonomy level, `L2` to `L5`, states what Remedy may start on its own; one shared
check answers every starting seam from a sixteen-cell matrix, a level of `L3` or higher needs the
passed gauntlet, every level change needs a decision record, and the level is visible where it
matters (docs/roadmap/features/T3_F078.md; DECISION F078 D1).

## Current Step
Session 1, round 1 on `feature/f078-autonomy-levels`: claim F078, book F055's round 9, move the
four watchdog keys to `packages/orchestration/config_keys_autonomy.py`, and land T001 — the three
keys, the matrix with its check, and the loading of the level with its refusals and its record.

## Next Steps
1. T002: the check at `dispatch_milestone_job` and at the operator's own starting commands; a
   refused start is recorded, visible and can be started by hand (DECISION F078 D2, written with
   that patch).
2. T003: the caps of `L5`, the level in `remedy status` and the reports, and the end-to-end proof
   per level.
3. The closure sequence: the one full suite, the self-use run, the evidence and the pull request.
