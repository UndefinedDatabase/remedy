# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISIONs F306
D1 and D2).

## Current Step
Session 2, round 6 on `feature/f306-findings-paydown-v8`: book round 5 from `.agent/handoff.md`,
then the step the structure ledger names second for `run_job`: its configuration resolution
becomes a function of its own (before T008 may edit `run_job`).

## Next Steps
1. T008 — the values of `claude_cli.customizations` and `claude_cli.all_tools` join the recorded
   execution configuration, read as optional by the job-input validation; the client interface's
   version rises and its generated pages are regenerated.
2. The closure, carrying R-1246 and R-1252 by name to the next paydown.

## Risks
- The configuration resolution inside `run_job` sets locals the rest of the function reads; the
  extraction must return every one of them unchanged.
