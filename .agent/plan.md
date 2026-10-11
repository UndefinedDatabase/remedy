# Plan — F297 Findings paydown v7

## Goal
Pay down the open findings F297 owns, each by the repair its own text names, with the evidence
that discharged it (docs/roadmap/features/T2_F297.md; DECISIONs F297 D1 to D10).

## Current Step
Round 9 on `feature/f297-findings-paydown-v7`, the first of session 2: book round 8 with the
resolutions of R-1156, R-1157 and R-1230, and land T021 and T022: R-1219 and R-1220
(DECISION F297 D10).

## Next Steps
1. The next round's first commit books round 9's verdict and the resolutions of R-1219 and
   R-1220.
2. T023 and T024: R-1240 and R-1249.
3. T025 R-1241, the structural step; then the closure sequence.

## Risks
- `do_sequence.py` stands at 994 lines: a slice that grows it draws its boundary first.
- `plan_order_job`, `_cmd_decision_resolve`, `run_pingpong`, `run_job`, `continue_from_node` and
  the files `pingpong_provider.py`, `pingpong_job.py` and `job.py` are on the structure page and
  may not grow.
- R-1240's job is missed through its mission: the approval card reads the mission's contract,
  which a gate result rewrites in the mission record, and a changed mission lists no job.
- R-1235 and R-1246 are carried (the operator allowed R-1246's four reads by DECISION F297 D2,
  and the session's permission settings still refuse them); R-1248 is owned by F305; R-1251 by
  the next findings paydown.
