# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISIONs F306
D1 and D2).

## Current Step
Session 2, round 6 on `feature/f306-findings-paydown-v8`: book round 5, then the structure ledger's
step (2) for `run_job`: its configuration resolution becomes `resolve_job_execution_config` in
`packages/orchestration/execution_config.py`, re-exported by name (before T008 may edit it).

## Next Steps
1. T008 — the values of `claude_cli.customizations` and `claude_cli.all_tools` join the recorded
   execution configuration through a resolver of their own that `resolve_job_execution_config`
   composes, read as optional by the job-input validation; the client interface's version rises
   and its generated pages are regenerated.
2. The closure, carrying R-1246 and R-1252 by name to the next paydown.

## Risks
- `run_job` reads fourteen of the resolved values after the resolution; each is rebound from the
  returned record, so the run still executes exactly what was recorded.
