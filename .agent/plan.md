# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISION F306 D1).

## Current Step
Round 2 on `feature/f306-findings-paydown-v8`, session 1: book round 1, then T003, R-1251 — the
runtime-flow tests give their fixture app a port of their own, and the runner refuses a check
whose health answer came from a process it did not start.

## Next Steps
1. T004 and T005 — the workspace-identity step of `run_manifest.py`, then R-1252.
2. T006 to T008 — R-1235's three steps.
3. The closure, carrying R-1246 by name to the next paydown.

## Risks
- The listener check reads the operating system's socket table; where that read fails, the
  runner keeps today's behaviour and says so in the check's log.
