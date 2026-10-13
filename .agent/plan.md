# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISIONs F306
D1 and D2).

## Current Step
Round 5 on `feature/f306-findings-paydown-v8`, session 1: book round 4, then T007, R-1235's second
step: `ExecutionConfig` and its two serializers move from `pingpong_job.py` to
`packages/orchestration/execution_config.py`, re-exported by name, and the client interface test's
source pointer follows them.

## Next Steps
1. T008 — R-1235's third step: the claude-cli configuration joins the recorded execution
   configuration, read as optional by the validation, and the client interface's version rises.
2. The closure, carrying R-1246 and R-1252 by name to the next paydown.

## Risks
- A name a test replaces on `pingpong_job` must stay there with every function that calls it.
