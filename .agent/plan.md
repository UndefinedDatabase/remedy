# Plan — F301 Mission upkeep: every fifth job cleans up

## Goal
A mission keeps its project clean by itself: after every fifth completed job, the next job is an
upkeep job Remedy plans from its own records — the findings earlier jobs left open, the project's
structure measure, and what was replaced and not deleted — by rules a person can read, with a skip
only as a recorded decision (docs/roadmap/features/T7_F301.md; DECISIONs F301 D1 to D4).

## Current Step
Round 6 on `feature/f301-mission-upkeep`: book round 5, register R-1234 with DECISION F301 D4,
then repair R-1234 — a halted job counts as ended once its mission moves on — with T004's chain
through a real run; the orchestrator's dispatch runs the upkeep job in place of a dispatch, with
R-1233's test of the dispatch path's approval; and the mission upkeep page says so.

## Next Steps
1. T005: the upkeep in `remedy mission show` and the client digest's mission entry, which the
   public API's digest answers; a fixture mission of six jobs whose sixth is the upkeep job.
2. Closure: the one full suite, the self-use item, the evidence package, the STATUS line.

## Risks
- The structure ratchet holds every round: no line may be added to a listed function or file, so
  new code goes into the new modules and a listed one is cut first.
- The mission, job and task records change no shape; an upkeep job is known by a key of its
  job's free metadata.
- R-1233 (Low) and R-1234 (Medium) are owned by F301 and repaired this round.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297.
