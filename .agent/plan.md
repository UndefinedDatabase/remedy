# Plan — amend1016p (operator order remedy-simple-orders, simple orders stay simple)

## Goal
A bounded order gets one job, one task and no planner call whatever door it came through; the full
lane keeps no constraint-only milestone and no checking-only task; the reviewer judges meaning.
Branch feature/simple-orders-fast-lane. Finding R-1336, DECISION amend1016p D1 to D3. Priority
registration; Rule A5's queue (F078) untouched, `.agent/STOP` kept.

## Current Step
Done: `order_scope.py`, the lane rule, the two plan filters, the reviewer preamble, the tests (the
HTTP path with the app's order among them), the do guide and the sandbox page.

## Next Steps
- Pull request; merge only on decodeux's word, since a merge changes what the next order runs.
- After the merge: the README lab order sent again as a fresh order.
