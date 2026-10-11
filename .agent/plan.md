# Plan — F297 Findings paydown v7

## Goal
Pay down the open findings F297 owns, each by the repair its own text names, with the evidence
that discharged it (docs/roadmap/features/T2_F297.md; DECISIONs F297 D1 to D11).

## Current Step
Round 10 on `feature/f297-findings-paydown-v7`, session 2: book round 9 with the resolutions of
R-1219 and R-1220, and land T023 and T024: R-1240 and R-1249 (DECISION F297 D11), with operator
question Q14 on the vocabulary page.

## Next Steps
1. The next round's first commit books round 10's verdict and the resolutions of R-1240 and
   R-1249.
2. T025 R-1241, the structural step: the burn alarm's trip handler leaves `run_job` for
   `packages/orchestration/job_burn.py`, and `run_job`'s row and pins fall by what moves.
3. The closure sequence.

## Risks
- `do_sequence.py` stands at 994 lines: a slice that grows it draws its boundary first.
- `plan_order_job`, `_cmd_decision_resolve`, `run_pingpong`, `run_job`, `continue_from_node` and
  the files `pingpong_provider.py`, `pingpong_job.py` and `job.py` are on the structure page and
  may not grow.
- R-1235 and R-1246 are carried (the operator allowed R-1246's four reads by DECISION F297 D2,
  and the session's permission settings still refuse them); R-1248 is owned by F305; R-1251 by
  the next findings paydown.
