# Plan — F301 Mission upkeep: every fifth job cleans up

## Goal
A mission keeps its project clean by itself: after every fifth completed job, the next job is an
upkeep job Remedy plans from its own records — the findings earlier jobs left open, the project's
structure measure, and what was replaced and not deleted — by rules a person can read, with a skip
only as a recorded decision (docs/roadmap/features/T7_F301.md; DECISION F301 D1).

## Current Step
Round 1 on `feature/f301-mission-upkeep`: claim F301, book F300's round 6, save T001's inventory
as `.agent/f301_inventory.md`, record DECISION F301 D1, and move the dispatch branch of
`execute_move` into `packages/orchestration/orchestrator_dispatch.py` with its boundary on the
structure page.

## Next Steps
1. T002: the project's upkeep ledger, `packages/orchestration/mission_upkeep.py`, with its lines,
   the open findings of a closed job and the cadence count.
2. T003: the boundary and one step of `config.py`, then `mission.upkeep_every`, the compiled
   step, the upkeep job through `remedy mission continue` with `--skip-upkeep`, and through the
   loop's dispatch, with R-1233's test of the dispatch path's approval.
3. T004 and T005: the replaced pairs through a run, and the upkeep in `remedy mission show` and
   the client digest.
4. A fixture mission of six jobs whose sixth is the upkeep job; then closure.

## Risks
- The structure ratchet holds every round: no line may be added to a listed function or file, so
  new code goes into the new modules and a listed one is cut first.
- The mission, job and task records change no shape; an upkeep job is known by a key of its
  job's free metadata.
- R-1233 (Low) is owned by F301 and repaired with T003's change to the dispatch path.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297.
