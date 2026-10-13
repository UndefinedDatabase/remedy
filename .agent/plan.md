# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISIONs F306
D1 and D2).

## Current Step
Round 4 on `feature/f306-findings-paydown-v8`, session 1: book round 3, DECISION F306 D2 (R-1252
carried), then T006, R-1235's first step: the job-input definition, its field sets, its validation
and its decoder move from `run_manifest.py` to `packages/orchestration/job_input_definition.py`,
re-exported by name.

## Next Steps
1. T007 — R-1235's second step: `ExecutionConfig` and its two serializers out of `pingpong_job.py`.
2. T008 — R-1235's third step: the claude-cli configuration joins the recorded execution
   configuration, read as optional by the validation, and the client interface's version rises.
3. The closure, carrying R-1246 and R-1252 by name to the next paydown.

## Risks
- A name a test replaces on `run_manifest` must stay there with every function that calls it.
