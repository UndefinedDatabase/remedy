# Plan — reliability campaign: cancel, stale work, truthful lifecycle (operator order 2026-10-17)

## Goal
Cancellation really ends an order's lifecycle, abandoned work leaves the active views for good
(evidence kept), every lifecycle word is true, and clients control it all over the public API.
Branch `feature/order-cancel` from PR 360's head `9b172a16c` (merge order: 360 first, then this);
worktree `.remedy-wt/order-cancel`. Outside the roadmap queue (F078 stays next). `.agent/STOP`, the
supervisor and the live checkout untouched; no merge, no deploy.

## Current Step
1. Findings R-1338 to R-1342 registered from the review of PR 360 (before any code change).

## Next Steps
2. `job_cancel.py`: a terminal cancel of one job (`remedy job cancel`, `POST /api/v1/jobs/{job}/cancel`);
   a running job settles `cancelled` at its next safe point (`_stop_job`), a run of a cancelled job is
   refused; a cancelled job has no open decision; the digest's never-ran hiding rule is deleted.
3. `order_cancel.py`: `remedy client cancel-order`, `POST /api/v1/orders/{order}/cancel`; a marker
   the walk reads before every step and before every apply; the order's jobs cancelled; the order
   answer's `cancel` and `phase`.
4. Story: a waiting job says what it waits for (R-1340); a cancelled job reads cancelled, a stop
   reads stopped.
5. R-1341/R-1342 (lane honesty, named files unchanged) if the evidence supports a small fix.
6. Docs (public API, machine client contract, do guide), interface version, decisions; owner and
   neighbouring tests; one full local gate on the final commit; PR (not merged).

## Risks
- `pingpong_job.py`, `decision_queue.py`, `command_catalog.py` are at their structure rows: every
  edit there is line-neutral, new logic lives in new modules.
- A planning order stops only when its planner call returns (safe points between steps).
