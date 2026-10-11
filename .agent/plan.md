# Plan — F297 Findings paydown v7

## Goal
Pay down the open findings F297 owns, each by the repair its own text names, with the evidence
that discharged it (docs/roadmap/features/T2_F297.md; DECISIONs F297 D1 to D6).

## Current Step
Round 5 on `feature/f297-findings-paydown-v7`: book round 4 with the resolutions of R-1250 and
R-1247, register R-1251, and land T015: R-1236 (DECISION F297 D6).

## Next Steps
1. Book round 5's verdict and the resolution of R-1236 in the next round's first commit.
2. T016 R-1149.
3. T017 and T018: R-1139 with R-1225, and R-1158.
4. T019 to T024: R-1156 with R-1157, R-1230, R-1219, R-1220, R-1240 and R-1249.
5. T025 R-1241, the structural step; then the closure sequence.

## Risks
- `mission_state.py` stands at 1000 lines with no row, and `do_sequence.py` at 994: a slice that
  grows either draws its boundary on the structure page first.
- `plan_order_job`, `_cmd_decision_resolve`, `run_pingpong`, `run_job` and the files
  `pingpong_provider.py` and `pingpong_job.py` are on the structure page and may not grow.
- R-1235 and R-1246 are carried (the operator allowed R-1246's four reads by DECISION F297 D2,
  and the session's permission settings still refuse them); R-1248 is owned by F305; R-1251,
  registered in round 5, is owned by the next findings paydown.
