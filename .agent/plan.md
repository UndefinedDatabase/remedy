# Plan — reliability campaign: cancel, stale work, truthful lifecycle (operator order 2026-10-17)

## Goal
Cancellation really ends an order's lifecycle, abandoned work leaves the active views for good
(evidence kept), every lifecycle word is true, and clients control it all over the public API.
Branch `feature/order-cancel` from PR 360's head `9b172a16c` (merge order: 360 first, then this);
worktree `.remedy-wt/order-cancel`. Outside the roadmap queue (F078 stays next). `.agent/STOP`, the
supervisor and the live checkout untouched; no merge, no deploy.

## Current Step
Done: 1 findings R-1338..R-1342; 2 `job_cancel.py` (job cancel, settle at safe point and at run
start, no decisions, digest hiding rule deleted); 3 `order_cancel.py` (`client cancel-order`, the
walk reads the request before/after every step and before every apply, `phase`/`cancel`); CLI,
HTTP 1.19, docs, decisions exec-1017c D1-D4. Now: commits, then step 4.

## Next Steps
4. Story: a waiting job says what it waits for (R-1340); a cancelled job reads cancelled, a stop
   reads stopped; an order job whose predecessor was cancelled or declined is not "waiting".
5. R-1341/R-1342 (lane honesty, named files unchanged) if the evidence supports a small fix.
6. P1 investigations (efficiency, verification across project types, memory) recorded with
   evidence; owner and neighbouring tests; one full local gate on the final commit; PR (not merged).

## Risks
- `pingpong_job.py`, `decision_queue.py`, `command_catalog.py` are at their structure rows: every
  edit there is line-neutral, new logic lives in new modules.
- A planning order stops only when its planner call returns (safe points between steps).
