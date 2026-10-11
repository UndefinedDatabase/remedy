# Plan — F297 Findings paydown v7

## Goal
Pay down the open findings F297 owns, each by the repair its own text names, with the evidence
that discharged it (docs/roadmap/features/T2_F297.md; DECISIONs F297 D1 to D8).

## Current Step
Round 7 on `feature/f297-findings-paydown-v7`: book round 6 with the resolution of R-1149, and
land T017 and T018: R-1139 with R-1225's measurement, and R-1158 (DECISION F297 D8).

## Next Steps
1. Book round 7's verdict and the resolutions of R-1139, R-1225 and R-1158 in the next round's
   first commit.
2. T019 to T024: R-1156 with R-1157, R-1230, R-1219, R-1220, R-1240 and R-1249.
3. T025 R-1241, the structural step; then the closure sequence.

## Risks
- `do_sequence.py` stands at 994 lines: a slice that grows it draws its boundary first.
- `plan_order_job`, `_cmd_decision_resolve`, `run_pingpong`, `run_job`, `continue_from_node` and
  the files `pingpong_provider.py`, `pingpong_job.py` and `job.py` are on the structure page and
  may not grow.
- R-1235 and R-1246 are carried (the operator allowed R-1246's four reads by DECISION F297 D2,
  and the session's permission settings still refuse them); R-1248 is owned by F305; R-1251 by
  the next findings paydown.
