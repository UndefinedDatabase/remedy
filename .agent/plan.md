# Plan — F301 Mission upkeep: every fifth job cleans up

## Goal
A mission keeps its project clean by itself: after every fifth completed job, the next job is an
upkeep job Remedy plans from its own records — the findings earlier jobs left open, the project's
structure measure, and what was replaced and not deleted — by rules a person can read, with a skip
only as a recorded decision (docs/roadmap/features/T7_F301.md; DECISIONs F301 D1 to D5).

## Current Step
Round 7 on `feature/f301-mission-upkeep`: book round 6 with the resolutions of R-1233 and R-1234,
record DECISION F301 D5, then T005: `upkeep_preview`, the digest's three upkeep counts with the
client interface at 1.6, and the upkeep section of `remedy mission show`, with the page.

## Next Steps
1. The acceptance fixture: a mission of six jobs whose sixth is the upkeep job naming the planted
   finding, the planted oversized file and the planted replacement, an old mission and job record
   loading and running unchanged, and the digest naming the jobs left; the Built State.
2. Closure: the one full suite, the self-use item, the evidence package, the STATUS line, the pull
   request.

## Risks
- The structure ratchet holds every round: no line may be added to a listed function or file, so
  new code goes into the new modules and a listed one is cut first.
- The mission, job and task records change no shape; an upkeep job is known by a key of its
  job's free metadata.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297.
