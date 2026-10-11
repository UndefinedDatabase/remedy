# Plan — F297 Findings paydown v7

## Goal
Pay down the open findings F297 owns, each by the repair its own text names, with the evidence
that discharged it (docs/roadmap/features/T2_F297.md; DECISIONs F297 D1 to D12).

## Current Step
Round 11 on `feature/f297-findings-paydown-v7`, session 2: book round 10 with the resolutions of
R-1240 and R-1249, and land T025: R-1241, the structural step that moves the burn alarm's trip
handler out of `run_job` into `packages/orchestration/job_burn.py`, then the samples kept in the
job record (DECISION F297 D12).

## Next Steps
1. The next round's first commit books round 11's verdict and the resolution of R-1241.
2. The closure sequence, by `docs/roadmap/STATUS_closure_protocol.md`: the carried findings
   R-1235 and R-1246 named for the next paydown, the integration gate's one full suite, the
   evidence, the next paydown's registration and the STATUS flip.

## Risks
- `do_sequence.py` stands at 994 lines: a slice that grows it draws its boundary first.
- `plan_order_job`, `_cmd_decision_resolve`, `run_pingpong`, `run_job`, `continue_from_node` and
  the files `pingpong_provider.py`, `pingpong_job.py` and `job.py` are on the structure page and
  may not grow.
- R-1235 and R-1246 are carried (the operator allowed R-1246's four reads by DECISION F297 D2,
  and the session's permission settings still refuse them); R-1248 is owned by F305; R-1251 by
  the next findings paydown.
