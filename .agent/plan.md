# Plan — F301 Mission upkeep: every fifth job cleans up

## Goal
A mission keeps its project clean by itself: after every fifth completed job, the next job is an
upkeep job Remedy plans from its own records — the findings earlier jobs left open, the project's
structure measure, and what was replaced and not deleted — by rules a person can read, with a skip
only as a recorded decision (docs/roadmap/features/T7_F301.md; DECISIONs F301 D1 to D3).

## Current Step
Round 4 on `feature/f301-mission-upkeep`: book round 3 and DECISION F301 D3, then T003's setting
`mission.upkeep_every` in `config_keys_mission.py` with the environment guide, and T003's rules in
`packages/orchestration/mission_upkeep.py`: the cadence, the plan, the compiled step, the upkeep
job and the recorded skip, with their tests.

## Next Steps
1. T003 through the command line: `remedy mission continue` makes the upkeep job when it is due,
   `--skip-upkeep <reason>` in `command_catalog_mission.py` records a skip, the lessons test of
   DECISION F301 D2 (4), and the page `docs/system/mission-upkeep-v1.md`.
2. The loop's dispatch path: the upkeep job in place of a dispatch, with R-1233's test of the
   dispatch path's approval; T004, the replaced pairs through a run.
3. T005: the upkeep in `remedy mission show` and the client digest; a fixture mission of six jobs
   whose sixth is the upkeep job; then closure.

## Risks
- The structure ratchet holds every round: no line may be added to a listed function or file, so
  new code goes into the new modules and a listed one is cut first.
- The mission, job and task records change no shape; an upkeep job is known by a key of its
  job's free metadata.
- R-1233 (Low) is owned by F301 and repaired with the change to the dispatch path.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297.
