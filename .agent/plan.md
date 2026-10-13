# Plan — F306 Findings paydown v8

## Goal
Pay down the four findings open at the claim — R-1235, R-1246, R-1251 and R-1252 — each by the
repair its own text names, after the structural steps the structure ledger owes for the files they
touch, or carry it by name to the next paydown (docs/roadmap/features/T2_F306.md; DECISION F306 D1).

## Current Step
Round 1 on `feature/f306-findings-paydown-v8`, session 1: claim F306, book F203's round 10, write
the slice list, and land T002, the move of `dev_server.py`'s ports and readiness probe to
`packages/runtimes/dev_server_ports.py`, re-exported by name, with the ratchet rows lowered.

## Next Steps
1. T003 — R-1251: a port of its own per runtime-flow test, and the runner's refusal of a health
   answer from a process it did not start.
2. T004 and T005 — the workspace-identity step of `run_manifest.py`, then R-1252.
3. T006 to T008 — R-1235's three steps.
4. The closure, carrying R-1246 by name to the next paydown.

## Risks
- A structural step that moves a name a test replaces on the old module must leave that name and
  its caller together (docs/system/structure-ledger-v1.md, "Files").
