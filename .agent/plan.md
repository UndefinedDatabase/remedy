# Plan — reliability campaign: cancel, stale work, truthful lifecycle (operator order 2026-10-17)

## Goal
Cancellation really ends an order's lifecycle, abandoned work leaves the active views for good
(evidence kept), every lifecycle word is true, and clients control it all over the public API.
Branch `feature/order-cancel` from PR 360's head `9b172a16c` (merge order: 360 first, then this);
worktree `.remedy-wt/order-cancel`. Outside the roadmap queue (F078 stays next). `.agent/STOP`, the
supervisor and the live checkout untouched; no merge, no deploy.

## Current Step
All steps done (findings R-1338..R-1344, decisions exec-1017c D1-D10, handoff written). Now: the
one full local gate on the final tree, then the PR (not merged).

## Next Steps
- Operator: merge PR 360, then this PR; restart `remedy serve`.
- Open: R-1343's loop half (`--test-command` refusal reads `test_failed`); the calibration run
  proposed in the handoff (needs an authorized model budget).

## Risks
- `pingpong_job.py`, `decision_queue.py`, `command_catalog.py` are at their structure rows: every
  edit there is line-neutral, new logic lives in new modules.
- A planning order stops only when its planner call returns (safe points between steps).
